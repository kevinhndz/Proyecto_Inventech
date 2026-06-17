import customtkinter as ctk
from tkinter import messagebox
from modulos import MODULOS_SIDEBAR
from repositorio import validar_login

# ─────────────────────────────────────────────
#  PALETA GLOBAL
# ─────────────────────────────────────────────
COLOR = {
    # Azul primario
    "primary":        ("#1a56db", "#3b82f6"),
    "primary_hover":  ("#1e429f", "#2563eb"),
    "primary_light":  ("#eff6ff", "#1e3a5f"),

    # Fondos
    "bg_main":        ("#f1f5f9", "#0f172a"),
    "bg_sidebar":     ("#ffffff", "#111827"),
    "bg_card":        ("#ffffff", "#1e293b"),
    "bg_header":      ("#1a56db", "#1e3a5f"),

    # Texto
    "text_primary":   ("#0f172a", "#f8fafc"),
    "text_secondary": ("#64748b", "#94a3b8"),
    "text_white":     ("#ffffff", "#ffffff"),

    # Bordes / separadores
    "border":         ("#e2e8f0", "#334155"),
    "sidebar_active": ("#eff6ff", "#1e3a5f"),

    # Estados
    "success":        ("#10b981", "#34d399"),
    "warning":        ("#f59e0b", "#fbbf24"),
    "danger":         ("#ef4444", "#f87171"),

    # Sidebar hover
    "sidebar_hover":  ("#f1f5f9", "#1e293b"),
}

FONT = {
    "brand":    ("Segoe UI", 18, "bold"),
    "title":    ("Segoe UI", 15, "bold"),
    "subtitle": ("Segoe UI", 11),
    "body":     ("Segoe UI", 10),
    "label":    ("Segoe UI", 9),
    "nav":      ("Segoe UI", 10, "bold"),
    "section":  ("Segoe UI", 8, "bold"),
    "small":    ("Segoe UI", 8),
}


# ═══════════════════════════════════════════════════════════
#  VENTANA DE LOGIN
# ═══════════════════════════════════════════════════════════
class VentanaLogin(ctk.CTk):
    def __init__(self, callback_exito):
        super().__init__()
        self.callback_exito = callback_exito
        self.title("Inventech — Acceso")
        self.geometry("420x560")
        self.resizable(False, False)
        self.configure(fg_color=COLOR["bg_main"])

        self._construir_ui()
        self._centrar_ventana()

    def _centrar_ventana(self):
        self.update_idletasks()
        w, h = 420, 560
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _construir_ui(self):
        # ── Tarjeta central ──
        card = ctk.CTkFrame(
            self,
            fg_color=COLOR["bg_card"],
            corner_radius=16,
            border_width=1,
            border_color=COLOR["border"],
        )
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.90)

        # Bloque de marca (cabecera azul redondeada)
        brand_block = ctk.CTkFrame(
            card,
            fg_color=COLOR["bg_header"],
            corner_radius=12,
            height=130,
        )
        brand_block.pack(fill="x", padx=20, pady=(22, 0))
        brand_block.pack_propagate(False)

        ctk.CTkLabel(
            brand_block,
            text="⬡  INVENTECH",
            font=FONT["brand"],
            text_color=COLOR["text_white"],
        ).pack(pady=(28, 2))

        ctk.CTkLabel(
            brand_block,
            text="Sistema de Gestión de Inventario",
            font=FONT["label"],
            text_color=("#bfdbfe", "#bfdbfe"),
        ).pack()

        # ── Separador ──
        ctk.CTkFrame(card, fg_color=COLOR["border"], height=1).pack(
            fill="x", padx=20, pady=18
        )

        # ── Título de sección ──
        ctk.CTkLabel(
            card,
            text="Iniciar sesión",
            font=FONT["title"],
            text_color=COLOR["text_primary"],
        ).pack(anchor="w", padx=28)

        ctk.CTkLabel(
            card,
            text="Ingresa tus credenciales para continuar",
            font=FONT["body"],
            text_color=COLOR["text_secondary"],
        ).pack(anchor="w", padx=28, pady=(2, 18))

        # ── Campos ──
        ctk.CTkLabel(
            card, text="USUARIO", font=FONT["section"], text_color=COLOR["text_secondary"]
        ).pack(anchor="w", padx=28)

        self.usuario_entry = ctk.CTkEntry(
            card,
            placeholder_text="Nombre de usuario",
            width=320, height=40,
            font=FONT["subtitle"],
            border_color=COLOR["border"],
            corner_radius=8,
        )
        self.usuario_entry.pack(padx=28, pady=(4, 14))

        ctk.CTkLabel(
            card, text="CONTRASEÑA", font=FONT["section"], text_color=COLOR["text_secondary"]
        ).pack(anchor="w", padx=28)

        self.pass_entry = ctk.CTkEntry(
            card,
            placeholder_text="••••••••",
            show="•",
            width=320, height=40,
            font=FONT["subtitle"],
            border_color=COLOR["border"],
            corner_radius=8,
        )
        self.pass_entry.pack(padx=28, pady=(4, 22))
        self.pass_entry.bind("<Return>", lambda e: self.verificar_credenciales())

        # ── Botón principal ──
        self.btn_login = ctk.CTkButton(
            card,
            text="Entrar al sistema",
            width=320, height=44,
            font=FONT["nav"],
            fg_color=COLOR["primary"],
            hover_color=COLOR["primary_hover"],
            text_color=COLOR["text_white"],
            corner_radius=10,
            command=self.verificar_credenciales,
        )
        self.btn_login.pack(padx=28)

        # ── Footer ──
        ctk.CTkLabel(
            card,
            text="© 2026 Inventech  •  v3.0",
            font=FONT["small"],
            text_color=COLOR["text_secondary"],
        ).pack(pady=(20, 0))

    def verificar_credenciales(self):
        usuario  = self.usuario_entry.get()
        password = self.pass_entry.get()

        es_valido, rol, nombre_usuario = validar_login(usuario, password)

        if es_valido:
            self.withdraw()
            self.callback_exito(rol, nombre_usuario)
        else:
            self.pass_entry.configure(border_color=COLOR["danger"])
            self.after(1500, lambda: self.pass_entry.configure(border_color=COLOR["border"]))
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")


# ═══════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════
def cargar_ventana_principal(rol_usuario, nombre_real):
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Inventech — Sistema de Gestión")
    ventana.geometry("1180x740")
    ventana.minsize(960, 580)
    ventana.configure(fg_color=COLOR["bg_main"])

    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=0)
    ventana.grid_columnconfigure(1, weight=1)

    _construir_sidebar(ventana, rol_usuario, nombre_real)
    _construir_area_principal(ventana, rol_usuario, nombre_real)

    ventana.mainloop()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def _construir_sidebar(ventana, rol_usuario, nombre_real):
    sidebar = ctk.CTkFrame(
        ventana,
        fg_color=COLOR["bg_sidebar"],
        width=252,
        corner_radius=0,
        border_width=1,
        border_color=COLOR["border"],
    )
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)
    sidebar.grid_rowconfigure(2, weight=1)

    # ── Cabecera sidebar ──
    header = ctk.CTkFrame(
        sidebar,
        fg_color=COLOR["bg_header"],
        corner_radius=0,
        height=72,
    )
    header.grid(row=0, column=0, sticky="ew")
    header.grid_propagate(False)

    ctk.CTkLabel(
        header,
        text="⬡  INVENTECH",
        font=FONT["brand"],
        text_color=COLOR["text_white"],
    ).pack(expand=True)

    # ── Info de usuario ──
    user_frame = ctk.CTkFrame(
        sidebar,
        fg_color=COLOR["primary_light"],
        corner_radius=0,
        height=62,
    )
    user_frame.grid(row=1, column=0, sticky="ew")
    user_frame.grid_propagate(False)

    avatar = ctk.CTkLabel(
        user_frame,
        text=nombre_real[0].upper(),
        width=34, height=34,
        font=("Segoe UI", 13, "bold"),
        fg_color=COLOR["primary"],
        text_color=COLOR["text_white"],
        corner_radius=17,
    )
    avatar.pack(side="left", padx=(14, 8), pady=14)

    info_col = ctk.CTkFrame(user_frame, fg_color="transparent")
    info_col.pack(side="left", fill="y", pady=10)

    ctk.CTkLabel(
        info_col,
        text=nombre_real,
        font=FONT["body"],
        text_color=COLOR["text_primary"],
        anchor="w",
    ).pack(anchor="w")

    badge_color = COLOR["success"] if rol_usuario == "Admin" else COLOR["warning"]
    ctk.CTkLabel(
        info_col,
        text=f"● {rol_usuario}",
        font=FONT["small"],
        text_color=badge_color,
        anchor="w",
    ).pack(anchor="w")

    # ── Menú de navegación ──
    nav_frame = ctk.CTkScrollableFrame(
        sidebar,
        fg_color="transparent",
        scrollbar_button_color=COLOR["border"],
    )
    nav_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=8)

    def _boton_nav(parent, texto, comando):
        def _cmd_seguro():
            if rol_usuario == "Empleado" and (
                "eliminar" in texto.lower() or "borrar" in texto.lower()
            ):
                messagebox.showwarning(
                    "Sin permiso",
                    "Necesitas permisos de Administrador para eliminar registros.",
                )
            else:
                comando()

        btn = ctk.CTkButton(
            parent,
            text=texto,
            command=_cmd_seguro,
            height=34,
            font=FONT["body"],
            fg_color="transparent",
            hover_color=COLOR["sidebar_hover"],
            text_color=COLOR["text_primary"],
            anchor="w",
            corner_radius=7,
            border_width=0,
        )
        return btn

    def _seccion(parent, titulo, modulos):
        ctk.CTkLabel(
            parent,
            text=titulo.upper(),
            font=FONT["section"],
            text_color=COLOR["text_secondary"],
            anchor="w",
        ).pack(pady=(14, 3), padx=6, fill="x")

        for texto, handler in modulos:
            btn = _boton_nav(parent, f"  {texto}", lambda h=handler: h(ventana))
            btn.pack(pady=1, fill="x")

    for seccion, modulos in MODULOS_SIDEBAR:
        _seccion(nav_frame, seccion, modulos)

    # ── Separador ──
    ctk.CTkFrame(nav_frame, fg_color=COLOR["border"], height=1).pack(
        pady=12, fill="x"
    )

    # Botón Salir con color de peligro
    btn_salir = ctk.CTkButton(
        nav_frame,
        text="  ⏻  Cerrar sesión",
        command=ventana.quit,
        height=36,
        font=FONT["body"],
        fg_color="transparent",
        hover_color=("#fee2e2", "#3b1f1f"),
        text_color=COLOR["danger"],
        anchor="w",
        corner_radius=7,
    )
    btn_salir.pack(pady=2, fill="x")

    # ── Footer sidebar ──
    footer = ctk.CTkFrame(sidebar, fg_color="transparent", height=36)
    footer.grid(row=3, column=0, sticky="sew", padx=12, pady=6)

    ctk.CTkLabel(
        footer,
        text="v3.0  •  © 2026 Inventech",
        font=FONT["small"],
        text_color=COLOR["text_secondary"],
    ).pack()


# ─────────────────────────────────────────────
#  ÁREA PRINCIPAL
# ─────────────────────────────────────────────
def _construir_area_principal(ventana, rol_usuario, nombre_real):
    area = ctk.CTkFrame(ventana, fg_color=COLOR["bg_main"], corner_radius=0)
    area.grid(row=0, column=1, sticky="nsew")
    area.grid_rowconfigure(1, weight=1)
    area.grid_columnconfigure(0, weight=1)

    # ── Topbar ──
    topbar = ctk.CTkFrame(
        area,
        fg_color=COLOR["bg_card"],
        corner_radius=0,
        height=62,
        border_width=1,
        border_color=COLOR["border"],
    )
    topbar.grid(row=0, column=0, sticky="ew")
    topbar.grid_propagate(False)

    ctk.CTkLabel(
        topbar,
        text=f"Hola, {nombre_real} 👋",
        font=FONT["title"],
        text_color=COLOR["text_primary"],
    ).pack(side="left", padx=24, pady=16)

    badge = ctk.CTkLabel(
        topbar,
        text=f"  {rol_usuario}  ",
        font=FONT["small"],
        fg_color=COLOR["primary_light"],
        text_color=COLOR["primary"],
        corner_radius=6,
    )
    badge.pack(side="left", pady=20)

    # ── Contenido scrollable ──
    contenido = ctk.CTkScrollableFrame(
        area, fg_color="transparent",
        scrollbar_button_color=COLOR["border"],
    )
    contenido.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    _pantalla_bienvenida(contenido, rol_usuario)


def _pantalla_bienvenida(parent, rol_usuario):
    # Título
    ctk.CTkLabel(
        parent,
        text="Panel principal",
        font=FONT["brand"],
        text_color=COLOR["text_primary"],
    ).pack(anchor="w", pady=(0, 4))

    ctk.CTkLabel(
        parent,
        text="Resumen de módulos disponibles en el sistema.",
        font=FONT["body"],
        text_color=COLOR["text_secondary"],
    ).pack(anchor="w", pady=(0, 20))

    # Tarjetas de módulos
    modulos_info = [
        ("📂", "Catálogos",    "Categorías, ubicaciones y proveedores",         COLOR["primary"]),
        ("📦", "Inventario",   "Materiales, movimientos, alertas e historial",   ("#7c3aed", "#a78bfa")),
        ("🔄", "Operaciones",  "Compras, préstamos y mantenimientos",            ("#059669", "#34d399")),
        ("🔧", "Sistema",      "Usuarios, roles, reportes y auditoría",          ("#d97706", "#fbbf24")),
    ]

    grid = ctk.CTkFrame(parent, fg_color="transparent")
    grid.pack(fill="x", pady=(0, 20))
    grid.columnconfigure((0, 1), weight=1)

    for i, (icon, titulo, desc, color) in enumerate(modulos_info):
        card = ctk.CTkFrame(
            grid,
            fg_color=COLOR["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLOR["border"],
        )
        card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")

        accent = ctk.CTkFrame(card, fg_color=color, width=4, corner_radius=2)
        accent.pack(side="left", fill="y", padx=(0, 0), pady=16)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(side="left", fill="both", expand=True, padx=14, pady=16)

        ctk.CTkLabel(
            inner,
            text=f"{icon}  {titulo}",
            font=FONT["nav"],
            text_color=COLOR["text_primary"],
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner,
            text=desc,
            font=FONT["body"],
            text_color=COLOR["text_secondary"],
            anchor="w",
            wraplength=280,
        ).pack(anchor="w", pady=(2, 0))

    # Banner de rol
    if rol_usuario == "Admin":
        banner_color = ("#eff6ff", "#1e3a5f")
        banner_text  = "🛡️  Sesión con privilegios de Administrador — tienes acceso completo al sistema."
        text_color   = COLOR["primary"]
    else:
        banner_color = ("#fffbeb", "#3b2a05")
        banner_text  = "⚠️  Sesión como Empleado — algunas acciones están restringidas."
        text_color   = ("#b45309", "#fcd34d")

    banner = ctk.CTkFrame(
        parent,
        fg_color=banner_color,
        corner_radius=10,
        border_width=1,
        border_color=COLOR["border"],
    )
    banner.pack(fill="x", padx=0, pady=(8, 0))

    ctk.CTkLabel(
        banner,
        text=banner_text,
        font=FONT["body"],
        text_color=text_color,
        anchor="w",
    ).pack(padx=16, pady=12, anchor="w")


# ═══════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    login_app = VentanaLogin(callback_exito=cargar_ventana_principal)
    login_app.mainloop()


"""
Usuarios con Permisos de Admin:
    Usuario: Roberto Martínez
    Usuario: Ana Valladares

Usuarios con Permisos de Empleado:
    Usuario: Luis Caceres
    Usuario: Fernando Zelaya
    Usuario: Hector Salgado
    Usuario: techwithkevin
"""