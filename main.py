import customtkinter as ctk
from tkinter import messagebox
from dbconexion import get_connection
from PIL import Image

# "Aqui funciona el CRUD, solo falta Update"

ctk.set_appearance_mode("System")   # usa el modo claro/oscuro del sistema
ctk.set_default_color_theme("blue") # define el color principal

# ventana principal
ventana = ctk.CTk()
fondo = ctk.CTkImage(Image.open("logotkinter.jpg"), size=(600,400))
label_fondo = ctk.CTkLabel(ventana, image=fondo, text="")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

ventana.title("Inventech - Gestión de Materiales")
ventana.geometry("600x400")

# titulo dentro de la ventana
label = ctk.CTkLabel(ventana, text="Inventech - Gestion de Materiales", font=("Arial", 20))
label.pack(pady=20)

def ver_materiales():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT NombreMaterial, Cantidad, IDCategoría FROM Materiales""")

        registros = cursor.fetchall()
        conn.close()

        if registros:
            texto = "\n".join([f"{nombre} - {cantidad} ({categoria})" for nombre, cantidad, categoria in registros])
            messagebox.showinfo("Materiales", texto)
        else:
            messagebox.showinfo("Materiales", "No hay registros en la tabla.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un problema: {e}")
        
#agregar materialesg
        
def agregar_material():
    form = ctk.CTkToplevel(ventana)
    form.lift()
    form.focus_force()
    form.title("Agregar Material")
    form.geometry("300x300")

    # Campos
    ctk.CTkLabel(form, text="Nombre:").pack(pady=5)
    entry_nombre = ctk.CTkEntry(form); entry_nombre.pack(pady=5)

    ctk.CTkLabel(form, text="Cantidad:").pack(pady=5)
    entry_cantidad = ctk.CTkEntry(form); entry_cantidad.pack(pady=5)

    ctk.CTkLabel(form, text="ID Categoría:").pack(pady=5)
    entry_categoria = ctk.CTkEntry(form); entry_categoria.pack(pady=5)

    ctk.CTkLabel(form, text="ID Ubicación:").pack(pady=5)
    entry_ubicacion = ctk.CTkEntry(form); entry_ubicacion.pack(pady=5)

    ctk.CTkLabel(form, text="Fecha ingreso (YYYY-MM-DD):").pack(pady=5)
    entry_fecha = ctk.CTkEntry(form); entry_fecha.pack(pady=5)

    # Función interna para guardar
    def guardar():
        nombre = entry_nombre.get()
        cantidad = entry_cantidad.get()
        categoria = entry_categoria.get()
        ubicacion = entry_ubicacion.get()
        fecha = entry_fecha.get()

        if not nombre or not cantidad or not categoria or not ubicacion or not fecha:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Materiales (NombreMaterial, Cantidad, IDCategoría, IDUbicación, FechaIngreso) VALUES (%s, %s, %s, %s, %s)",
                (nombre, cantidad, categoria, ubicacion, fecha)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Material agregado correctamente.")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")
            
    ctk.CTkButton(form, text="Guardar", command=guardar).pack(pady=10)
    

def eliminar_material():
    form = ctk.CTkToplevel(ventana)
    form.title("Eliminar Material")
    form.geometry("300x150")
    form.lift(); form.focus_force()

    ctk.CTkLabel(form, text="Digite el ID del material a borrar:").pack(pady=10)
    entry_id = ctk.CTkEntry(form); entry_id.pack(pady=5)
    
    def borrar():
        if not (id_material := entry_id.get()):
            messagebox.showwarning("Campo vacio", "Ingrese el ID."); return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Materiales WHERE IDMaterial = %s", (id_material,))
            conn.commit(); conn.close()
            messagebox.showinfo( "Material eliminado."); form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")

    ctk.CTkButton(form, text="Borrar", command=borrar).pack(pady=10)



# Boton para ver materiales
boton_ver = ctk.CTkButton(ventana, text="Ver materiales", command=ver_materiales)
boton_ver.pack(pady=10)


# Boton para agregar material
boton_agregar = ctk.CTkButton(ventana, text="Agregar material", command=agregar_material)
boton_agregar.pack(pady=10)

# Boton para eliminar material
boton_eliminar = ctk.CTkButton(ventana, text="Eliminar material", command=eliminar_material)
boton_eliminar.pack(pady=10)

# mantiene la ventana abierta
ventana.mainloop()
