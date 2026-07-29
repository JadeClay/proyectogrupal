#
# Ventana de Gestion de Usuarios
#
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from conexion_bd import (
    buscar_usuarios,
    insertar_usuario,
    actualizar_usuario,
    eliminar_usuario,
)


def dialogo_usuario(parent, titulo="Usuario", nombre="", email="", password=""):
    resultado = [None]

    dialogo = ctk.CTkToplevel(parent)
    dialogo.title(titulo)
    dialogo.geometry("400x300")
    dialogo.resizable(False, False)
    dialogo.grab_set()

    x = (dialogo.winfo_screenwidth() - 400) // 2
    y = (dialogo.winfo_screenheight() - 300) // 2
    dialogo.geometry(f"400x300+{x}+{y}")

    ctk.CTkLabel(dialogo, text=titulo, font=("Arial", 16, "bold")).pack(pady=(15, 10))

    frame = ctk.CTkFrame(dialogo, fg_color="transparent")
    frame.pack(fill="x", padx=30)

    ctk.CTkLabel(frame, text="Nombre:").pack(anchor="w")
    entry_nombre = ctk.CTkEntry(frame, width=340)
    entry_nombre.pack(pady=(0, 8))
    entry_nombre.insert(0, nombre)

    ctk.CTkLabel(frame, text="Email:").pack(anchor="w")
    entry_email = ctk.CTkEntry(frame, width=340)
    entry_email.pack(pady=(0, 8))
    entry_email.insert(0, email)

    ctk.CTkLabel(frame, text="Contraseña:").pack(anchor="w")
    entry_password = ctk.CTkEntry(frame, width=340)
    entry_password.pack(pady=(0, 8))
    entry_password.insert(0, password)

    def guardar():
        resultado[0] = (
            entry_nombre.get().strip(),
            entry_email.get().strip(),
            entry_password.get().strip(),
        )
        dialogo.destroy()

    def cancelar():
        dialogo.destroy()

    frame_botones = ctk.CTkFrame(dialogo, fg_color="transparent")
    frame_botones.pack(pady=15)

    ctk.CTkButton(
        frame_botones, text="Guardar", width=140, fg_color="#4CAF50",
        hover_color="#45a049", command=guardar,
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Cancelar", width=140, fg_color="#9E9E9E",
        hover_color="#757575", command=cancelar,
    ).pack(side="left", padx=5)

    entry_nombre.focus_set()
    dialogo.wait_window()
    return resultado[0]


def cargar_usuarios_ui(tabla, texto=""):
    """Carga los usuarios en la tabla. Si hay texto, filtra."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    usuarios = buscar_usuarios(texto)
    for usuario in usuarios:
        tabla.insert("", "end", values=usuario)


def seleccionar_usuario_ui(event, tabla, estado):
    """Guarda la fila seleccionada en el diccionario de estado."""
    seleccion = tabla.selection()
    if seleccion:
        estado["usuario_seleccionado"] = tabla.item(seleccion[0])["values"]
    else:
        estado["usuario_seleccionado"] = None


def agregar_usuario_ui(ventana, tabla):
    resultado = dialogo_usuario(ventana, titulo="Agregar Usuario")
    if not resultado:
        return

    nombre, email, password = resultado

    id_usuario, error = insertar_usuario(nombre, email, password)
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Usuario agregado correctamente.", parent=ventana)
        cargar_usuarios_ui(tabla)


def editar_usuario_ui(ventana, tabla, estado):
    if not estado["usuario_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un usuario para editar.", parent=ventana)
        return

    usuario = estado["usuario_seleccionado"]
    id_usuario = usuario[0]

    resultado = dialogo_usuario(
        ventana, titulo="Editar Usuario",
        nombre=usuario[1], email=usuario[2], password=usuario[3],
    )
    if not resultado:
        return

    nombre, email, password = resultado

    ok, error = actualizar_usuario(id_usuario, nombre, email, password)
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente.", parent=ventana)
        cargar_usuarios_ui(tabla)


def eliminar_usuario_ui(ventana, tabla, estado):
    if not estado["usuario_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un usuario para eliminar.", parent=ventana)
        return

    usuario = estado["usuario_seleccionado"]
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de eliminar al usuario '{usuario[1]}'?",
        parent=ventana,
    )
    if not respuesta:
        return

    ok, error = eliminar_usuario(usuario[0])
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.", parent=ventana)
        estado["usuario_seleccionado"] = None
        cargar_usuarios_ui(tabla)


def volver_al_menu(ventana):
    ventana.master.deiconify()
    ventana.destroy()


# FUNCION PRINCIPAL
def mostrar_ventana_usuario(ventana):
    """Muestra la pantalla de gestión de usuarios."""
    estado = {"usuario_seleccionado": None}

    # --- Configurar ventana ---
    ventana.title("Gestión de Usuarios")
    ventana.geometry("800x550")
    ventana.resizable(False, False)
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 800) // 2
    y = (ventana.winfo_screenheight() - 550) // 2
    ventana.geometry(f"800x550+{x}+{y}")

    # --- Título ---
    ctk.CTkLabel(
        ventana, text="Gestión de Usuarios", font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    # --- Barra de búsqueda ---
    frame_busqueda = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_busqueda.pack(fill="x", padx=20, pady=(0, 5))

    ctk.CTkLabel(frame_busqueda, text="Buscar:").pack(side="left", padx=(0, 5))
    entrada_busqueda = ctk.CTkEntry(frame_busqueda, width=300, placeholder_text="Nombre o email...")
    entrada_busqueda.pack(side="left", fill="x", expand=True)

    def on_busqueda(event=None):
        cargar_usuarios_ui(tabla, entrada_busqueda.get().strip())

    entrada_busqueda.bind("<KeyRelease>", on_busqueda)

    # --- Crear tabla ---
    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "nombre", "email", "password"),
        show="headings",
        yscrollcommand=scroll_y.set,
    )

    tabla.heading("id", text="ID")
    tabla.column("id", width=50, anchor="center")
    tabla.heading("nombre", text="Nombre")
    tabla.column("nombre", width=200)
    tabla.heading("email", text="Email")
    tabla.column("email", width=250)
    tabla.heading("password", text="Contraseña")
    tabla.column("password", width=150, anchor="center")

    tabla.pack(fill="both", expand=True)
    scroll_y.config(command=tabla.yview)

    tabla.bind("<<TreeviewSelect>>", lambda e: seleccionar_usuario_ui(e, tabla, estado))
    tabla.bind("<Double-1>", lambda e: editar_usuario_ui(ventana, tabla, estado))

    # --- Crear botones ---
    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.pack(pady=15)

    ctk.CTkButton(
        frame_botones, text="Agregar", width=120, fg_color="#4CAF50", hover_color="#45a049",
        command=lambda: agregar_usuario_ui(ventana, tabla),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Editar", width=120, fg_color="#2196F3", hover_color="#1976D2",
        command=lambda: editar_usuario_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Eliminar", width=120, fg_color="#f44336", hover_color="#da190b",
        command=lambda: eliminar_usuario_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Volver", width=120, fg_color="#9E9E9E", hover_color="#757575",
        command=lambda: volver_al_menu(ventana),
    ).pack(side="left", padx=5)

    # --- Cargar datos iniciales ---
    cargar_usuarios_ui(tabla)
