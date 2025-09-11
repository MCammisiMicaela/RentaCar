import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import json

class RegisterUser:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Usuarios")
        self.center_window(self.root, 450, 350)
        self.path = Path(__file__).parent.joinpath('users_data.json')
        self.users = {}
        self.load_data_from_json()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True)

        tk.Label(self.main_frame, text="Bienvenido al sistema").pack(pady=10)
        tk.Button(self.main_frame, text="Iniciar Sesión", width=20, command=self.login_window).pack(pady=5)
        tk.Button(self.main_frame, text="Salir", width=20, command=self.root.quit).pack(pady=5)

    def center_window(self, win, width, height):
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def save_data_to_json(self):
        try:
            with open(self.path, "w") as file:
                json.dump(self.users, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando datos: {e}")

    def load_data_from_json(self):
        if self.path.exists():
            with open(self.path, "r") as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def register_window(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Registro")
        self.center_window(reg_win, 450, 350)

        frame = tk.Frame(reg_win)
        frame.pack(expand=True)

        tk.Label(frame, text="Nickname").grid(row=0, column=0, padx=5, pady=5)
        nickname_entry = tk.Entry(frame)
        nickname_entry.grid(row=0, column=1)

        tk.Label(frame, text="Nombre").grid(row=1, column=0, padx=5, pady=5)
        fname_entry = tk.Entry(frame)
        fname_entry.grid(row=1, column=1)

        tk.Label(frame, text="Apellido").grid(row=2, column=0, padx=5, pady=5)
        lname_entry = tk.Entry(frame)
        lname_entry.grid(row=2, column=1)

        tk.Label(frame, text="Email").grid(row=3, column=0, padx=5, pady=5)
        email_entry = tk.Entry(frame)
        email_entry.grid(row=3, column=1)

        tk.Label(frame, text="Contraseña").grid(row=4, column=0, padx=5, pady=5)
        pwd_entry = tk.Entry(frame, show="*")
        pwd_entry.grid(row=4, column=1)

        def save_user():
            nick = nickname_entry.get().strip()
            if not nick or nick in self.users:
                messagebox.showerror("Error", "Nickname inválido o ya existe.")
                return

            self.users[nick] = {
                "first name": fname_entry.get(),
                "last name": lname_entry.get(),
                "email": email_entry.get(),
                "password": pwd_entry.get(),
                "role": "admin" if not self.users else "user",
                "access": True,
                "status": "offline",
                "attempts": 0,
                "reservas": []
            }
            self.save_data_to_json()
            messagebox.showinfo("Éxito", f"Usuario {nick} registrado correctamente.")
            reg_win.destroy()

        tk.Button(frame, text="Registrar", command=save_user).grid(row=5, column=0, columnspan=2, pady=10)

    def login_window(self):
        log_win = tk.Toplevel(self.root)
        log_win.title("Iniciar Sesión")
        self.center_window(log_win, 450, 350)

        frame = tk.Frame(log_win)
        frame.pack(expand=True)

        tk.Label(frame, text="Nickname").grid(row=0, column=0, padx=5, pady=5)
        nick_entry = tk.Entry(frame)
        nick_entry.grid(row=0, column=1)

        tk.Label(frame, text="Contraseña").grid(row=1, column=0, padx=5, pady=5)
        pwd_entry = tk.Entry(frame, show="*")
        pwd_entry.grid(row=1, column=1)

        def login_action():
            nick = nick_entry.get().strip()
            pwd = pwd_entry.get()

            if nick not in self.users:
                messagebox.showerror("Error", "Usuario no existe.")
                return
            if not self.users[nick]["access"]:
                messagebox.showerror("Error", "Acceso denegado.")
                return
            if self.users[nick]["password"] != pwd:
                self.users[nick]["attempts"] += 1
                self.save_data_to_json()
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return

            self.users[nick]["attempts"] = 0
            self.users[nick]["status"] = "online"
            self.save_data_to_json()

            role = self.users[nick]["role"]
            log_win.destroy()
            if role == "admin":
                self.admin_menu(nick)
            else:
                self.user_menu(nick)

        tk.Button(frame, text="Ingresar", command=login_action).grid(row=2, column=0, columnspan=2, pady=10)

        bottom_frame = tk.Frame(log_win)
        bottom_frame.pack(side="bottom", pady=10)

        tk.Label(bottom_frame, text="¿No tiene una cuenta?").pack(side="left")
        tk.Button(bottom_frame, text="Registrarse", command=self.register_window).pack(side="left", padx=5)

    def admin_menu(self, nick):
        win = tk.Toplevel(self.root)
        win.title("Menú Admin")
        self.center_window(win, 450, 350)

        frame = tk.Frame(win)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Bienvenido Admin {nick}").pack(pady=10)
        tk.Label(frame, text="Funciones administrativas aquí").pack(pady=5)

    def user_menu(self, nick):
        win = tk.Toplevel(self.root)
        win.title("Menú Usuario")
        self.center_window(win, 450, 350)

        frame = tk.Frame(win)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Bienvenido {nick}").pack(pady=10)
        tk.Button(frame, text="Mi cuenta", command=lambda: self.account_window(nick)).pack(pady=5)
        tk.Button(frame, text="Mi historial", command=lambda: self.history_window(nick)).pack(pady=5)
        tk.Button(frame, text="Buscar autos", command=lambda: self.search_cars_window(nick)).pack(pady=5)
        tk.Button(frame, text="Cerrar sesión", command=win.destroy).pack(pady=5)

    def account_window(self, nick):
        win = tk.Toplevel(self.root)
        win.title("Mi Cuenta")
        self.center_window(win, 400, 300)
        user = self.users[nick]

        frame = tk.Frame(win)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Nombre: {user.get('first name', '')}").pack()
        tk.Label(frame, text=f"Apellido: {user.get('last name', '')}").pack()
        tk.Label(frame, text=f"Email: {user.get('email', '')}").pack()
        tk.Label(frame, text=f"Nickname: {nick}").pack()

        tk.Button(frame, text="Modificar datos personales", command=lambda: self.edit_user_data(nick)).pack(pady=5)
        tk.Button(frame, text="Modificar contraseña", command=lambda: self.change_password(nick)).pack(pady=5)

    def edit_user_data(self, nick):
        win = tk.Toplevel(self.root)
        win.title("Editar Datos")
        self.center_window(win, 350, 250)
        user = self.users[nick]

        frame = tk.Frame(win)
        frame.pack(expand=True)

        fname = tk.Entry(frame)
        fname.insert(0, user.get("first name", ""))
        fname.grid(row=0, column=1)
        tk.Label(frame, text="Nombre").grid(row=0, column=0)

        lname = tk.Entry(frame)
        lname.insert(0, user.get("last name", ""))
        lname.grid(row=1, column=1)
        tk.Label(frame, text="Apellido").grid(row=1, column=0)

        email = tk.Entry

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterUser(root)
    root.mainloop()
