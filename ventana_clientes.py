import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from conexion_bd import (
    buscar_clientes,
    insertar_cliente,
    actualizar_cliente,
    eliminar_cliente,
)

def dialogo_cliente(parent, titulo="Cliente", nombre="", email="", telefono=""):
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

    ctk.CTkLabel(frame, text="Teléfono:").pack(anchor="w")
    entry_telefono = ctk.CTkEntry(frame, width=340)
    entry_telefono.pack(pady=(0, 8))
    entry_telefono.insert(0, telefono)

    def guardar():
        resultado[0] = (
            entry_nombre.get().strip(),
            entry_email.get().strip(),
            entry_telefono.get().strip(),
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


def cargar_clientes_ui(tabla, texto=""):
    """Carga los clientes en la tabla. Si hay texto, filtra."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    clientes = buscar_clientes(texto)
    for cliente in clientes:
        tabla.insert("", "end", values=cliente)


def seleccionar_cliente_ui(event, tabla, estado):
    """Guarda la fila seleccionada en el diccionario de estado."""
    seleccion = tabla.selection()
    if seleccion:
        estado["cliente_seleccionado"] = tabla.item(seleccion[0])["values"]
    else:
        estado["cliente_seleccionado"] = None


# Funcion para agregar un cliente nuevo.
# Abre el dialogo, recibe los datos, y los envia a la BD.
# Si la BD retorna un error (ej: email duplicado), lo muestra al usuario.
def agregar_cliente_ui(ventana, tabla):
    # Abrir dialogo para que el usuario ingrese los datos
    resultado = dialogo_cliente(ventana, titulo="Agregar Cliente")
    if not resultado:
        return

    nombre, email, telefono = resultado

    # Enviar a la BD - ahora retorna (id, error) en vez de solo id
    id_cliente, error = insertar_cliente(nombre, email, telefono)

    # Si hay error de MySQL, lo mostramos al usuario
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Cliente agregado correctamente.", parent=ventana)
        cargar_clientes_ui(tabla)


# Funcion para editar un cliente existente.
# Abre el dialogo con los datos actuales, recibe los cambios, y los envia a la BD.
# Si la BD retorna un error (ej: email duplicado), lo muestra al usuario.
def editar_cliente_ui(ventana, tabla, estado):
    # Verificar que haya un cliente seleccionado en la tabla
    if not estado["cliente_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un cliente para editar.", parent=ventana)
        return

    cliente = estado["cliente_seleccionado"]
    id_cliente = cliente[0]

    # Abrir dialogo con los datos actuales del cliente
    resultado = dialogo_cliente(
        ventana, titulo="Editar Cliente",
        nombre=cliente[1], email=cliente[2], telefono=cliente[3],
    )
    if not resultado:
        return

    nombre, email, telefono = resultado

    # Enviar a la BD - ahora retorna (ok, error) en vez de solo True/False
    ok, error = actualizar_cliente(id_cliente, nombre, email, telefono)

    # Si hay error de MySQL, lo mostramos al usuario
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.", parent=ventana)
        cargar_clientes_ui(tabla)


# Funcion para eliminar (desactivar) un cliente.
# Pide confirmacion al usuario, y si acepta, ejecuta el soft delete en la BD.
def eliminar_cliente_ui(ventana, tabla, estado):
    # Verificar que haya un cliente seleccionado en la tabla
    if not estado["cliente_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un cliente para eliminar.", parent=ventana)
        return

    cliente = estado["cliente_seleccionado"]

    # Pedir confirmacion antes de eliminar
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de eliminar al cliente '{cliente[1]}'?",
        parent=ventana,
    )
    if not respuesta:
        return

    # Ejecutar el soft delete - ahora retorna (ok, error)
    ok, error = eliminar_cliente(cliente[0])

    # Si hay error de MySQL, lo mostramos al usuario
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.", parent=ventana)
        estado["cliente_seleccionado"] = None
        cargar_clientes_ui(tabla)

def volver_al_menu(ventana):
    ventana.master.deiconify()
    ventana.destroy()

# FUNCION PRINCIPAL
def mostrar_ventana_clientes(ventana):
    """Muestra la pantalla de gestión de clientes."""
    estado = {"cliente_seleccionado": None}

    # --- Configurar ventana ---
    ventana.title("Gestión de Clientes")
    ventana.geometry("800x550")
    ventana.resizable(False, False)
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 800) // 2
    y = (ventana.winfo_screenheight() - 550) // 2
    ventana.geometry(f"800x550+{x}+{y}")

    # --- Título ---
    ctk.CTkLabel(
        ventana, text="Gestión de Clientes", font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    # --- Barra de búsqueda ---
    frame_busqueda = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_busqueda.pack(fill="x", padx=20, pady=(0, 5))

    ctk.CTkLabel(frame_busqueda, text="Buscar:").pack(side="left", padx=(0, 5))
    entrada_busqueda = ctk.CTkEntry(frame_busqueda, width=300, placeholder_text="Nombre, email o teléfono...")
    entrada_busqueda.pack(side="left", fill="x", expand=True)

    def on_busqueda(event=None):
        cargar_clientes_ui(tabla, entrada_busqueda.get().strip())

    entrada_busqueda.bind("<KeyRelease>", on_busqueda)

    # --- Crear tabla ---
    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "nombre", "email", "telefono"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
    )

    tabla.heading("id", text="ID")
    tabla.column("id", width=50, anchor="center")
    tabla.heading("nombre", text="Nombre")
    tabla.column("nombre", width=250)
    tabla.heading("email", text="Email")
    tabla.column("email", width=250)
    tabla.heading("telefono", text="Teléfono")
    tabla.column("telefono", width=150, anchor="center")

    tabla.pack(fill="both", expand=True)
    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    # Esto hace que al seleccionar algo en la lista se llame la funcion seleccionar cliente
    tabla.bind("<<TreeviewSelect>>", lambda e: seleccionar_cliente_ui(e, tabla, estado)) 
    # Esto hace que al darle doble click se edite el cliente
    tabla.bind("<Double-1>", lambda e: editar_cliente_ui(ventana, tabla, estado))

    # --- Crear botones ---
    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.pack(pady=15)

    ctk.CTkButton(
        frame_botones, text="Agregar", width=120, fg_color="#4CAF50", hover_color="#45a049",
        command=lambda: agregar_cliente_ui(ventana, tabla),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Editar", width=120, fg_color="#2196F3", hover_color="#1976D2",
        command=lambda: editar_cliente_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Eliminar", width=120, fg_color="#f44336", hover_color="#da190b",
        command=lambda: eliminar_cliente_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Volver", width=120, fg_color="#9E9E9E", hover_color="#757575",
        command=lambda: volver_al_menu(ventana),
    ).pack(side="left", padx=5)

    # --- Cargar datos iniciales ---
    cargar_clientes_ui(tabla)
