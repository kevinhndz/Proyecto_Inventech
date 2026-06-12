from tkinter import messagebox

from dbconexion import validar_cantidad, validar_id
from ui_helpers import ventana_lista, formulario_campos, cerrar_modal
import repositorio as repo


def _opciones_materiales():
    return [f"{r[0]} - {r[1]} (stock: {r[2]})" for r in repo.listar_materiales_opciones()] or ["(sin materiales)"]


def _parse_material(valor):
    return int(valor.split(" - ")[0])


def ver_movimientos(parent):
    filas = repo.listar_movimientos()
    ventana_lista(parent, "Movimientos", "ID | Fecha | Material | Tipo | Cantidad | Motivo | Usuario", filas, "950x500")


def registrar_movimiento(parent):
    def guardar(vals, form):
        if vals["material"].startswith("("):
            messagebox.showwarning("Error", "No hay materiales disponibles.", parent=form)
            return
        ok, cantidad = validar_cantidad(vals["cantidad"])
        if not ok:
            messagebox.showwarning("Error", cantidad, parent=form)
            return
        tipo = vals["tipo"]
        if tipo not in ("Entrada", "Salida"):
            messagebox.showwarning("Error", "Tipo de movimiento inválido.", parent=form)
            return
        repo.registrar_movimiento(
            _parse_material(vals["material"]),
            tipo,
            cantidad,
            vals.get("motivo", "").strip(),
            vals.get("usuario", "Sistema").strip() or "Sistema",
        )
        messagebox.showinfo("Éxito", "Movimiento registrado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Registrar Movimiento", [
        ("Material:", "material", _opciones_materiales()),
        ("Tipo:", "tipo", ["Entrada", "Salida"]),
        ("Cantidad:", "cantidad"),
        ("Motivo:", "motivo"),
        ("Usuario:", "usuario"),
    ], guardar, "420x400")


def ver_alertas(parent):
    filas = repo.listar_alertas()
    ventana_lista(parent, "Alertas de Stock", "ID | Material | Actual | Mínimo | Estado | Fecha", filas, "850x450")


def configurar_alerta(parent):
    def guardar(vals, form):
        if vals["material"].startswith("("):
            messagebox.showwarning("Error", "No hay materiales.", parent=form)
            return
        ok, nivel = validar_cantidad(vals["nivel"])
        if not ok:
            messagebox.showwarning("Error", nivel, parent=form)
            return
        repo.configurar_alerta(_parse_material(vals["material"]), nivel)
        messagebox.showinfo("Éxito", "Alerta configurada.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Configurar Alerta", [
        ("Material:", "material", _opciones_materiales()),
        ("Nivel mínimo:", "nivel"),
    ], guardar, "380x260")


def ver_historial(parent):
    filas = repo.listar_historial()
    ventana_lista(parent, "Historial", "ID | Material | Anterior | Nueva | Usuario | Motivo | Fecha", filas, "950x500")


def ver_inventario_inicial(parent):
    filas = repo.listar_inventario_inicial()
    ventana_lista(parent, "Inventario Inicial", "ID | Material | Cantidad Inicial | Fecha", filas, "700x400")


def registrar_inventario_inicial(parent):
    def guardar(vals, form):
        if vals["material"].startswith("("):
            messagebox.showwarning("Error", "No hay materiales.", parent=form)
            return
        ok, cantidad = validar_cantidad(vals["cantidad"])
        if not ok:
            messagebox.showwarning("Error", cantidad, parent=form)
            return
        repo.registrar_inventario_inicial(_parse_material(vals["material"]), cantidad)
        messagebox.showinfo("Éxito", "Inventario inicial registrado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Inventario Inicial", [
        ("Material:", "material", _opciones_materiales()),
        ("Cantidad inicial:", "cantidad"),
    ], guardar, "380x260")


MODULOS_INVENTARIO = [
    ("Ver Movimientos", ver_movimientos),
    (" Registrar Movimiento", registrar_movimiento),
    (" Alertas de Stock", ver_alertas),
    (" Configurar Alerta", configurar_alerta),
    (" Historial", ver_historial),
    (" Inventario Inicial", ver_inventario_inicial),
    (" Registrar Inv. Inicial", registrar_inventario_inicial),
]
