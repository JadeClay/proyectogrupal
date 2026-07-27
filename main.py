# ============================================================
# main.py  --  ARCHIVO PRINCIPAL
# ============================================================
# Este es el punto de entrada del programa.
# Se ejecuta primero y arranca todo.
#
# FLUJO:
#   1) Crea la ventana principal
#   2) Muestra la pantalla de login
#   3) Si el login es correcto, muestra el menu
#   4) Si cierran sesion, vuelve al login
#   5) Si salen, cierra todo
# ============================================================

# Librerias externas
import customtkinter as ctk
from tkinter import messagebox

# Codigo propio    
from ventana_menu import mostrar_menu

# Configurar tema oscuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ventana principal (se crea una sola vez)
RAIZ = None


# ============================================================
# FUNCIONES DE NAVEGACION
# ============================================================

def iniciar_sistema():
    """Crea la ventana principal y arranca el programa."""
    global RAIZ

    RAIZ = ctk.CTk()
    RAIZ.title("Mi Sistema")

    mostrar_login(despues_login)

    RAIZ.mainloop()


def mostrar_login(callback_ok):
    """Muestra la pantalla de login."""
    from ventana_login import mostrar_login as login

    limpiar_ventana(RAIZ)
    login(RAIZ, callback_ok)

    RAIZ.protocol("WM_DELETE_WINDOW", confirmar_salida)

# FUNCION CALLBACK PARA EL LOGIN
def despues_login(id_usuario, nombre_usuario, email_usuario):

    limpiar_ventana(RAIZ)

    mostrar_menu(
        RAIZ,
        id_usuario,
        nombre_usuario,
        email_usuario,
        callback_cerrar_sesion=volver_al_login
    )

    RAIZ.protocol("WM_DELETE_WINDOW", volver_al_login)


def volver_al_login():
    """Vuelve a la pantalla de login."""
    limpiar_ventana(RAIZ)
    mostrar_login(despues_login)


def limpiar_ventana(ventana):
    """Elimina todos los widgets de una ventana."""
    for widget in ventana.winfo_children():
        widget.destroy()


def confirmar_salida():
    """Pregunta si quiere salir y cierra el programa."""
    respuesta = messagebox.askyesno(
        "Salir",
        "Esta seguro que desea salir del sistema?"
    )

    if respuesta:
        RAIZ.quit()


# ============================================================
# ARRANCAR EL PROGRAMA
# ============================================================

if __name__ == "__main__":
    print("Iniciando sistema...")
    iniciar_sistema()
