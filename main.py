import customtkinter as ctk
from tkinter import messagebox  
from modulos import MODULOS_SIDEBAR
from repositorio import validar_login  # Importamos la función que pusimos en repositorio.py

# ========================================================
# 1. ESTA ES LA VENTANA DE LOGIN
# ========================================================
class VentanaLogin(ctk.CTk):
    def __init__(self, callback_exito):
        super().__init__()
        self.callback_exito = callback_exito
        self.title("Inventech - Acceso")
        self.geometry("360x300")
        self.resizable(False, False)
        
        # Estilos rápidos del Login
        ctk.CTkLabel(self, text="INVENTECH", font=("Arial", 22, "bold"), text_color=("#2563eb", "#3b82f6")).pack(pady=(25, 5))
        ctk.CTkLabel(self, text="Control de Acceso", font=("Arial", 12), text_color=("#6b7280", "#9ca3af")).pack(pady=(0, 20))
        
        # Entrada de Usuario
        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Nombre de Usuario", width=260, height=35)
        self.usuario_entry.pack(pady=10)
        
        # Entrada de Contraseña
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Contraseña (12345)", show="*", width=260, height=35)
        self.pass_entry.pack(pady=10)
        
        # Botón
        ctk.CTkButton(self, text="Iniciar Sesión", width=260, height=38, font=("Arial", 12, "bold"),
                      fg_color=("#2563eb", "#1e40af"), hover_color=("#1d4ed8", "#1e3a8a"),
                      command=self.verificar_credenciales).pack(pady=25)

    def verificar_credenciales(self):
        usuario = self.usuario_entry.get()
        password = self.pass_entry.get()
        
        # Recibe los 3 valores desde repositorio.py
        es_valido, rol, nombre_usuario = validar_login(usuario, password)
        
        if es_valido:
            self.withdraw()  # Oculta la ventana de login sin romper la consola
            self.callback_exito(rol, nombre_usuario)  # Pasa ambos datos a la ventana principal
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")


# ========================================================
# 2. TU VENTANA PRINCIPAL ORIGINAL (Arreglada)
# ========================================================
# Ahora acepta correctamente rol_usuario Y nombre_real
def cargar_ventana_principal(rol_usuario, nombre_real):
    # Aquí configuramos los temas tal cual los tenías
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
    
    # EL SALUDO PERSONALIZADO QUE PEDISTE:
    saludo_texto = f"Hola {nombre_real}, bienvenido a Inventech — Rol: {rol_usuario}"
    ctk.CTkLabel(header_principal, text=saludo_texto, font=("Arial", 18, "bold")).pack(side="left", padx=15, pady=10)

    frame_contenido = ctk.CTkScrollableFrame(frame_principal, fg_color="transparent")
    frame_contenido.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

    def crear_boton_sidebar(parent, texto, comando):
        # NOTA DE SEGURIDAD: Si el rol es 'Empleado', bloqueamos si presionan un botón de Eliminar
        def comando_seguro():
            if rol_usuario == "Empleado" and ("eliminar" in texto.lower() or "borrar" in texto.lower()):
                messagebox.showwarning("Acceso Denegado", "No tienes permisos de Administrador para eliminar registros.")
            else:
                comando()

        return ctk.CTkButton(
            parent,
            text=texto,
            command=comando_seguro,
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

    ventana.mainloop()


# ========================================================
# 3. EJECUCIÓN INICIAL DEL PROGRAMA
# ========================================================
if __name__ == "__main__":
    # Arranca el Login pasando la nueva función con dos parámetros
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