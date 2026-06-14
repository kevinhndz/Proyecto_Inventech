from tkinter import messagebox

from dbconexion import validar_cantidad, validar_id, validar_nombre
from ui_helpers import ventana_lista, formulario_campos, pedir_id, cerrar_modal
import repositorio as repo


def _opciones_materiales():
    return [f"{r[0]} - {r[1]} (stock: {r[2]})" for r in repo.listar_materiales_opciones()] or ["(sin materiales)"]


def _parse_id(valor):
    return int(valor.split(" - ")[0])


def ver_prestamos(parent):
    filas = repo.listar_prestamos()
    ventana_lista(parent, "Préstamos", "ID | Usuario | Fecha | Estado | Descripción | Responsable", filas, "900x450")


def ver_detalle_prestamos(parent):
    filas = repo.listar_detalle_prestamos()
    ventana_lista(parent, "Detalle Préstamos", "ID | Préstamo | Material | Cantidad | Devolución | Devuelto", filas, "850x450")


def nuevo_prestamo(parent):
    def guardar(vals, form):
        ok, nombre = validar_nombre(vals["usuario"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        repo.crear_prestamo(nombre, vals.get("descripcion", "").strip(), vals.get("responsable", "").strip())
        messagebox.showinfo("Éxito", "Préstamo creado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Nuevo Préstamo", [
        ("Nombre usuario:", "usuario"),
        ("Descripción:", "descripcion"),
        ("Responsable:", "responsable"),
    ], guardar, "380x300")


def agregar_articulo_prestamo(parent):
    def guardar(vals, form):
        ok, id_prestamo = validar_id(vals["prestamo"])
        if not ok:
            messagebox.showwarning("Error", id_prestamo, parent=form)
            return
        if vals["material"].startswith("("):
            messagebox.showwarning("Error", "No hay materiales.", parent=form)
            return
        ok, cantidad = validar_cantidad(vals["cantidad"])
        if not ok:
            messagebox.showwarning("Error", cantidad, parent=form)
            return
        repo.agregar_detalle_prestamo(id_prestamo, _parse_id(vals["material"]), cantidad, vals.get("usuario", "Sistema").strip())
        messagebox.showinfo("Éxito", "Artículo prestado (stock descontado).", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Agregar Artículo al Préstamo", [
        ("ID Préstamo:", "prestamo"),
        ("Material:", "material", _opciones_materiales()),
        ("Cantidad:", "cantidad"),
        ("Usuario:", "usuario"),
    ], guardar, "420x380")


def devolver_prestamo(parent):
    def confirmar(id_txt, form):
        ok, id_prestamo = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_prestamo, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Registrar devolución del préstamo #{id_prestamo}?", parent=form):
            return
        repo.devolver_prestamo(id_prestamo)
        messagebox.showinfo("Éxito", "Préstamo devuelto y stock restaurado.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Devolver Préstamo", "ID del préstamo:", confirmar)


MODULOS_PRESTAMOS = [
    (" Ver Préstamos", ver_prestamos),
    (" Detalle Préstamos", ver_detalle_prestamos),
    (" Nuevo Préstamo", nuevo_prestamo),
    (" Agregar Artículo", agregar_articulo_prestamo),
    ("Devolver Préstamo", devolver_prestamo),
]
