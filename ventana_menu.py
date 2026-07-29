# Menú principal del sistema.
# Desde aquí se accede a todas las demás pantallas.
#
# PARA AGREGAR UNA NUEVA PANTALLA:
#   1) Creá un archivo "ventana_ejemplo.py" con una función
#      mostrar_ejemplo(ventana)
#   2) Importá esa función acá
#   3) Agregá un botón que la abra
# ============================================================

import customtkinter as ctk
from tkinter import messagebox

# VENTANAS
from ventana_clientes import mostrar_ventana_clientes
from ventana_vehiculo import mostrar_ventana_vehiculos
from ventana_servicios import mostrar_ventana_servicios
from ventana_usuario import mostrar_ventana_usuario


def abrir_pantalla(master, estado, funcion_pantalla):
    """
    Abre una ventana nueva (Toplevel) y ejecuta la función
    que dibuja esa pantalla.
    """
    if estado["ventana_actual"] is not None:
        if estado["ventana_actual"].winfo_exists():
            messagebox.showinfo(
                "Ventana abierta",
                "Ya hay una ventana abierta. Termine de usarla primero."
            )
            return

    nueva_ventana = ctk.CTkToplevel(master)
    estado["ventana_actual"] = nueva_ventana
    master.withdraw()

    funcion_pantalla(nueva_ventana)

    nueva_ventana.protocol(
        "WM_DELETE_WINDOW",
        lambda: cerrar_pantalla(nueva_ventana, estado, master)
    )


def cerrar_pantalla(ventana, estado, master):
    """Cierra la ventana actual y limpia el registro."""
    ventana.destroy()
    estado["ventana_actual"] = None
    master.deiconify()


def cerrar_sesion(master, callback_cerrar_sesion):
    """Pregunta si quiere cerrar sesion y vuelve al login."""
    respuesta = messagebox.askyesno(
        "Cerrar Sesión",
        "¿Está seguro que desea cerrar sesión?"
    )

    if respuesta:
        callback_cerrar_sesion()


def salir_sistema(master):
    """Cierra todo el programa."""
    respuesta = messagebox.askyesno(
        "Salir del Sistema",
        "¿Está seguro que desea salir del sistema?"
    )

    if respuesta:
        master.quit()


def mostrar_menu(master, id_usuario, nombre_usuario, email_usuario,
                 callback_cerrar_sesion):
    """
    Dibuja el menú principal.
    """
    estado = {"ventana_actual": None}

    master.geometry("500x500")
    master.resizable(False, False)
    master.update_idletasks()

    x = (master.winfo_screenwidth() - 500) // 2
    y = (master.winfo_screenheight() - 500) // 2
    master.geometry(f"500x500+{x}+{y}")

    # --- Título ---
    ctk.CTkLabel(
        master,
        text="MENÚ PRINCIPAL",
        font=("Arial", 24, "bold")
    ).pack(pady=(20, 5))

    # --- Info del usuario ---
    frame_info = ctk.CTkFrame(master, fg_color="transparent")
    frame_info.pack(pady=5)

    ctk.CTkLabel(
        frame_info,
        text=f"Usuario: {nombre_usuario}",
        font=("Arial", 12),
        text_color="#aaaaaa"
    ).pack()

    ctk.CTkLabel(
        frame_info,
        text=f"Email: {email_usuario}",
        font=("Arial", 12),
        text_color="#aaaaaa"
    ).pack()

    # --- Separador ---
    ctk.CTkFrame(
        master,
        height=2,
        fg_color="#555555"
    ).pack(fill="x", padx=30, pady=15)

    # --- Botones del menú ---
    frame_botones = ctk.CTkFrame(master, fg_color="transparent")
    frame_botones.pack(expand=True)

    ctk.CTkButton(
        frame_botones,
        text="Gestión de Clientes",
        font=("Arial", 14, "bold"),
        width=280,
        height=50,
        fg_color="#4CAF50",
        hover_color="#45a049",
        command=lambda: abrir_pantalla(master, estado, mostrar_ventana_clientes),
    ).pack(pady=8)

    ctk.CTkButton(
        frame_botones,
        text="Gestión de Vehículos",
        font=("Arial", 14, "bold"),
        width=280,
        height=50,
        fg_color="#1E1096",
        hover_color="#110456",
        command=lambda: abrir_pantalla(master, estado, mostrar_ventana_vehiculos),
    ).pack(pady=8)

    ctk.CTkButton(
        frame_botones,
        text="Gestión de Servicios",
        font=("Arial", 14, "bold"),
        width=280,
        height=50,
        fg_color="#FF9800",
        hover_color="#E68900",
        command=lambda: abrir_pantalla(master, estado, mostrar_ventana_servicios),
    ).pack(pady=8)

    ctk.CTkButton(
        frame_botones,
        text="Gestión de Usuarios",
        font=("Arial", 14, "bold"),
        width=280,
        height=50,
        fg_color="#E91E63",
        hover_color="#C2185B",
        command=lambda: abrir_pantalla(master, estado, mostrar_ventana_usuario),
    ).pack(pady=8)

    # --- Botones de sesión (abajo) ---
    ctk.CTkButton(
        master,
        text="Cerrar Sesión",
        font=("Arial", 12, "bold"),
        width=200,
        fg_color="#9E9E9E",
        hover_color="#757575",
        command=lambda: cerrar_sesion(master, callback_cerrar_sesion)
    ).pack(side="bottom", pady=(0, 10))

    ctk.CTkButton(
        master,
        text="Salir del Sistema",
        font=("Arial", 12, "bold"),
        width=200,
        fg_color="#f44336",
        hover_color="#da190b",
        command=lambda: salir_sistema(master)
    ).pack(side="bottom", pady=15)
