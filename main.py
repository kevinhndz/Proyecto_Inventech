import customtkinter as ctk

ctk.set_appearance_mode("System")   # usa el modo claro/oscuro del sistema
ctk.set_default_color_theme("blue") # define el color principal

# ventana principal
ventana = ctk.CTk()
ventana.title("Inventech - Gestión de Materiales")
ventana.geometry("600x400")

# titulo dentro de la ventana
label = ctk.CTkLabel(ventana, text="Inventech - Gestion de Materiales", font=("Arial", 20))
label.pack(pady=20)

# Boton para ver materiales
boton_ver = ctk.CTkButton(ventana, text="Ver materiales")
boton_ver.pack(pady=10)

# Boton para agregar material
boton_agregar = ctk.CTkButton(ventana, text="Agregar material")
boton_agregar.pack(pady=10)

# Boton para eliminar material
boton_eliminar = ctk.CTkButton(ventana, text="Eliminar material")
boton_eliminar.pack(pady=10)

# mantiene la ventana abierta
ventana.mainloop()
