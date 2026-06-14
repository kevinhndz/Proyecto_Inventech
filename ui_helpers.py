"""Utilidades reutilizables para formularios y listados."""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext


def configurar_modal(win, parent):
    """Coloca el modal encima de la ventana principal y bloquea interacción con ella."""
    win.transient(parent)
    win.resizable(True, True)

    def traer_al_frente():
        win.lift()
        win.focus_force()
        try:
            win.attributes("-topmost", True)
            win.after(150, lambda: win.attributes("-topmost", False))
        except Exception:
            pass

    win.update_idletasks()
    traer_al_frente()
    win.after(50, traer_al_frente)
    win.grab_set()


def cerrar_modal(win):
    try:
        win.grab_release()
    except Exception:
        pass
    win.destroy()


def ventana_lista(parent, titulo, encabezado, filas, geometria="800x500"):
    win = ctk.CTkToplevel(parent)
    win.title(titulo)
    win.geometry(geometria)
    configurar_modal(win, parent)
    win.protocol("WM_DELETE_WINDOW", lambda: cerrar_modal(win))

    texto = encabezado + "\n" + "-" * min(120, len(encabezado)) + "\n"
    if filas:
        for fila in filas:
            texto += " | ".join(str(c) for c in fila) + "\n"
    else:
        texto += "\n(No hay registros)\n"

    widget = scrolledtext.ScrolledText(win, height=22, width=120, font=("Courier", 9))
    widget.pack(padx=10, pady=10, fill="both", expand=True)
    widget.insert("1.0", texto)
    widget.config(state="disabled")
    ctk.CTkButton(win, text="Cerrar", command=lambda: cerrar_modal(win)).pack(pady=5)
    return win


def formulario_campos(parent, titulo, campos, on_guardar, geometria="400x480"):
    """campos: lista de (label, key) o (label, key, opciones_combo)."""
    form = ctk.CTkToplevel(parent)
    form.title(titulo)
    form.geometry(geometria)
    configurar_modal(form, parent)
    form.protocol("WM_DELETE_WINDOW", lambda: cerrar_modal(form))

    frame = ctk.CTkScrollableFrame(form)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    entries = {}
    for campo in campos:
        label, key = campo[0], campo[1]
        ctk.CTkLabel(frame, text=label, font=("Arial", 11)).pack(pady=(10, 0))
        if len(campo) > 2 and campo[2]:
            widget = ctk.CTkComboBox(frame, values=campo[2], width=280)
            widget.set(campo[2][0])
        else:
            widget = ctk.CTkEntry(frame, width=280)
        widget.pack(pady=5)
        entries[key] = widget

    def guardar():
        valores = {}
        for key, widget in entries.items():
            valores[key] = widget.get() if hasattr(widget, "get") else ""
        try:
            on_guardar(valores, form)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=form)

    frame_btn = ctk.CTkFrame(form)
    frame_btn.pack(pady=10)
    ctk.CTkButton(frame_btn, text="Guardar", command=guardar, width=100).pack(side="left", padx=5)
    ctk.CTkButton(frame_btn, text="Cancelar", command=lambda: cerrar_modal(form), width=100).pack(side="left", padx=5)
    return form, entries


def pedir_id(parent, titulo, mensaje, on_confirmar):
    form = ctk.CTkToplevel(parent)
    form.title(titulo)
    form.geometry("350x180")
    configurar_modal(form, parent)
    form.protocol("WM_DELETE_WINDOW", lambda: cerrar_modal(form))

    ctk.CTkLabel(form, text=mensaje, font=("Arial", 12)).pack(pady=15)
    entry = ctk.CTkEntry(form, width=200)
    entry.pack(pady=5)
    entry.focus_set()

    def confirmar():
        try:
            on_confirmar(entry.get(), form)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=form)

    frame_btn = ctk.CTkFrame(form)
    frame_btn.pack(pady=15)
    ctk.CTkButton(frame_btn, text="Confirmar", command=confirmar, width=100).pack(side="left", padx=5)
    ctk.CTkButton(frame_btn, text="Cancelar", command=lambda: cerrar_modal(form), width=100).pack(side="left", padx=5)
