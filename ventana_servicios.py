#
# Ventana de Gestion de Servicios
#
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from conexion_bd import (
    buscar_servicios,
    insertar_servicio,
    actualizar_servicio,
    eliminar_servicio,
    buscar_vehiculos,
    buscar_clientes,
    buscar_datos_factura,
)
from fpdf import FPDF
from tkinter import filedialog
import os

def crear_pdf_factura(datos, ruta, ventana):
    (serv_id, fecha, costo, descripcion, estado_serv,
     placa, marca, modelo, anio, cliente_nombre, cliente_email, cliente_telefono) = datos

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, "FACTURA", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Servicio #{serv_id}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # Linea separadora
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # --- Datos del cliente ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "CLIENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Nombre:   {cliente_nombre}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Email:    {cliente_email}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Telefono: {cliente_telefono}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # --- Datos del vehiculo ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "VEHICULO", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Placa:   {placa}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Marca:   {marca}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Modelo:  {modelo}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Anio:    {anio}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # --- Detalle del servicio ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "DETALLE DEL SERVICIO", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Fecha:       {fecha}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Descripcion: {descripcion}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Estado:      {estado_serv}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    
    # Linea separadora
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # --- Subtotal ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"SUBTOTAL:  ${costo}", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.cell(0, 10, f"ITBIS (18%):  ${(costo*18)/100:.2f}", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.cell(0, 10, f"TOTAL A PAGAR:  ${costo + (costo*18)/100:.2f}", new_x="LMARGIN", new_y="NEXT", align="R")
    
    
    pdf.output(ruta)
    messagebox.showinfo("Factura generada", f"Factura guardada en:\n{ruta}", parent=ventana)
    os.startfile(ruta)

def dialogo_servicio(parent, titulo="Servicio", fecha="", costo="", descripcion="", estado="Pendiente", vehiculo_id=None):
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

    vehiculos = buscar_vehiculos()
    clientes = buscar_clientes()
    mapa_clientes = {c[0]: c[1] for c in clientes}

    opciones = [] # array con las opciones del combobox (guarda los textos)
    mapa_vehiculos = {} # Diccionario que relaciona el texto de la opcion con el ID
    for v in vehiculos:
        id_v, placa, marca, modelo, anio, id_cliente = v
        nombre_cliente = mapa_clientes.get(id_cliente, "Sin dueño")
        texto = f"{placa} - {marca} {modelo} ({nombre_cliente})"
        opciones.append(texto)
        mapa_vehiculos[texto] = id_v

    ctk.CTkLabel(frame, text="Vehiculo:").pack(anchor="w")
    combo_vehiculo = ctk.CTkComboBox(frame, values=opciones, width=340)
    combo_vehiculo.pack(pady=(0, 8))

    if vehiculo_id:
        for texto, id_ in mapa_vehiculos.items():
            if id_ == vehiculo_id:
                combo_vehiculo.set(texto)
                break
    elif opciones:
        combo_vehiculo.set(opciones[0])

    ctk.CTkLabel(frame, text="Fecha (YYYY-MM-DD):").pack(anchor="w")
    entry_fecha = ctk.CTkEntry(frame, width=340)
    entry_fecha.pack(pady=(0, 8))
    entry_fecha.insert(0, fecha)

    ctk.CTkLabel(frame, text="Costo:").pack(anchor="w")
    entry_costo = ctk.CTkEntry(frame, width=340)
    entry_costo.pack(pady=(0, 8))
    entry_costo.insert(0, costo)

    ctk.CTkLabel(frame, text="Descripcion:").pack(anchor="w")
    entry_descripcion = ctk.CTkEntry(frame, width=340)
    entry_descripcion.pack(pady=(0, 8))
    entry_descripcion.insert(0, descripcion)

    ctk.CTkLabel(frame, text="Estado:").pack(anchor="w")
    combo_estado = ctk.CTkComboBox(frame, values=["Pendiente", "Completado"], width=340)
    combo_estado.pack(pady=(0, 8))
    combo_estado.set(estado)

    def guardar():
        texto_seleccionado = combo_vehiculo.get()
        id_vehiculo = mapa_vehiculos.get(texto_seleccionado)
        resultado[0] = (
            id_vehiculo,
            entry_fecha.get().strip(),
            entry_costo.get().strip(),
            entry_descripcion.get().strip(),
            combo_estado.get(),
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

    entry_fecha.focus_set()
    dialogo.wait_window()
    return resultado[0]


def cargar_servicios_ui(tabla, texto=""):
    """Carga los servicios en la tabla. Si hay texto, filtra."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    servicios = buscar_servicios(texto)
    for servicio in servicios:
        tabla.insert("", "end", values=servicio)


def seleccionar_servicio_ui(event, tabla, estado):
    """Guarda la fila seleccionada en el diccionario de estado."""
    seleccion = tabla.selection()
    if seleccion:
        estado["servicio_seleccionado"] = tabla.item(seleccion[0])["values"]
    else:
        estado["servicio_seleccionado"] = None


def agregar_servicio_ui(ventana, tabla):
    resultado = dialogo_servicio(ventana, titulo="Agregar Servicio")
    if not resultado:
        return

    id_vehiculo, fecha, costo, descripcion, estado = resultado

    # La BD valida los campos obligatorios y muestra el error si lo hay
    id_servicio, error = insertar_servicio(id_vehiculo, fecha, costo, descripcion, estado)
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Servicio agregado correctamente.", parent=ventana)
        cargar_servicios_ui(tabla)


def editar_servicio_ui(ventana, tabla, estado):
    if not estado["servicio_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un servicio para editar.", parent=ventana)
        return

    servicio = estado["servicio_seleccionado"]
    id_servicio = servicio[0]

    resultado = dialogo_servicio(
        ventana, titulo="Editar Servicio",
        fecha=str(servicio[2]), costo=str(servicio[3]),
        descripcion=servicio[4], estado=servicio[5],
        vehiculo_id=servicio[6]
    )
    if not resultado:
        return

    id_vehiculo, fecha, costo, descripcion, estado_nuevo = resultado

    # La BD valida los campos y muestra el error si lo hay
    ok, error = actualizar_servicio(id_servicio, fecha, costo, descripcion, estado_nuevo)
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Servicio actualizado correctamente.", parent=ventana)
        cargar_servicios_ui(tabla)


def eliminar_servicio_ui(ventana, tabla, estado):
    if not estado["servicio_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un servicio para eliminar.", parent=ventana)
        return

    servicio = estado["servicio_seleccionado"]
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de eliminar el servicio del vehiculo '{servicio[1]}'?",
        parent=ventana,
    )
    if not respuesta:
        return

    ok, error = eliminar_servicio(servicio[0])
    if error:
        messagebox.showerror("Error de base de datos", error, parent=ventana)
    else:
        messagebox.showinfo("Éxito", "Servicio eliminado correctamente.", parent=ventana)
        estado["servicio_seleccionado"] = None
        cargar_servicios_ui(tabla)


def generar_factura_ui(ventana, estado):
    if not estado["servicio_seleccionado"]:
        messagebox.showwarning("Atención", "Seleccione un servicio para generar la factura.", parent=ventana)
        return

    servicio = estado["servicio_seleccionado"]
    id_servicio = servicio[0]

    datos = buscar_datos_factura(id_servicio)
    if not datos:
        messagebox.showerror("Error", "No se pudieron obtener los datos del servicio.", parent=ventana)
        return

    (serv_id, fecha, costo, descripcion, estado_serv,
     placa, marca, modelo, anio,
     cliente_nombre, cliente_email, cliente_telefono) = datos

    ruta = filedialog.asksaveasfilename(
        title="Guardar Factura",
        defaultextension=".pdf",
        filetypes=[("Archivo PDF", "*.pdf")],
        initialfile=f"factura_servicio_{serv_id}.pdf",
        parent=ventana,
    )
    if not ruta:
        return

    crear_pdf_factura(datos, ruta, ventana)
    

def volver_al_menu(ventana):
    ventana.master.deiconify()
    ventana.destroy()

# FUNCION PRINCIPAL
def mostrar_ventana_servicios(ventana):
    """Muestra la pantalla de gestión de servicios."""
    estado = {"servicio_seleccionado": None}

    # --- Configurar ventana ---
    ventana.title("Gestión de Servicios")
    ventana.geometry("800x550")
    ventana.resizable(False, False)
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 800) // 2
    y = (ventana.winfo_screenheight() - 550) // 2
    ventana.geometry(f"800x550+{x}+{y}")

    # --- Título ---
    ctk.CTkLabel(
        ventana, text="Gestión de Servicios", font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    # --- Barra de búsqueda ---
    frame_busqueda = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_busqueda.pack(fill="x", padx=20, pady=(0, 5))

    ctk.CTkLabel(frame_busqueda, text="Buscar:").pack(side="left", padx=(0, 5))
    entrada_busqueda = ctk.CTkEntry(frame_busqueda, width=300, placeholder_text="Placa o descripción...")
    entrada_busqueda.pack(side="left", fill="x", expand=True)

    def on_busqueda(event=None):
        cargar_servicios_ui(tabla, entrada_busqueda.get().strip())

    entrada_busqueda.bind("<KeyRelease>", on_busqueda)

    # --- Crear tabla ---
    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")
    #scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    #scroll_x.pack(side="bottom", fill="x")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "placa", "fecha", "costo", "descripcion", "estado", "id_vehiculo"),
        show="headings",
        yscrollcommand=scroll_y.set,
        #xscrollcommand=scroll_x.set,
    )

    tabla.heading("id", text="ID")
    tabla.column("id", width=50, anchor="center")
    tabla.heading("placa", text="Placa")
    tabla.column("placa", width=100, anchor="center")
    tabla.heading("fecha", text="Fecha")
    tabla.column("fecha", width=100, anchor="center")
    tabla.heading("costo", text="Costo")
    tabla.column("costo", width=80, anchor="center")
    tabla.heading("descripcion", text="Descripcion")
    tabla.column("descripcion", width=200)
    tabla.heading("estado", text="Estado")
    tabla.column("estado", width=100, anchor="center")
    tabla.heading("id_vehiculo", text="ID Vehiculo")
    tabla.column("id_vehiculo", width=0, stretch=False)

    tabla.pack(fill="both", expand=True)
    scroll_y.config(command=tabla.yview)
    #scroll_x.config(command=tabla.xview)

    # Ocultar columna id_vehiculo (solo se usa internamente)
    tabla.column("id_vehiculo", width=0, minwidth=0)

    tabla.bind("<<TreeviewSelect>>", lambda e: seleccionar_servicio_ui(e, tabla, estado))
    tabla.bind("<Double-1>", lambda e: editar_servicio_ui(ventana, tabla, estado))

    # --- Crear botones ---
    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.pack(pady=15)

    ctk.CTkButton(
        frame_botones, text="Agregar", width=120, fg_color="#4CAF50", hover_color="#45a049",
        command=lambda: agregar_servicio_ui(ventana, tabla),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Editar", width=120, fg_color="#2196F3", hover_color="#1976D2",
        command=lambda: editar_servicio_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Eliminar", width=120, fg_color="#f44336", hover_color="#da190b",
        command=lambda: eliminar_servicio_ui(ventana, tabla, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Generar Factura", width=120, fg_color="#FF9800", hover_color="#F57C00",
        command=lambda: generar_factura_ui(ventana, estado),
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        frame_botones, text="Volver", width=120, fg_color="#9E9E9E", hover_color="#757575",
        command=lambda: volver_al_menu(ventana),
    ).pack(side="left", padx=5)

    # --- Cargar datos iniciales ---
    cargar_servicios_ui(tabla)
