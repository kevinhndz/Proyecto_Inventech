"""Utilidades reutilizables para formularios, modales y listados — Inventech UI v3 (PRO)."""

import customtkinter as ctk
from tkinter import messagebox, ttk

# ─────────────────────────────────────────────
#  PALETA COMPARTIDA — unificada con la C{} de main.py v3
#  (antes ui_helpers tenía su propia paleta ligeramente distinta)
# ─────────────────────────────────────────────
COLOR = {
    "primary":        ("#1a56db", "#3b82f6"),
    "primary_hover":  ("#1e429f", "#2563eb"),
    "primary_light":  ("#eff6ff", "#1e3a5f"),
    "bg_main":        ("#f1f5f9", "#0c111d"),   # antes "#0f172a" -> ahora igual que C["bg"]
    "bg_sidebar":     ("#ffffff", "#111827"),
    "bg_card":        ("#ffffff", "#1c2637"),   # antes "#1e293b" -> ahora igual que C["card"]
    "bg_header":      ("#1e3a8a", "#1e40af"),   # antes "#1a56db"/"#1e3a5f" -> ahora igual que C["p700"]
    "text_primary":   ("#0f172a", "#f1f5f9"),   # antes "#f8fafc"
    "text_secondary": ("#64748b", "#6b7fa3"),   # antes "#94a3b8"
    "text_white":     ("#ffffff", "#ffffff"),
    "border":         ("#e2e8f0", "#2d3f55"),   # antes "#334155"
    "danger":         ("#ef4444", "#f87171"),
    "success":        ("#0d9488", "#14b8a6"),   # acento esmeralda, igual que C["g500"]
    "success_light":  ("#ccfbf1", "#0d3d38"),   # igual que C["g100"]
}

FONT = {
    "brand":    ("Segoe UI", 18, "bold"),
    "title":    ("Segoe UI", 13, "bold"),
    "subtitle": ("Segoe UI", 11),
    "body":     ("Segoe UI", 10),
    "label":    ("Segoe UI", 9),
    "nav":      ("Segoe UI", 10, "bold"),
    "section":  ("Segoe UI", 8, "bold"),
    "small":    ("Segoe UI", 8),
    "mono":     ("Consolas", 9),
}


# ═══════════════════════════════════════════════════════════
#  HELPERS DE MODAL  (sin cambios de lógica respecto a v2)
# ═══════════════════════════════════════════════════════════
def configurar_modal(win, parent):
    """Coloca el modal encima de la ventana principal y bloquea la interacción."""
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


def _centrar_sobre_parent(win, parent, w, h):
    """Centra la ventana sobre el parent."""
    win.update_idletasks()
    px = parent.winfo_rootx() + parent.winfo_width()  // 2
    py = parent.winfo_rooty() + parent.winfo_height() // 2
    win.geometry(f"{w}x{h}+{px - w // 2}+{py - h // 2}")


def _header_modal(win, titulo):
    """Crea una cabecera azul con título para cualquier modal."""
    hdr = ctk.CTkFrame(win, fg_color=COLOR["bg_header"], corner_radius=0, height=52)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkLabel(
        hdr,
        text=titulo,
        font=FONT["title"],
        text_color=COLOR["text_white"],
    ).pack(side="left", padx=18, pady=14)
    return hdr


def _divider(parent):
    ctk.CTkFrame(parent, fg_color=COLOR["border"], height=1).pack(fill="x", padx=0)


# ═══════════════════════════════════════════════════════════
#  TABLA DE DATOS — ttk.Treeview estilizado (reemplaza ScrolledText)
# ═══════════════════════════════════════════════════════════
def _modo_idx():
    """Devuelve 0 si el modo actual es claro, 1 si es oscuro.

    Las tuplas de COLOR son (claro, oscuro), igual que en main.py.
    ttk no se re-pinta solo al cambiar de modo, así que el color
    se fija una sola vez al abrir la ventana (suficiente para
    ventanas que se abren "a demanda" como estos modales).
    """
    return 0 if ctk.get_appearance_mode() == "Light" else 1


def _ordenar_columna_factory(tree, columnas):
    """Crea un manejador de clic-en-encabezado para ordenar la tabla.

    Cada columna alterna entre orden ascendente/descendente y
    muestra una flechita (▲ / ▼) en el encabezado activo.
    """
    estado = {"col": None, "reverse": False}

    def ordenar(col):
        reverse = estado["col"] == col and not estado["reverse"]
        datos = [(tree.set(k, col), k) for k in tree.get_children("")]

        def clave(item):
            valor = item[0]
            try:
                return (0, float(valor.replace(",", "")))
            except (ValueError, AttributeError):
                return (1, str(valor).lower())

        datos.sort(key=clave, reverse=reverse)
        for indice, (_valor, k) in enumerate(datos):
            tree.move(k, "", indice)

        for c in columnas:
            simbolo = (" ▼" if reverse else " ▲") if c == col else ""
            tree.heading(c, text=c + simbolo)

        estado["col"], estado["reverse"] = col, reverse

    return ordenar


def ventana_lista(parent, titulo, encabezado, filas, geometria="860x520"):
    win = ctk.CTkToplevel(parent)
    win.title(titulo)
    win.configure(fg_color=COLOR["bg_main"])
    configurar_modal(win, parent)
    win.protocol("WM_DELETE_WINDOW", lambda: cerrar_modal(win))

    # Dimensionar y centrar
    try:
        w, h = map(int, geometria.split("x"))
    except Exception:
        w, h = 860, 520
    _centrar_sobre_parent(win, parent, w, h)
    win.geometry(f"{w}x{h}")

    _header_modal(win, titulo)

    # Contenedor principal
    body = ctk.CTkFrame(win, fg_color=COLOR["bg_card"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=16, pady=16)
    body.grid_rowconfigure(0, weight=1)
    body.grid_columnconfigure(0, weight=1)

    columnas = [c.strip() for c in encabezado.split("|")]
    idx = _modo_idx()

    bg       = COLOR["bg_card"][idx]
    fg       = COLOR["text_primary"][idx]
    head_bg  = COLOR["bg_header"][idx]
    head_fg  = COLOR["text_white"][idx]
    sel_bg   = COLOR["primary"][idx]
    alt_bg   = COLOR["primary_light"][idx]
    hover_bg = COLOR["success_light"][idx]
    muted    = COLOR["text_secondary"][idx]

    # Estilo único por ventana (evita choques si hay varias listas abiertas)
    style_name = f"Inventech{id(win)}.Treeview"
    style = ttk.Style(win)
    style.theme_use("clam")  # "clam" permite controlar todos los colores

    style.configure(
        style_name,
        background=bg, fieldbackground=bg, foreground=fg,
        rowheight=28, borderwidth=0, font=FONT["body"],
    )
    style.configure(
        f"{style_name}.Heading",
        background=head_bg, foreground=head_fg,
        font=FONT["nav"], relief="flat", padding=(8, 6),
    )
    style.map(
        style_name,
        background=[("selected", sel_bg)],
        foreground=[("selected", COLOR["text_white"][idx])],
    )
    style.map(f"{style_name}.Heading", background=[("active", head_bg)])

    tree = ttk.Treeview(body, columns=columnas, show="headings", style=style_name)
    ordenar = _ordenar_columna_factory(tree, columnas)

    for j, col in enumerate(columnas):
        max_len = len(col)
        for f in filas or []:
            if j < len(f):
                max_len = max(max_len, len(str(f[j])))
        ancho = min(max(max_len * 7 + 24, 90), 320)
        tree.heading(col, text=col, command=lambda c=col: ordenar(c))
        tree.column(col, anchor="w", width=ancho, stretch=True)

    vsb = ctk.CTkScrollbar(body, orientation="vertical", command=tree.yview,
                           button_color=COLOR["border"], fg_color="transparent")
    hsb = ctk.CTkScrollbar(body, orientation="horizontal", command=tree.xview,
                           button_color=COLOR["border"], fg_color="transparent")
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # Filas alternadas + fila "vacía" + tag de hover
    tree.tag_configure("oddrow", background=bg, foreground=fg)
    tree.tag_configure("evenrow", background=alt_bg, foreground=fg)
    tree.tag_configure("empty", background=bg, foreground=muted)
    tree.tag_configure("hover", background=hover_bg)

    if filas:
        for i, fila in enumerate(filas):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=fila, tags=(tag,))
    else:
        vacio = ["(Sin registros)"] + [""] * (len(columnas) - 1)
        tree.insert("", "end", values=vacio, tags=("empty",))

    # Resalta la fila bajo el cursor
    def _quitar_hover():
        for item in tree.get_children():
            tags = [t for t in tree.item(item, "tags") if t != "hover"]
            tree.item(item, tags=tuple(tags))

    def _on_motion(event):
        fila_id = tree.identify_row(event.y)
        _quitar_hover()
        if fila_id:
            tags = list(tree.item(fila_id, "tags")) + ["hover"]
            tree.item(fila_id, tags=tuple(tags))

    tree.bind("<Motion>", _on_motion)
    tree.bind("<Leave>", lambda e: _quitar_hover())

    _divider(win)

    # Footer con contador + botón
    footer = ctk.CTkFrame(win, fg_color=COLOR["bg_card"], height=54)
    footer.pack(fill="x")
    footer.pack_propagate(False)

    total = len(filas) if filas else 0
    etiqueta_total = "registro" if total == 1 else "registros"
    ctk.CTkLabel(footer, text=f"{total} {etiqueta_total}", font=FONT["small"],
                  text_color=COLOR["text_secondary"]).pack(side="left", padx=18)

    ctk.CTkButton(
        footer,
        text="Cerrar",
        width=110, height=36,
        font=FONT["nav"],
        fg_color=COLOR["primary"],
        hover_color=COLOR["primary_hover"],
        text_color=COLOR["text_white"],
        corner_radius=8,
        command=lambda: cerrar_modal(win),
    ).pack(side="right", padx=16, pady=9)

    return win


# ═══════════════════════════════════════════════════════════
#  FORMULARIO GENÉRICO  (sin cambios de lógica)
# ═══════════════════════════════════════════════════════════
def formulario_campos(parent, titulo, campos, on_guardar, geometria="420x520"):
    """
    campos: lista de (label, key) o (label, key, opciones_combo).
    Lógica de on_guardar sin cambios.
    """
    try:
        w, h = map(int, geometria.split("x"))
    except Exception:
        w, h = 420, 520

    form = ctk.CTkToplevel(parent)
    form.title(titulo)
    form.configure(fg_color=COLOR["bg_main"])
    configurar_modal(form, parent)
    form.protocol("WM_DELETE_WINDOW", lambda: cerrar_modal(form))
    _centrar_sobre_parent(form, parent, w, h)
    form.geometry(f"{w}x{h}")

    _header_modal(form, titulo)

    # Cuerpo con scroll
    scroll = ctk.CTkScrollableFrame(
        form,
        fg_color=COLOR["bg_card"],
        corner_radius=0,
        scrollbar_button_color=COLOR["border"],
    )
    scroll.pack(fill="both", expand=True, padx=0, pady=0)

    entries = {}
    for campo in campos:
        label_txt, key = campo[0], campo[1]

        ctk.CTkLabel(
            scroll,
            text=label_txt.upper(),
            font=FONT["section"],
            text_color=COLOR["text_secondary"],
            anchor="w",
        ).pack(anchor="w", padx=22, pady=(16, 3))

        if len(campo) > 2 and campo[2]:
            widget = ctk.CTkComboBox(
                scroll,
                values=campo[2],
                width=340, height=38,
                font=FONT["body"],
                border_color=COLOR["border"],
                corner_radius=8,
            )
            widget.set(campo[2][0])
        else:
            widget = ctk.CTkEntry(
                scroll,
                width=340, height=38,
                font=FONT["body"],
                border_color=COLOR["border"],
                corner_radius=8,
            )
        widget.pack(padx=22, pady=(0, 2))
        entries[key] = widget

    _divider(form)

    # Footer con botones
    footer = ctk.CTkFrame(form, fg_color=COLOR["bg_card"], height=58)
    footer.pack(fill="x")
    footer.pack_propagate(False)

    def guardar():
        valores = {k: (w.get() if hasattr(w, "get") else "") for k, w in entries.items()}
        try:
            on_guardar(valores, form)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=form)

    ctk.CTkButton(
        footer,
        text="Guardar",
        width=120, height=36,
        font=FONT["nav"],
        fg_color=COLOR["primary"],
        hover_color=COLOR["primary_hover"],
        text_color=COLOR["text_white"],
        corner_radius=8,
        command=guardar,
    ).pack(side="left", padx=16, pady=11)

    ctk.CTkButton(
        footer,
        text="Cancelar",
        width=110, height=36,
        font=FONT["nav"],
        fg_color="transparent",
        hover_color=COLOR["bg_main"],
        text_color=COLOR["text_secondary"],
        border_width=1,
        border_color=COLOR["border"],
        corner_radius=8,
        command=lambda: cerrar_modal(form),
    ).pack(side="left", pady=11)

    return form, entries


# ═══════════════════════════════════════════════════════════
#  MODAL DE CONFIRMACIÓN POR ID  (sin cambios de lógica)
# ═══════════════════════════════════════════════════════════
def pedir_id(parent, titulo, mensaje, on_confirmar):
    w, h = 380, 210
    form = ctk.CTkToplevel(parent)
    form.title(titulo)
    form.configure(fg_color=COLOR["bg_main"])
    configurar_modal(form, parent)
    form.protocol("WM_DELETE_WINDOW", lambda: cerrar_modal(form))
    _centrar_sobre_parent(form, parent, w, h)
    form.geometry(f"{w}x{h}")

    _header_modal(form, titulo)

    body = ctk.CTkFrame(form, fg_color=COLOR["bg_card"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=0, pady=0)

    ctk.CTkLabel(
        body,
        text=mensaje,
        font=FONT["subtitle"],
        text_color=COLOR["text_primary"],
        wraplength=320,
    ).pack(pady=(20, 10), padx=24)

    entry = ctk.CTkEntry(
        body,
        width=300, height=38,
        font=FONT["body"],
        border_color=COLOR["border"],
        corner_radius=8,
        placeholder_text="Ingresa el ID...",
    )
    entry.pack(padx=24)
    entry.focus_set()

    _divider(form)

    footer = ctk.CTkFrame(form, fg_color=COLOR["bg_card"], height=54)
    footer.pack(fill="x")
    footer.pack_propagate(False)

    def confirmar():
        try:
            on_confirmar(entry.get(), form)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=form)

    entry.bind("<Return>", lambda e: confirmar())

    ctk.CTkButton(
        footer,
        text="Confirmar",
        width=120, height=36,
        font=FONT["nav"],
        fg_color=COLOR["primary"],
        hover_color=COLOR["primary_hover"],
        text_color=COLOR["text_white"],
        corner_radius=8,
        command=confirmar,
    ).pack(side="left", padx=16, pady=9)

    ctk.CTkButton(
        footer,
        text="Cancelar",
        width=110, height=36,
        font=FONT["nav"],
        fg_color="transparent",
        hover_color=COLOR["bg_main"],
        text_color=COLOR["text_secondary"],
        border_width=1,
        border_color=COLOR["border"],
        corner_radius=8,
        command=lambda: cerrar_modal(form),
    ).pack(side="left", pady=9)

    return form