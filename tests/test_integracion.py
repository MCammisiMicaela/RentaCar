import os, sys, json, pathlib, shutil, tempfile, importlib, datetime, types, hashlib
from contextlib import contextmanager

PROJECT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from servicios.persistencia import cargar_json, guardar_json
from servicios.gestion_reservas import cargar_reservas, crear_reserva, cancelar_reserva, auto_disponible, calificar_reserva, normalizar_reservas, obtener_reservas_usuario
from servicios.gestion_autos import cargar_autos, guardar_autos
from servicios.seguridad import crear_hash_contrasena, verificar_contrasena
from servicios.autenticacion import validar_login
from servicios.gestion_usuarios import cargar_usuarios, guardar_usuarios
from clases.cliente import Cliente
from clases.auto import Auto

def fixture_workspace(fn):
    original=pathlib.Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        pathlib.Path('datos').mkdir()
        try:fn()
        finally:os.chdir(original)


def test_passwords():
    hash1=crear_hash_contrasena('TestPassword123!')
    assert hash1.startswith('pbkdf2_sha256$')
    assert verificar_contrasena('TestPassword123!',hash1)
    assert not verificar_contrasena('BAD',hash1)
    assert not verificar_contrasena('bad','plaintext')
    def test():
        usuario=Cliente('prueba','Prueba','Usuario','01/01/2000','3421234567',hash1)
        guardar_usuarios([usuario]); assert cargar_usuarios()[0].contraseña==hash1
        assert validar_login('prueba','TestPassword123!')[0]
        assert not validar_login('prueba','mal')[0]
        assert validar_login('no existe','cualquiera')[0] is False
        usuario.cambiar_contraseña('OtroSecreto456')
        assert verificar_contrasena('OtroSecreto456',usuario.contraseña)
    fixture_workspace(test)


def test_old_autos():
    def go():
        old={'AAA001':{'patente':'AAA001','marca':'Ford','modelo':'K','categoria':'Chico','caracteristica':'5 puertas','pasajeros':4,'color':'azul','precio_por_dia':10000,'foto':'auto.png','bloqueado':False,'disponibilidad':[]}}
        guardar_json('datos/autos.json',old)
        autos=cargar_autos()
        assert len(autos)==1
        assert autos[0].transmision=='Sin especificar'
        assert autos[0].datos_adicionales['caracteristica']=='5 puertas'
        guardar_autos(autos)
        data=json.loads(pathlib.Path('datos/autos.json').read_text())
        assert data['AAA001']['caracteristica']=='5 puertas'
        assert data['AAA001']['transmision']=='Sin especificar'
    fixture_workspace(go)


def test_booking():
    def go():
        today=datetime.date.today(); d=today+datetime.timedelta(days=1);h=d+datetime.timedelta(days=2)
        veh=Auto('AAA001','Ford','Ka','Chico','Manual',4,'Azul',12000,'auto.png')
        guardar_autos([veh])
        assert cargar_json('datos/reservas.json') == []
        exito,msg=crear_reserva('cliente','AAA001',d.isoformat(),h.isoformat());assert exito,msg
        assert not crear_reserva('otro','AAA001',d.isoformat(),h.isoformat())[0]
        reservas=cargar_reservas(); assert len(reservas)==1
        rid=reservas[0]['id_reserva'];assert rid=='R-0001'
        assert reservas[0]['puntaje'] is None
        assert not cancelar_reserva(rid,'otro')[0]
        assert cancelar_reserva(rid,'cliente')[0]
        assert not cancelar_reserva(rid,'cliente')[0]
        assert crear_reserva('otro','AAA001',d.isoformat(),h.isoformat())[0]
        # The vehicle manual availability is not modified by reservation/cancellation
        assert cargar_autos()[0].disponibilidad == []
        bloqueado=Auto('BBB002','Citroen','C3','Chico','Manual',4,'Rojo',12000,'auto.png',disponibilidad=[{'desde':d.isoformat(),'hasta':h.isoformat()}])
        guardar_autos(cargar_autos()+[bloqueado]);assert not crear_reserva('cliente','BBB002',d.isoformat(),h.isoformat())[0]
        assert not calificar_reserva(rid,4,'cliente')[0]
        reservas=cargar_reservas(); reservas[0]['estado']='finalizada';guardar_json('datos/reservas.json',reservas)
        assert calificar_reserva(rid,5,'cliente')[0]
        assert not calificar_reserva(rid,4,'cliente')[0]
        assert not calificar_reserva(rid,6,'cliente')[0]
        assert cargar_reservas()[0]['puntaje']==5
        assert len(obtener_reservas_usuario('cliente'))==1
        assert not crear_reserva('cliente','AAA001','2020-02-01','2020-02-02')[0]
    fixture_workspace(go)


def test_legacy_reservation():
    def go():
        old={'reserva_id_001':{'usuario':'cliente','auto':'AAA001','fecha_inicio':'2023-02-01','fecha_fin':'2023-02-02','estado':'activa','campo_extra':'preservado'}}
        guardar_json('datos/reservas.json',old)
        lista=cargar_reservas()
        assert len(lista)==1
        r=lista[0];assert r['id_reserva']=='LEGACY-reserva_id_001' and r['patente']=='AAA001'
        assert r['campo_extra']=='preservado' and r['estado']=='finalizada'
        assert cargar_reservas()[0]['campo_extra']=='preservado'
        assert cargar_json('datos/reservas.json')[0]['campo_extra']=='preservado'
        assert not calificar_reserva('LEGACY-reserva_id_001',5,'otro')[0]
        assert calificar_reserva('LEGACY-reserva_id_001',5,'cliente')[0]
        assert cargar_json('datos/reservas.json')[0]['puntaje']==5
        assert cargar_json('datos/reservas.json')[0]['fecha_inicio']=='2023-02-01'
    fixture_workspace(go)


def test_invalid_json():
    def go():
        p=pathlib.Path('datos/autos.json');p.write_text('{not-valid}',encoding='utf-8')
        try:cargar_autos();assert False,'should raise on invalid JSON'
        except json.JSONDecodeError:pass
        assert p.read_text()=='{not-valid}'
    fixture_workspace(go)


def test_ui_imports_without_assets_or_data():
    import sys, types, importlib
    if 'tkcalendar' not in sys.modules:
        dummy=types.ModuleType('tkcalendar')
        dummy.DateEntry=type('DateEntry',(),{})
        dummy.Calendar=type('Calendar',(),{})
        sys.modules['tkcalendar']=dummy
    def go():
        modules=['interfaces.administrador.menu_admin','interfaces.cliente.menu_cliente',
        'interfaces.cliente.buscar_auto','interfaces.cliente.reservar_auto',
        'interfaces.cliente.mis_reservas','interfaces.cliente.puntuar_auto',
        'interfaces.administrador.formulario_auto','interfaces.administrador.gestionar_autos',
        'interfaces.administrador.historial_reservas','interfaces.comunes.registro_usuario',
        'interfaces.comunes.mi_cuenta','config.precarga_admin']
        for m in modules:importlib.import_module(m)
        # no import-time creation of reservations files
        assert not pathlib.Path('datos/reservas.json').exists()
    fixture_workspace(go)

if __name__=='__main__':
 for f in [test_passwords,test_old_autos,test_booking,test_legacy_reservation,test_invalid_json,test_ui_imports_without_assets_or_data]:
  try:f();print('OK',f.__name__)
  except Exception as e:
   import traceback;traceback.print_exc();print('FAIL',f.__name__);raise
