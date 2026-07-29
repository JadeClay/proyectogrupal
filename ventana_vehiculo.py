#
# Ventana de Gestion de Vehiculos
#
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from conexion_bd import (
    buscar_vehiculos,
    insertar_vehiculo,
    actualizar_vehiculo,
    eliminar_vehiculo,
    buscar_clientes
)


def dialogo_vehiculo(parent, titulo="Vehículo", placa="", marca="", modelo="", anio="", cliente_id=None):
    resultado = [None]

    dialogo = ctk.CTkToplevel(parent)
    dialogo.title(titulo)
    dialogo.geometry("400x450")
    dialogo.resizable(False, False)
    dialogo.grab_set()

    x = (dialogo.winfo_screenwidth() - 400) // 2
    y = (dialogo.winfo_screenheight() - 450) // 2
    dialogo.geometry(f"400x450+{x}+{y}")

    ctk.CTkLabel(dialogo, text=titulo, font=("Arial", 16, "bold")).pack(pady=(15, 10))

    frame = ctk.CTkFrame(dialogo, fg_color="transparent")
    frame.pack(fill="x", padx=30)

    ctk.CTkLabel(frame, text="Placa:").pack(anchor="w")
    entry_placa = ctk.CTkEntry(frame, width=340)
    entry_placa.pack(pady=(0, 8))
    entry_placa.insert(0, placa)

    ctk.CTkLabel(frame, text="Marca:").pack(anchor="w")
    entry_marca = ctk.CTkEntry(frame, width=340)
    entry_marca.pack(pady=(0, 8))
    entry_marca.insert(0, marca)

    ctk.CTkLabel(frame, text="Modelo:").pack(anchor="w")
    entry_modelo = ctk.CTkEntry(frame, width=340)
    entry_modelo.pack(pady=(0, 8))
    entry_modelo.insert(0, modelo)

    ctk.CTkLabel(frame, text="Año:").pack(anchor="w")
    entry_anio = ctk.CTkEntry(frame, width=340)
    entry_anio.pack(pady=(0, 8))
    entry_anio.insert(0, anio)

    clientes = buscar_clientes()
    nombres_clientes = [c[1] for c in clientes]
    mapa_clientes = {c[1]: c[0] for c in clientes}

    ctk.CTkLabel(frame, text="Cliente:").pack(anchor="w")
    combo_cliente = ctk.CTkComboBox(frame, values=nombres_clientes, width=340)
    combo_cliente.pack(pady=(0, 8))

    if cliente_id:
        for nombre, id_ in mapa_clientes.items():
            if id_ == cliente_id:
                combo_cliente.set(nombre)
                break
    elif nombres_clientes:
        combo_cliente.set(nombres_clientes[0])

    def guardar():
        nombre_seleccionado = combo_cliente.get()
        id_cliente = mapa_clientes.get(nombre_seleccionado)
        resultado[0] = (
            entry_placa.get().strip(),
            entry_marca.get().strip(),
            entry_modelo.get().strip(),
            entry_anio.get().strip(),
            id_cliente,
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

    entry_placa.focus_set()
    dialogo.wait_window()
    return resultado[0]


def cargar_vehiculos_ui(tabla, texto=""):
    """Carga los vehiculos en la tabla. Si hay texto, filtra."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    vehiculos = buscar_vehiculos(texto)
    for vehiculo in vehiculos:
        tabla.insert("", "end", values=vehiculo)


def seleccionar_vehiculo_ui(event, tabla, estado):
    """Guarda la fila seleccionada en el diccionario de estado."""
    seleccion = tabla.selection()
    if seleccion:
        estado["vehiculo_seleccionado"] = tabla.item(seleccion[0])["values"]
    else:
        estado["vehiculo_seleccionado"] = None


# Funcion para agregar un vehiculo nuevo.
# Abre el dialogo, recibe los datos, y los envia a la BD.
# Si la BD retorna un error (ej: placa duplicada), lo muestra al usuario.
def agregar_vehiculo_ui(ventana, tabla):
    # Abrir dialogo para que el usuario ingrese los datos
    resultado = dialogo_vehiculo(ventana, titulo="Agregar Vehiculo")
    if not resultado:
        return

    placa, marca, modelo, anio, cliente_id = resultado

    # Enviar a la BD - ahora retorna (id, error) en vez de solo id
    id_vehiculo, error = insertar_vehiculo(placa, marca, modelo, anio, cliente_id)

    # Si hay error de MySQL, lo mostramos al usuario
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Vehiculo agregado correctamente.", parent=ventana)
        cargar_vehiculos_ui(tabla)


# Funcion para editar un vehiculo existente.
# Abre el dialogo con los datos actuales, recibe los cambios, y los envia a la BD.
# Si la BD retorna un error (ej: placa duplicada), lo muestra al usuario.
def editar_vehiculo_ui(ventana, tabla, estado):
    # Verificar que haya un vehiculo seleccionado en la tabla
    if not estado["vehiculo_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un vehiculo para editar.", parent=ventana)
        return

    vehiculo = estado["vehiculo_seleccionado"]
    id_vehiculo = vehiculo[0]

    # Abrir dialogo con los datos actuales del vehiculo
    resultado = dialogo_vehiculo(
        ventana, titulo="Editar Vehiculo",
        placa=vehiculo[1], marca=vehiculo[2], modelo=vehiculo[3], anio=vehiculo[4], cliente_id=vehiculo[5]
    )
    if not resultado:
        return

    placa, marca, modelo, anio, cliente_id = resultado

    # Enviar a la BD - ahora retorna (ok, error) en vez de solo True/False
    ok, error = actualizar_vehiculo(id_vehiculo, placa, marca, modelo, anio, cliente_id)

    # Si hay error de MySQL, lo mostramos al usuario
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Vehiculo actualizado correctamente.", parent=ventana)
        cargar_vehiculos_ui(tabla)


# Funcion para eliminar (desactivar) un vehiculo.
# Pide confirmacion al usuario, y si acepta, ejecuta el soft delete en la BD.
def eliminar_vehiculo_ui(ventana, tabla, estado):
    # Verificar que haya un vehiculo seleccionado en la tabla
    if not estado["vehiculo_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un vehiculo para eliminar.", parent=ventana)
        return

    vehiculo = estado["vehiculo_seleccionado"]

    # Pedir confirmacion antes de eliminar
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de eliminar al vehiculo '{vehiculo[1]}'?",
        parent=ventana,
    )
    if not respuesta:
        return

    # Ejecutar el soft delete - ahora retorna (ok, error)
    ok, error = eliminar_vehiculo(vehiculo[0])

    # Si hay error de MySQL, lo mostramos al usuario
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Vehiculo eliminado correctamente.", parent=ventana)
        estado["vehiculo_seleccionado"] = None
        cargar_vehiculos_ui(tabla)

def volver_al_menu(ventana):
    ventana.master.deiconify()
    ventana.destroy()

# FUNCION PRINCIPAL
def mostrar_ventana_vehiculos(ventana):
    """Muestra la pantalla de gestión de vehiculos."""
    estado = {"vehiculo_seleccionado": None}

    # --- Configurar ventana ---
    ventana.title("Gestión de Vehículos")
    ventana.geometry("800x550")
    ventana.resizable(False, False)
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 800) // 2
    y = (ventana.winfo_screenheight() - 550) // 2
    ventana.geometry(f"800x550+{x}+{y}")

    # --- Título ---
    ctk.CTkLabel(
        ventana, text="Gestión de Vehículos", font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    # --- Barra de búsqueda ---
    frame_busqueda = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_busqueda.pack(fill="x", padx=20, pady=(0, 5))

    ctk.CTkLabel(frame_busqueda, text="Buscar:").pack(side="left", padx=(0, 5))
    entrada_busqueda = ctk.CTkEntry(frame_busqueda, width=300, placeholder_text="Placa, marca o modelo...")
    entrada_busqueda.pack(side="left", fill="x", expand=True)

    def on_busqueda(event=None):
        cargar_vehiculos_ui(tabla, entrada_busqueda.get().strip())

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
        columns=("id", "placa", "marca", "modelo", "anio"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
    )

    tabla.heading("id", text="ID")
    tabla.column("id", width=50, anchor="center")
    tabla.heading("placa", text="Placa")
    tabla.column("placa", width=100, anchor="center")
    tabla.heading("marca", text="Marca")
    tabla.column("marca", width=150)
    tabla.heading("modelo", text="Modelo")
    tabla.column("modelo", width=150)
    tabla.heading("anio", text="Año")
    tabla.column("anio", width=80, anchor="center")

    tabla.pack(fill="both", expand=True)
    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    # Esto hace que al seleccionar algo en la lista se llame la funcion seleccionar vehiculo
    tabla.bind("<<TreeviewSelect>>", lambda e: seleccionar_vehiculo_ui(e, tabla, estado)) 
    # Esto hace que al darle doble click se edite el vehiculo
    tabla.bind("<Double-1>", lambda e: editar_vehiculo_ui(ventana, tabla, estado))

    # --- Crear botones ---
    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.pack(pady=15)

    ctk.CTkButton(
        frame_botones, text="Agregar", width=120, fg_color="#4CAF50", hover_color="#45a049",
        command=lambda: agregar_vehiculo_ui(ventana, tabla),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Editar", width=120, fg_color="#2196F3", hover_color="#1976D2",
        command=lambda: editar_vehiculo_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Eliminar", width=120, fg_color="#f44336", hover_color="#da190b",
        command=lambda: eliminar_vehiculo_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Volver", width=120, fg_color="#9E9E9E", hover_color="#757575",
        command=lambda: volver_al_menu(ventana),
    ).pack(side="left", padx=5)

    # --- Cargar datos iniciales ---
    cargar_vehiculos_ui(tabla)