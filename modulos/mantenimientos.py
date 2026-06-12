from tkinter import messagebox

from dbconexion import validar_fecha, validar_id
from ui_helpers import ventana_lista, formulario_campos, pedir_id, cerrar_modal
import repositorio as repo


def _opciones_materiales():
    return [f"{r[0]} - {r[1]}" for r in repo.listar_materiales_opciones()] or ["(sin materiales)"]


def _parse_id(valor):
    return int(valor.split(" - ")[0])


def ver_mantenimientos(parent):
    filas = repo.listar_mantenimientos()
    ventana_lista(
        parent, "Mantenimientos",
        "ID | Material | Fecha | Descripción | Costo | Técnico | Próximo",
        filas, "950x450",
    )


def registrar_mantenimiento(parent):
    def guardar(vals, form):
        if vals["material"].startswith("("):
            messagebox.showwarning("Error", "No hay materiales.", parent=form)
            return
        ok, fecha = validar_fecha(vals["fecha"])
        if not ok:
            messagebox.showwarning("Error", fecha, parent=form)
            return
        try:
            costo = float(vals.get("costo") or 0)
            if costo < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "Costo inválido.", parent=form)
            return
        proximo = vals.get("proximo", "").strip()
        if proximo:
            ok, proximo = validar_fecha(proximo)
            if not ok:
                messagebox.showwarning("Error", proximo, parent=form)
                return
        repo.crear_mantenimiento(
            _parse_id(vals["material"]),
            vals["fecha"],
            vals.get("descripcion", "").strip(),
            costo,
            vals.get("tecnico", "").strip(),
            proximo or "",
        )
        messagebox.showinfo("Éxito", "Mantenimiento registrado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Registrar Mantenimiento", [
        ("Material:", "material", _opciones_materiales()),
        ("Fecha (YYYY-MM-DD):", "fecha"),
        ("Descripción:", "descripcion"),
        ("Costo:", "costo"),
        ("Técnico:", "tecnico"),
        ("Próximo (YYYY-MM-DD):", "proximo"),
    ], guardar, "420x480")


def eliminar_mantenimiento(parent):
    def confirmar(id_txt, form):
        ok, id_mant = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_mant, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar mantenimiento ID {id_mant}?", parent=form):
            return
        if not repo.eliminar_mantenimiento(id_mant):
            messagebox.showwarning("Aviso", "No se encontró el registro.", parent=form)
            return
        messagebox.showinfo("Éxito", "Mantenimiento eliminado.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Eliminar Mantenimiento", "ID del mantenimiento:", confirmar)


MODULOS_MANTENIMIENTOS = [
    (" Ver Mantenimientos", ver_mantenimientos),
    ("Registrar Mantenimiento", registrar_mantenimiento),
    (" Eliminar Mantenimiento", eliminar_mantenimiento),
]
