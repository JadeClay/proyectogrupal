# ============================================================
# ventana_login.py
# ============================================================
# Pantalla de login.
# El usuario ingresa email y contraseña.
# Si los datos son correctos, se llama al callback de éxito.
# ============================================================

import customtkinter as ctk
from tkinter import messagebox
from conexion_bd import buscar_usuario

# FUNCION PARA LOGUEARSE
def intentar_ingresar(txt_email, txt_password, callback_ok):
    """
    Toma los datos de los campos y verifica si son correctos.
    Si son correctos, llama a callback_ok(id, nombre, email).
    """
    email = txt_email.get().strip()
    password = txt_password.get().strip()

    # Validar que no estén vacíos
    if not email or not password:
        messagebox.showwarning(
            "Campos vacíos",
            "Por favor complete todos los campos."
        )
        return

    # Buscar el usuario en la base de datos
    usuario = buscar_usuario(email, password)

    if usuario:
        messagebox.showinfo(
            "Bienvenido",
            f"Hola {usuario[1]}! Has iniciado sesión correctamente."
        )
        callback_ok(usuario[0], usuario[1], email)
    else:
        messagebox.showerror(
            "Error de inicio de sesión",
            "Email o contraseña incorrectos.\n"
            "Verifique los datos e intente nuevamente."
        )


def mostrar_login(master, callback_ok):
    """
    Dibuja la pantalla de login dentro de la ventana master.
    Cuando el login es exitoso, llama a callback_ok(id, nombre, email).
    """
    master.geometry("400x300")
    master.resizable(False, False)
    master.update_idletasks
    x = (master.winfo_screenwidth() - 400) // 2
    y = (master.winfo_screenheight() - 300) // 2
    master.geometry(f"{400}x{300}+{x}+{y}")

    # --- Título ---
    ctk.CTkLabel(
        master,
        text="Iniciar Sesión",
        font=("Arial", 22, "bold")
    ).pack(pady=(20, 10))

    # --- Formulario ---
    frame_form = ctk.CTkFrame(master, fg_color="transparent")
    frame_form.pack(fill="both", expand=True, padx=30)

    # Campo email
    ctk.CTkLabel(frame_form, text="Email:", anchor="w").pack(
        fill="x", pady=(5, 0)
    )

    txt_email = ctk.CTkEntry(
        frame_form,
        placeholder_text="ejemplo@correo.com"
    )
    txt_email.pack(fill="x", pady=(0, 10))
    txt_email.insert(0, "admin@test.com")

    # Campo contraseña
    ctk.CTkLabel(frame_form, text="Contraseña:", anchor="w").pack(
        fill="x", pady=(5, 0)
    )

    txt_password = ctk.CTkEntry(
        frame_form,
        show="*",
        placeholder_text="Su contraseña"
    )
    txt_password.pack(fill="x", pady=(0, 10))
    txt_password.insert(0, "1234")

    # --- Botones ---
    frame_botones = ctk.CTkFrame(master, fg_color="transparent")
    frame_botones.pack(pady=10)

    ctk.CTkButton(
        frame_botones,
        text="Ingresar",
        width=120,
        fg_color="#4CAF50",
        hover_color="#45a049",
        command=lambda: intentar_ingresar(txt_email, txt_password, callback_ok)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        frame_botones,
        text="Salir",
        width=120,
        fg_color="#f44336",
        hover_color="#da190b",
        command=master.destroy
    ).pack(side="left", padx=5)

    # Permitir ingresar con la tecla Enter
    master.bind(
        "<Return>",
        lambda e: intentar_ingresar(txt_email, txt_password, callback_ok)
    )
