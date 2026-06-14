from tkinter import messagebox

from dbconexion import validar_id, validar_nombre
from ui_helpers import ventana_lista, formulario_campos, pedir_id, cerrar_modal
import repositorio as repo


def _opciones_roles():
    return [f"{r[0]} - {r[1]}" for r in repo.listar_roles()] or ["(sin roles)"]


def _parse_id(valor):
    return int(valor.split(" - ")[0])


def ver_usuarios(parent):
    filas = repo.listar_usuarios()
    ventana_lista(parent, "Usuarios", "ID | Nombre | Rol | Correo | Activo", filas, "750x400")


def ver_roles(parent):
    filas = repo.listar_roles()
    ventana_lista(parent, "Roles", "ID | Rol | Descripción", filas, "550x350")


def agregar_usuario(parent):
    def guardar(vals, form):
        ok, nombre = validar_nombre(vals["nombre"])
        if not ok:
            messagebox.showwarning("Error", nombre, parent=form)
            return
        correo = vals.get("correo", "").strip()
        if not correo or "@" not in correo:
            messagebox.showwarning("Error", "Correo inválido.", parent=form)
            return
        if vals["rol"].startswith("("):
            messagebox.showwarning("Error", "No hay roles.", parent=form)
            return
        repo.crear_usuario(nombre, _parse_id(vals["rol"]), correo)
        messagebox.showinfo("Éxito", "Usuario creado.", parent=form)
        cerrar_modal(form)

    formulario_campos(parent, "Nuevo Usuario", [
        ("Nombre:", "nombre"),
        ("Correo:", "correo"),
        ("Rol:", "rol", _opciones_roles()),
    ], guardar, "380x300")


def eliminar_usuario(parent):
    def confirmar(id_txt, form):
        ok, id_user = validar_id(id_txt)
        if not ok:
            messagebox.showwarning("Error", id_user, parent=form)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar usuario ID {id_user}?", parent=form):
            return
        if not repo.eliminar_usuario(id_user):
            messagebox.showwarning("Aviso", "No se encontró el usuario.", parent=form)
            return
        messagebox.showinfo("Éxito", "Usuario eliminado.", parent=form)
        cerrar_modal(form)

    pedir_id(parent, "Eliminar Usuario", "ID del usuario:", confirmar)


MODULOS_USUARIOS = [
    (" Ver Usuarios", ver_usuarios),
    (" Ver Roles", ver_roles),
    (" Nuevo Usuario", agregar_usuario),
    (" Eliminar Usuario", eliminar_usuario),
]
