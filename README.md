# Inventech - Sistema de Gestión de Materiales

**Inventech** es una aplicación de escritorio robusta en Python para gestionar materiales con una interfaz gráfica moderna (CustomTkinter) y conexión a base de datos MySQL.

## 🎯 Características Principales

- ✅ **CRUD Completo**: Create, Read, Update, Delete
- ✅ **Interfaz Moderna**: CustomTkinter con tema adaptable
- ✅ **Validaciones Robustas**: Datos numéricos, fechas y nombres
- ✅ **Conexión MySQL**: Integración segura con base de datos
- ✅ **Confirmaciones de Seguridad**: Previene eliminaciones accidentales
- ✅ **Manejo de Errores**: Excepciones controladas y mensajes claros
- ✅ **Búsqueda y Visualización**: Tabla con scroll para ver todos los materiales

## 📁 Estructura de Archivos

```
Proyecto_Inventech/
│
├── main.py                 # Aplicación principal con interfaz gráfica
├── dbconexion.py           # Módulo de conexión y validaciones
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (NO commitar)
├── README.md              # Este archivo
└── logotkinter.jpg        # Imagen de fondo (opcional)
```

### Descripción de Archivos

| Archivo | Descripción |
|---------|------------|
| `main.py` | Interfaz gráfica CRUD completa con validaciones |
| `dbconexion.py` | Funciones de conexión y validadores de datos |
| `requirements.txt` | Librerías necesarias para ejecutar el proyecto |
| `.env` | Credenciales de base de datos (local, no versionado) |

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd Proyecto_Inventech
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```ini
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_basedatos
```

### 5. Ejecutar la aplicación
```bash
python main.py
```

## 📋 Dependencias

- **customtkinter** (≥5.2.0) - Interfaz gráfica moderna
- **mysql-connector-python** (≥8.0.33) - Conexión a MySQL
- **Pillow** (≥10.0.0) - Procesamiento de imágenes
- **python-dotenv** (≥1.0.0) - Variables de entorno

## 🎨 Operaciones CRUD

### 1. Ver Materiales (READ)
- Muestra lista completa de materiales
- Visualiza: ID, Nombre, Cantidad, Categoría, Ubicación, Fecha

### 2. Agregar Material (CREATE)
- Campos: Nombre, Cantidad, ID Categoría, ID Ubicación, Fecha
- Validaciones automáticas
- Confirmación de éxito

### 3. Actualizar Material (UPDATE)
- Selecciona material por ID
- Actualiza solo los campos necesarios
- Campos opcionales: nombre, cantidad, categoría, ubicación, fecha

### 4. Eliminar Material (DELETE)
- Selecciona por ID
- Pide confirmación antes de eliminar
- Previene pérdida accidental de datos

## ✅ Validaciones Implementadas

| Campo | Validación |
|-------|-----------|
| **Nombre** | No vacío, máximo 100 caracteres |
| **Cantidad** | Número entero positivo |
| **ID Categoría** | Número entero positivo |
| **ID Ubicación** | Número entero positivo |
| **Fecha** | Formato YYYY-MM-DD |

## 🔐 Configuración de Base de Datos

### Instalación de Base de Datos

La base de datos completa incluye **15 tablas** con relaciones complejas:

**Opción 1: Automática (Recomendado)**
```bash
python crear_bd.py
```

**Opción 2: Manual**
1. Abre MySQL Workbench o cliente MySQL
2. Carga el archivo `schema.sql`
3. Ejecuta el script

**Opción 3: Línea de comandos**
```bash
mysql -u root -p < schema.sql
```

Ver [INSTALACION_BD.md](INSTALACION_BD.md) para instrucciones detalladas.

### Tablas de la Base de Datos

| Tabla | Descripción |
|-------|------------|
| **Usuarios** | Gestión de usuarios del sistema |
| **RolesUsuarios** | Roles (Admin, Docente, Alumno) |
| **Materiales** | Inventario principal |
| **Categorías** | Clasificación de materiales |
| **Ubicaciones** | Lugares de almacenamiento |
| **Proveedores** | Información de proveedores |
| **MovimientosInventario** | Historial de entradas/salidas |
| **AlertasStock** | Alertas de bajo inventario |
| **HistorialInventario** | Registro de cambios |
| **Compras** | Pedidos realizados |
| **DetalleCompras** | Artículos por compra |
| **Préstamos** | Gestión de préstamos |
| **DetallePréstamos** | Detalle de préstamos |
| **Mantenimientos** | Registros de mantenimiento |
| **InventarioInicial** | Estado inicial |
