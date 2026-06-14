import customtkinter as ctk

from modulos import MODULOS_SIDEBAR

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Inventech - Sistema de Gestión")
ventana.geometry("1100x720")
ventana.minsize(900, 550)

ventana.grid_rowconfigure(0, weight=1)
ventana.grid_columnconfigure(0, weight=0)
ventana.grid_columnconfigure(1, weight=1)

# ========== SIDEBAR ==========
sidebar = ctk.CTkFrame(ventana, fg_color=("#f0f0f0", "#1a1a1a"), width=240)
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)
sidebar.grid_rowconfigure(1, weight=1)

header_sidebar = ctk.CTkFrame(sidebar, fg_color=("#2563eb", "#1e40af"), height=90)
header_sidebar.grid(row=0, column=0, sticky="ew")
header_sidebar.grid_propagate(False)
ctk.CTkLabel(header_sidebar, text="INVENTECH", font=("Arial", 16, "bold"), text_color="white").pack(pady=20)

botones_sidebar = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
botones_sidebar.grid(row=1, column=0, sticky="nsew", padx=8, pady=10)

# ========== ÁREA PRINCIPAL ==========
frame_principal = ctk.CTkFrame(ventana)
frame_principal.grid(row=0, column=1, sticky="nsew")
frame_principal.grid_rowconfigure(1, weight=1)
frame_principal.grid_columnconfigure(0, weight=1)

header_principal = ctk.CTkFrame(frame_principal, fg_color=("#e8f0ff", "#0f172a"), height=80)
header_principal.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
header_principal.grid_propagate(False)
ctk.CTkLabel(header_principal, text="Sistema de Gestión de Inventario", font=("Arial", 22, "bold")).pack(side="left", padx=10, pady=10)

frame_contenido = ctk.CTkScrollableFrame(frame_principal, fg_color="transparent")
frame_contenido.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)


def crear_boton_sidebar(parent, texto, comando):
    return ctk.CTkButton(
        parent,
        text=texto,
        command=comando,
        height=38,
        font=("Arial", 10, "bold"),
        fg_color=("#3b82f6", "#1e40af"),
        hover_color=("#2563eb", "#1e3a8a"),
        text_color="white",
        corner_radius=8,
        anchor="w",
    )


def crear_seccion(parent, titulo, modulos):
    ctk.CTkLabel(
        parent,
        text=titulo.upper(),
        font=("Arial", 9, "bold"),
        text_color=("#6b7280", "#9ca3af"),
        anchor="w",
    ).pack(pady=(12, 4), padx=4, fill="x")

    for texto, handler in modulos:
        btn = crear_boton_sidebar(parent, texto, lambda h=handler: h(ventana))
        btn.pack(pady=3, fill="x")


for seccion, modulos in MODULOS_SIDEBAR:
    crear_seccion(botones_sidebar, seccion, modulos)

ctk.CTkFrame(botones_sidebar, fg_color=("#d1d5db", "#374151"), height=2).pack(pady=12, fill="x")
crear_boton_sidebar(botones_sidebar, "Salir", ventana.quit).pack(pady=4, fill="x")

footer_sidebar = ctk.CTkFrame(sidebar, fg_color="transparent", height=60)
footer_sidebar.grid(row=2, column=0, sticky="sew", padx=10, pady=8)
ctk.CTkLabel(footer_sidebar, text="v3.0 - Todos los módulos", font=("Arial", 8), text_color=("#6b7280", "#9ca3af")).pack()
ctk.CTkLabel(footer_sidebar, text="© 2026 Inventech", font=("Arial", 8), text_color=("#6b7280", "#9ca3af")).pack()

# ========== PANTALLA DE BIENVENIDA ==========
frame_welcome = ctk.CTkFrame(frame_contenido, fg_color="transparent")
frame_welcome.pack(fill="both", expand=True, padx=10, pady=20)

ctk.CTkLabel(
    frame_welcome,
    text="Bienvenido a Inventech",
    font=("Arial", 20, "bold"),
).pack(pady=(10, 5))

ctk.CTkLabel(
    frame_welcome,
    text="Gestión integral de inventario, compras, préstamos y mantenimientos.",
    font=("Arial", 12),
    text_color=("#6b7280", "#9ca3af"),
).pack(pady=5)

modulos_info = [
    ("Catálogos", "Categorías, ubicaciones y proveedores"),
    ("Inventario", "Materiales, movimientos, alertas e historial"),
    ("Operaciones", "Compras, préstamos y mantenimientos"),
    ("Sistema", "Usuarios, roles, reportes y auditoría"),
]

frame_cards = ctk.CTkFrame(frame_welcome, fg_color=("#f3f4f6", "#1f2937"), corner_radius=10)
frame_cards.pack(pady=25, padx=10, fill="both")

for titulo, desc in modulos_info:
    row = ctk.CTkFrame(frame_cards, fg_color="transparent")
    row.pack(pady=10, padx=15, fill="x")
    ctk.CTkLabel(row, text=titulo, font=("Arial", 11, "bold"), width=120, anchor="w").pack(side="left")
    ctk.CTkLabel(row, text=desc, font=("Arial", 10), text_color=("#6b7280", "#9ca3af"), anchor="w").pack(side="left", padx=10)

if __name__ == "__main__":
    ventana.mainloop()
