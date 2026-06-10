import customtkinter as ctk

ctk.set_appearance_mode("System")   # ssa el modo claro/oscuro del sistema
ctk.set_default_color_theme("blue") # define el color principal

# este pedazo de codigo crea la ventana principal

ventana = ctk.CTk()    # esto crea la ventana
ventana.title("Inventech - Gestión de Materiales")
ventana.geometry("600x400")       

# esto lo que hace es agrega un titulo dentro de la ventana
label = ctk.CTkLabel(ventana, text="Bienvenido a Inventech", font=("Arial", 20))
label.pack(pady=20)               

# creacion de boton
boton = ctk.CTkButton(ventana, text="Probar conexión a MySQL")
boton.pack(pady=10)

# mantiene la ventana abierta
ventana.mainloop()
