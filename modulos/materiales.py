from tkinter import messagebox

from dbconexion import validar_cantidad, validar_fecha, validar_id, validar_nombre
from ui_helpers import ventana_lista, formulario_campos, pedir_id, cerrar_modal
import repositorio as repo


def _opciones_categorias():
    return [f"{r[0]} - {r[1]}" for r in repo.listar_categorias()] or ["(sin categorías)"]


def _opciones_ubicaciones():
    return [f"{r[0]} - {r[1]}" for r in repo.listar_ubicaciones()] or ["(sin ubicaciones)"]


def _parse_combo_id(valor):
    return int(valor.split(" - ")[0])


def ver_materiales(parent):
    filas = repo.listar_materiales()
    ventana_lista(parent, "Materiales", "ID | Nombre | Cantidad | Categoría | Ubicación | Fecha", filas)


def agregar_material(parent):
    def guardar(vals, form):
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        ok, cantidad = validar_cantidad(vals["cantidad"])
        if not ok:
            messagebox.showwarning("Error", cantidad, parent=form)
            return
        ok, fecha = validar_fecha(vals["fecha"])
        if not ok:
            messagebox.showwarning("Error", fecha, parent=form)
            return
        try:
            id_cat = _parse_combo_id(vals["categoria"])
            id_ubi = _parse_combo_id(vals["ubicacion"])
        except (ValueError, IndexError):
            messagebox.showwarning("Error", "Selecciona categoría y ubicación válidas.", parent=form)
            return
        precio = float(vals.get("precio") or 0)
        repo.crear_material(nombre, cantidad, id_cat, id_ubi, fecha, vals.get("descripcion", "").strip(), precio)
        messagebox.showinfo("Éxito", "Material agregado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Agregar Material", [
        ("Nombre:", "nombre"),
        ("Cantidad:", "cantidad"),
        ("Categoría:", "categoria", _opciones_categorias()),
        ("Ubicación:", "ubicacion", _opciones_ubicaciones()),
        ("Fecha (YYYY-MM-DD):", "fecha"),
        ("Precio unitario:", "precio"),
        ("Descripción:", "descripcion"),
    ], guardar, "420x520")


def actualizar_material(parent):
    def guardar(vals, form):
        ok, id_mat = validar_id(vals["id"])
        if not ok:
            messagebox.showwarning("Error", id_mat, parent=form)
            return
        datos = {}
        if vals.get("nombre", "").strip():
            ok, nombre = validar_nombre(vals["nombre"])
            if not ok:
                messagebox.showwarning("Error", nombre, parent=form)
                return
            datos["nombre"] = nombre
        if vals.get("cantidad", "").strip():
            ok, cantidad = validar_cantidad(vals["cantidad"])
            if not ok:
                messagebox.showwarning("Error", cantidad, parent=form)
                return
            datos["cantidad"] = cantidad
        if vals.get("categoria", "").strip() and not vals["categoria"].startswith("("):
            datos["categoria"] = _parse_combo_id(vals["categoria"])
        if vals.get("ubicacion", "").strip() and not vals["ubicacion"].startswith("("):
            datos["ubicacion"] = _parse_combo_id(vals["ubicacion"])
        if vals.get("fecha", "").strip():
            ok, fecha = validar_fecha(vals["fecha"])
            if not ok:
                messagebox.showwarning("Error", fecha, parent=form)
                return
            datos["fecha"] = fecha
        if vals.get("precio", "").strip():
            datos["precio"] = float(vals["precio"])
        if vals.get("descripcion", "").strip():
            datos["descripcion"] = vals["descripcion"].strip()
        if not datos:
            messagebox.showwarning("Aviso", "Ingresa al menos un campo.", parent=form)
            return
        if not repo.actualizar_material(id_mat, datos):
            messagebox.showwarning("Aviso", "No se encontró el material.", parent=form)
            return
        messagebox.showinfo("Éxito", "Material actualizado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Actualizar Material", [
        ("ID Material:", "id"),
        ("Nuevo nombre:", "nombre"),
        ("Nueva cantidad:", "cantidad"),
        ("Categoría:", "categoria", [""] + _opciones_categorias()),
        ("Ubicación:", "ubicacion", [""] + _opciones_ubicaciones()),
        ("Nueva fecha:", "fecha"),
        ("Precio:", "precio"),
        ("Descripción:", "descripcion"),
    ], guardar, "420x580")


def eliminar_material(parent):
    def confirmar(id_txt, form):
        ok, id_mat = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_mat, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar material ID {id_mat}?", parent=form):
            return
        if not repo.eliminar_material(id_mat):
            messagebox.showwarning("Aviso", "No se encontró el material.", parent=form)
            return
        messagebox.showinfo("Éxito", "Material eliminado.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Eliminar Material", "ID del material:", confirmar)


MODULOS_MATERIALES = [
    (" Ver Materiales", ver_materiales),
    (" Agregar Material", agregar_material),
    (" Actualizar Material", actualizar_material),
    (" Eliminar Material", eliminar_material),
]
