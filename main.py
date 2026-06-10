import customtkinter as ctk
from tkinter import messagebox
from dbconexion import get_connection

ctk.set_appearance_mode("System")   # usa el modo claro/oscuro del sistema
ctk.set_default_color_theme("blue") # define el color principal

# ventana principal
ventana = ctk.CTk()
ventana.title("Inventech - Gestión de Materiales")
ventana.geometry("600x400")

# titulo dentro de la ventana
label = ctk.CTkLabel(ventana, text="Inventech - Gestion de Materiales", font=("Arial", 20))
label.pack(pady=20)

def ver_materiales():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cantidad, categoria FROM materiales")
        registros = cursor.fetchall()
        conn.close()

        if registros:
            texto = "\n".join([f"{nombre} - {cantidad} ({categoria})" for nombre, cantidad, categoria in registros])
            messagebox.showinfo("Materiales", texto)
        else:
            messagebox.showinfo("Materiales", "No hay registros en la tabla.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un problema: {e}")


# Boton para ver materiales
boton_ver = ctk.CTkButton(ventana, text="Ver materiales", command=ver_materiales)
boton_ver.pack(pady=10)


# Boton para agregar material
boton_agregar = ctk.CTkButton(ventana, text="Agregar material")
boton_agregar.pack(pady=10)

# Boton para eliminar material
boton_eliminar = ctk.CTkButton(ventana, text="Eliminar material")
boton_eliminar.pack(pady=10)

# mantiene la ventana abierta
ventana.mainloop()
