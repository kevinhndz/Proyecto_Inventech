-- ============================================
-- BASE DE DATOS: INVENTECH (SQLite)
-- Sistema de Gestión de Materiales
-- ============================================

PRAGMA foreign_keys = ON;

-- ========== CATÁLOGOS ==========

CREATE TABLE IF NOT EXISTS RolesUsuarios (
    IDRol INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreRol TEXT NOT NULL UNIQUE CHECK (NombreRol IN ('Alumno', 'Docente', 'Admin')),
    Descripcion TEXT,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Usuarios (
    IDUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreUsuario TEXT NOT NULL,
    IDRol INTEGER NOT NULL,
    Correo TEXT NOT NULL UNIQUE,
    Contraseña TEXT,
    Activo BOOLEAN DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDRol) REFERENCES RolesUsuarios(IDRol) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Categorias (
    IDCategoría INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreCategoría TEXT NOT NULL UNIQUE,
    Descripción TEXT,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Ubicaciones (
    IDUbicación INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreUbicación TEXT NOT NULL UNIQUE,
    Responsable TEXT,
    Descripción TEXT,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Proveedores (
    IDProveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreProveedor TEXT NOT NULL UNIQUE,
    Teléfono TEXT,
    Dirección TEXT,
    Correo TEXT,
    Activo BOOLEAN DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ========== INVENTARIO ==========

CREATE TABLE IF NOT EXISTS Materiales (
    IDMaterial INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreMaterial TEXT NOT NULL UNIQUE,
    Cantidad INTEGER NOT NULL DEFAULT 0,
    IDCategoría INTEGER NOT NULL,
    IDUbicación INTEGER NOT NULL,
    FechaIngreso DATE NOT NULL,
    Descripción TEXT,
    PrecioUnitario REAL DEFAULT 0,
    Activo BOOLEAN DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDCategoría) REFERENCES Categorias(IDCategoría),
    FOREIGN KEY (IDUbicación) REFERENCES Ubicaciones(IDUbicación),
    CHECK (Cantidad >= 0),
    CHECK (PrecioUnitario >= 0)
);

CREATE TABLE IF NOT EXISTS AlertasStock (
    IDAlerta INTEGER PRIMARY KEY AUTOINCREMENT,
    IDMaterial INTEGER NOT NULL UNIQUE,
    CantidadActual INTEGER NOT NULL,
    NivelMinimo INTEGER DEFAULT 5,
    EstadoAlerta TEXT CHECK(EstadoAlerta IN ('Normal', 'Bajo', 'Agotado')) DEFAULT 'Normal',
    FechaAlerta DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS HistorialInventario (
    IDHistorial INTEGER PRIMARY KEY AUTOINCREMENT,
    IDMaterial INTEGER NOT NULL,
    FechaCambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    CantidadAnterior INTEGER NOT NULL,
    CantidadNueva INTEGER NOT NULL,
    UsuarioResponsable TEXT,
    Motivo TEXT,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MovimientosInventario (
    IDMovimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    IDMaterial INTEGER NOT NULL,
    TipoMovimiento TEXT CHECK(TipoMovimiento IN ('Entrada', 'Salida')) NOT NULL,
    Cantidad INTEGER NOT NULL,
    Motivo TEXT,
    FechaMovimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    UsuarioResponsable TEXT,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial) ON DELETE CASCADE,
    CHECK (Cantidad > 0)
);

CREATE TABLE IF NOT EXISTS InventarioInicial (
    IDInventarioInicial INTEGER PRIMARY KEY AUTOINCREMENT,
    IDMaterial INTEGER NOT NULL UNIQUE,
    CantidadInicial INTEGER NOT NULL,
    FechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial) ON DELETE CASCADE,
    CHECK (CantidadInicial >= 0)
);

-- ========== COMPRAS ==========

CREATE TABLE IF NOT EXISTS Compras (
    IDCompra INTEGER PRIMARY KEY AUTOINCREMENT,
    FechaCompra DATETIME DEFAULT CURRENT_TIMESTAMP,
    IDProveedor INTEGER NOT NULL,
    Total REAL DEFAULT 0,
    Estado TEXT CHECK(Estado IN ('Pendiente', 'Completada', 'Cancelada')) DEFAULT 'Pendiente',
    Descripción TEXT,
    UsuarioResponsable TEXT,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDProveedor) REFERENCES Proveedores(IDProveedor)
);

CREATE TABLE IF NOT EXISTS DetalleCompras (
    IDDetalleCompra INTEGER PRIMARY KEY AUTOINCREMENT,
    IDCompra INTEGER NOT NULL,
    IDMaterial INTEGER NOT NULL,
    Cantidad INTEGER NOT NULL,
    PrecioUnitario REAL NOT NULL,
    Subtotal REAL GENERATED ALWAYS AS (Cantidad * PrecioUnitario) STORED,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDCompra) REFERENCES Compras(IDCompra) ON DELETE CASCADE,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial),
    CHECK (Cantidad > 0),
    CHECK (PrecioUnitario >= 0)
);

-- ========== PRÉSTAMOS ==========

CREATE TABLE IF NOT EXISTS Prestamos (
    IDPrestamo INTEGER PRIMARY KEY AUTOINCREMENT,
    FechaPrestamo DATETIME DEFAULT CURRENT_TIMESTAMP,
    NombreUsuario TEXT NOT NULL,
    Estado TEXT CHECK(Estado IN ('Pendiente', 'Devuelto', 'Cancelado')) DEFAULT 'Pendiente',
    Descripción TEXT,
    Responsable TEXT,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DetallePrestamos (
    IDDetallePrestamo INTEGER PRIMARY KEY AUTOINCREMENT,
    IDPrestamo INTEGER NOT NULL,
    IDMaterial INTEGER NOT NULL,
    Cantidad INTEGER NOT NULL,
    FechaDevolución DATE,
    DevueltoCompletamente BOOLEAN DEFAULT 0,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDPrestamo) REFERENCES Prestamos(IDPrestamo) ON DELETE CASCADE,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial),
    CHECK (Cantidad > 0)
);

-- ========== MANTENIMIENTOS Y AUDITORÍA ==========

CREATE TABLE IF NOT EXISTS Mantenimientos (
    IDMantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    IDMaterial INTEGER NOT NULL,
    FechaMantenimiento DATETIME NOT NULL,
    Descripción TEXT,
    Costo REAL DEFAULT 0,
    TécnicoResponsable TEXT,
    ProximoMantenimiento DATE,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDMaterial) REFERENCES Materiales(IDMaterial) ON DELETE CASCADE,
    CHECK (Costo >= 0)
);

CREATE TABLE IF NOT EXISTS AuditLog (
    IDAudit INTEGER PRIMARY KEY AUTOINCREMENT,
    TipoOperación TEXT NOT NULL,
    NombreTabla TEXT NOT NULL,
    IDRegistro INTEGER,
    UsuarioResponsable TEXT,
    DescripcionCambio TEXT,
    FechaOperación DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ========== ÍNDICES ==========

CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON Usuarios(IDRol);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON Usuarios(Activo);
CREATE INDEX IF NOT EXISTS idx_materiales_categoria ON Materiales(IDCategoría);
CREATE INDEX IF NOT EXISTS idx_materiales_ubicacion ON Materiales(IDUbicación);
CREATE INDEX IF NOT EXISTS idx_materiales_activo ON Materiales(Activo);
CREATE INDEX IF NOT EXISTS idx_alertas_material ON AlertasStock(IDMaterial);
CREATE INDEX IF NOT EXISTS idx_movimientos_material ON MovimientosInventario(IDMaterial);
CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON MovimientosInventario(FechaMovimiento);
CREATE INDEX IF NOT EXISTS idx_compras_proveedor ON Compras(IDProveedor);
CREATE INDEX IF NOT EXISTS idx_compras_estado ON Compras(Estado);
CREATE INDEX IF NOT EXISTS idx_detallecompras_compra ON DetalleCompras(IDCompra);
CREATE INDEX IF NOT EXISTS idx_prestamos_usuario ON Prestamos(NombreUsuario);
CREATE INDEX IF NOT EXISTS idx_prestamos_estado ON Prestamos(Estado);
CREATE INDEX IF NOT EXISTS idx_detalleprestamos_prestamo ON DetallePrestamos(IDPrestamo);
CREATE INDEX IF NOT EXISTS idx_mantenimientos_material ON Mantenimientos(IDMaterial);
CREATE INDEX IF NOT EXISTS idx_auditlog_tabla ON AuditLog(NombreTabla);
CREATE INDEX IF NOT EXISTS idx_auditlog_fecha ON AuditLog(FechaOperación);
CREATE INDEX IF NOT EXISTS idx_historial_material ON HistorialInventario(IDMaterial);
CREATE INDEX IF NOT EXISTS idx_historial_fecha ON HistorialInventario(FechaCambio);

-- ========== DATOS INICIALES ==========

INSERT OR IGNORE INTO RolesUsuarios (NombreRol, Descripcion) VALUES
('Admin', 'Administrador del sistema'),
('Docente', 'Profesor o instructor'),
('Alumno', 'Estudiante del programa');

INSERT OR IGNORE INTO Usuarios (NombreUsuario, IDRol, Correo) VALUES
('Administrador', 1, 'admin@inventech.local');

INSERT OR IGNORE INTO Categorias (NombreCategoría, Descripción) VALUES
('Electrónica', 'Componentes electrónicos'),
('Herramientas', 'Herramientas de trabajo'),
('Seguridad', 'Equipos de protección personal'),
('Consumibles', 'Materiales consumibles'),
('Equipo Pesado', 'Maquinaria y equipo');

INSERT OR IGNORE INTO Ubicaciones (NombreUbicación, Responsable) VALUES
('Almacén Principal', 'Juan Pérez'),
('Laboratorio A', 'María García'),
('Laboratorio B', 'Carlos López'),
('Taller', 'Roberto Díaz'),
('Oficina', 'Laura Martínez');

INSERT OR IGNORE INTO Proveedores (NombreProveedor, Teléfono, Dirección, Correo) VALUES
('ElectroMart', '+34-91-234-5678', 'Calle Principal 123', 'info@electromart.es'),
('TechSupply', '+34-93-987-6543', 'Av. Diagonal 456', 'sales@techsupply.es'),
('ToolPro', '+34-96-555-4321', 'Plaza Central 789', 'contact@toolpro.es');

-- ========== VISTAS ==========

CREATE VIEW IF NOT EXISTS v_estado_inventario AS
SELECT
    m.IDMaterial,
    m.NombreMaterial,
    m.Cantidad,
    c.NombreCategoría,
    u.NombreUbicación,
    m.PrecioUnitario,
    (m.Cantidad * m.PrecioUnitario) AS ValorTotal,
    CASE
        WHEN a.EstadoAlerta = 'Agotado' THEN 'Agotado'
        WHEN a.EstadoAlerta = 'Bajo' THEN 'Bajo Stock'
        ELSE 'Normal'
    END AS EstadoStock
FROM Materiales m
LEFT JOIN Categorias c ON m.IDCategoría = c.IDCategoría
LEFT JOIN Ubicaciones u ON m.IDUbicación = u.IDUbicación
LEFT JOIN AlertasStock a ON m.IDMaterial = a.IDMaterial
WHERE m.Activo = 1
ORDER BY m.NombreMaterial;

CREATE VIEW IF NOT EXISTS v_movimientos_recientes AS
SELECT
    mi.IDMovimiento,
    datetime(mi.FechaMovimiento, 'localtime') AS Fecha,
    m.NombreMaterial,
    mi.TipoMovimiento,
    mi.Cantidad,
    mi.Motivo,
    mi.UsuarioResponsable
FROM MovimientosInventario mi
LEFT JOIN Materiales m ON mi.IDMaterial = m.IDMaterial
ORDER BY mi.FechaMovimiento DESC
LIMIT 50;

CREATE VIEW IF NOT EXISTS v_compras_pendientes AS
SELECT
    c.IDCompra,
    p.NombreProveedor,
    date(c.FechaCompra) AS Fecha,
    c.Total,
    COUNT(dc.IDDetalleCompra) AS CantidadArticulos
FROM Compras c
LEFT JOIN Proveedores p ON c.IDProveedor = p.IDProveedor
LEFT JOIN DetalleCompras dc ON c.IDCompra = dc.IDCompra
WHERE c.Estado = 'Pendiente'
GROUP BY c.IDCompra
ORDER BY c.FechaCompra DESC;

CREATE VIEW IF NOT EXISTS v_prestamos_activos AS
SELECT
    p.IDPrestamo,
    p.NombreUsuario,
    date(p.FechaPrestamo) AS Fecha,
    COUNT(dp.IDDetallePrestamo) AS ArticulosPrestados,
    p.Estado,
    p.Descripción
FROM Prestamos p
LEFT JOIN DetallePrestamos dp ON p.IDPrestamo = dp.IDPrestamo
WHERE p.Estado = 'Pendiente'
GROUP BY p.IDPrestamo
ORDER BY p.FechaPrestamo DESC;
