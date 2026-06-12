from tkinter import messagebox

from dbconexion import validar_id, validar_nombre
from ui_helpers import ventana_lista, formulario_campos, pedir_id, cerrar_modal
import repositorio as repo


def _ver_categorias(parent):
    filas = repo.listar_categorias()
    ventana_lista(parent, "Categorías", "ID | Nombre | Descripción", filas, "650x400")


def _agregar_categoria(parent):
    def guardar(vals, form):
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        repo.crear_categoria(nombre, vals.get("descripcion", "").strip())
        messagebox.showinfo("Éxito", "Categoría creada.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Nueva Categoría", [
        ("Nombre:", "nombre"),
        ("Descripción:", "descripcion"),
    ], guardar, "380x280")


def _editar_categoria(parent):
    def guardar(vals, form):
        ok, id_cat = validar_id(vals["id"])
        if not ok:
            messagebox.showwarning("Error", id_cat, parent=form)
            return
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        if not repo.actualizar_categoria(id_cat, nombre, vals.get("descripcion", "").strip()):
            messagebox.showwarning("Aviso", "No se encontró la categoría.", parent=form)
            return
        messagebox.showinfo("Éxito", "Categoría actualizada.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Editar Categoría", [
        ("ID Categoría:", "id"),
        ("Nuevo nombre:", "nombre"),
        ("Nueva descripción:", "descripcion"),
    ], guardar, "380x320")


def _eliminar_categoria(parent):
    def confirmar(id_txt, form):
        ok, id_cat = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_cat, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar categoría ID {id_cat}?", parent=form):
            return
        if not repo.eliminar_categoria(id_cat):
            messagebox.showwarning("Aviso", "No se encontró la categoría.", parent=form)
            return
        messagebox.showinfo("Éxito", "Categoría eliminada.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Eliminar Categoría", "ID de la categoría:", confirmar)


def _ver_ubicaciones(parent):
    filas = repo.listar_ubicaciones()
    ventana_lista(parent, "Ubicaciones", "ID | Nombre | Responsable | Descripción", filas, "750x400")


def _agregar_ubicacion(parent):
    def guardar(vals, form):
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        repo.crear_ubicacion(nombre, vals.get("responsable", "").strip(), vals.get("descripcion", "").strip())
        messagebox.showinfo("Éxito", "Ubicación creada.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Nueva Ubicación", [
        ("Nombre:", "nombre"),
        ("Responsable:", "responsable"),
        ("Descripción:", "descripcion"),
    ], guardar, "380x340")


def _editar_ubicacion(parent):
    def guardar(vals, form):
        ok, id_ubi = validar_id(vals["id"])
        if not ok:
            messagebox.showwarning("Error", id_ubi, parent=form)
            return
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        if not repo.actualizar_ubicacion(id_ubi, nombre, vals.get("responsable", "").strip(), vals.get("descripcion", "").strip()):
            messagebox.showwarning("Aviso", "No se encontró la ubicación.", parent=form)
            return
        messagebox.showinfo("Éxito", "Ubicación actualizada.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Editar Ubicación", [
        ("ID Ubicación:", "id"),
        ("Nuevo nombre:", "nombre"),
        ("Responsable:", "responsable"),
        ("Descripción:", "descripcion"),
    ], guardar, "380x380")


def _eliminar_ubicacion(parent):
    def confirmar(id_txt, form):
        ok, id_ubi = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_ubi, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar ubicación ID {id_ubi}?", parent=form):
            return
        if not repo.eliminar_ubicacion(id_ubi):
            messagebox.showwarning("Aviso", "No se encontró la ubicación.", parent=form)
            return
        messagebox.showinfo("Éxito", "Ubicación eliminada.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Eliminar Ubicación", "ID de la ubicación:", confirmar)


def _ver_proveedores(parent):
    filas = repo.listar_proveedores()
    ventana_lista(parent, "Proveedores", "ID | Nombre | Teléfono | Dirección | Correo | Activo", filas, "900x450")


def _agregar_proveedor(parent):
    def guardar(vals, form):
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        repo.crear_proveedor(nombre, vals.get("telefono", "").strip(), vals.get("direccion", "").strip(), vals.get("correo", "").strip())
        messagebox.showinfo("Éxito", "Proveedor creado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Nuevo Proveedor", [
        ("Nombre:", "nombre"),
        ("Teléfono:", "telefono"),
        ("Dirección:", "direccion"),
        ("Correo:", "correo"),
    ], guardar, "380x400")


def _editar_proveedor(parent):
    def guardar(vals, form):
        ok, id_prov = validar_id(vals["id"])
        if not ok:
            messagebox.showwarning("Error", id_prov, parent=form)
            return
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        if not repo.actualizar_proveedor(id_prov, nombre, vals.get("telefono", "").strip(), vals.get("direccion", "").strip(), vals.get("correo", "").strip()):
            messagebox.showwarning("Aviso", "No se encontró el proveedor.", parent=form)
            return
        messagebox.showinfo("Éxito", "Proveedor actualizado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Editar Proveedor", [
        ("ID Proveedor:", "id"),
        ("Nombre:", "nombre"),
        ("Teléfono:", "telefono"),
        ("Dirección:", "direccion"),
        ("Correo:", "correo"),
    ], guardar, "380x420")


def _eliminar_proveedor(parent):
    def confirmar(id_txt, form):
        ok, id_prov = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_prov, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar proveedor ID {id_prov}?", parent=form):
            return
        if not repo.eliminar_proveedor(id_prov):
            messagebox.showwarning("Aviso", "No se encontró el proveedor.", parent=form)
            return
        messagebox.showinfo("Éxito", "Proveedor eliminado.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Eliminar Proveedor", "ID del proveedor:", confirmar)


MODULOS_CATALOGOS = [
    ("Categorías", _ver_categorias),
    ("Nueva Categoría", _agregar_categoria),
    (" Editar Categoría", _editar_categoria),
    (" Eliminar Categoría", _eliminar_categoria),
    (" Ubicaciones", _ver_ubicaciones),
    ("Nueva Ubicación", _agregar_ubicacion),
    ("Editar Ubicación", _editar_ubicacion),
    ("Eliminar Ubicación", _eliminar_ubicacion),
    (" Proveedores", _ver_proveedores),
    (" Nuevo Proveedor", _agregar_proveedor),
    (" Editar Proveedor", _editar_proveedor),
    (" Eliminar Proveedor", _eliminar_proveedor),
]
