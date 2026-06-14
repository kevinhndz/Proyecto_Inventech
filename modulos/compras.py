from tkinter import messagebox

from dbconexion import validar_cantidad, validar_id
from ui_helpers import ventana_lista, formulario_campos, pedir_id, cerrar_modal
import repositorio as repo


def _opciones_proveedores():
    return [f"{r[0]} - {r[1]}" for r in repo.listar_proveedores()] or ["(sin proveedores)"]


def _opciones_materiales():
    return [f"{r[0]} - {r[1]}" for r in repo.listar_materiales_opciones()] or ["(sin materiales)"]


def _parse_id(valor):
    return int(valor.split(" - ")[0])


def ver_compras(parent):
    filas = repo.listar_compras()
    ventana_lista(parent, "Compras", "ID | Proveedor | Fecha | Total | Estado | Descripción", filas, "900x450")


def ver_detalle_compras(parent):
    filas = repo.listar_detalle_compras()
    ventana_lista(parent, "Detalle Compras", "ID | Compra | Material | Cantidad | Precio | Subtotal", filas, "900x450")


def nueva_compra(parent):
    def guardar(vals, form):
        if vals["proveedor"].startswith("("):
            messagebox.showwarning("Error", "No hay proveedores.", parent=form)
            return
        repo.crear_compra(_parse_id(vals["proveedor"]), vals.get("descripcion", "").strip(), vals.get("usuario", "Sistema").strip())
        messagebox.showinfo("Éxito", "Compra creada (estado Pendiente).", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Nueva Compra", [
        ("Proveedor:", "proveedor", _opciones_proveedores()),
        ("Descripción:", "descripcion"),
        ("Usuario:", "usuario"),
    ], guardar, "380x300")


def agregar_articulo_compra(parent):
    def guardar(vals, form):
        ok, id_compra = validar_id(vals["compra"])
        if not ok:
            messagebox.showwarning("Error", id_compra, parent=form)
            return
        if vals["material"].startswith("("):
            messagebox.showwarning("Error", "No hay materiales.", parent=form)
            return
        ok, cantidad = validar_cantidad(vals["cantidad"])
        if not ok:
            messagebox.showwarning("Error", cantidad, parent=form)
            return
        try:
            precio = float(vals["precio"])
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "Precio inválido.", parent=form)
            return
        repo.agregar_detalle_compra(id_compra, _parse_id(vals["material"]), cantidad, precio)
        messagebox.showinfo("Éxito", "Artículo agregado a la compra.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Agregar Artículo a Compra", [
        ("ID Compra:", "compra"),
        ("Material:", "material", _opciones_materiales()),
        ("Cantidad:", "cantidad"),
        ("Precio unitario:", "precio"),
    ], guardar, "420x380")


def completar_compra(parent):
    def confirmar(id_txt, form):
        ok, id_compra = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_compra, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Completar compra #{id_compra}? Se registrarán entradas de stock.", parent=form):
            return
        repo.completar_compra(id_compra)
        messagebox.showinfo("Éxito", "Compra completada y stock actualizado.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Completar Compra", "ID de la compra:", confirmar)


MODULOS_COMPRAS = [
    (" Ver Compras", ver_compras),
    (" Detalle Compras", ver_detalle_compras),
    ("Nueva Compra", nueva_compra),
    (" Agregar Artículo", agregar_articulo_compra),
    (" Completar Compra", completar_compra),
]
