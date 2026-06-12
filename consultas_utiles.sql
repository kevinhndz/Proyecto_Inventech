-- ============================================
-- EJEMPLOS DE CONSULTAS ÚTILES - INVENTECH
-- ============================================

USE inventech_db;

-- ============================================
-- 1. CONSULTAS DE INVENTARIO
-- ============================================

-- Ver estado actual del inventario
SELECT * FROM v_estado_inventario;

-- Materiales con bajo stock
SELECT 
    m.NombreMaterial,
    m.Cantidad,
    a.NivelMinimo,
    a.EstadoAlerta,
    u.NombreUbicación
FROM AlertasStock a
LEFT JOIN Materiales m ON a.IDMaterial = m.IDMaterial
LEFT JOIN Ubicaciones u ON m.IDUbicación = u.IDUbicación
WHERE a.EstadoAlerta IN ('Bajo', 'Agotado')
ORDER BY a.EstadoAlerta DESC;

-- Valor total del inventario por categoría
SELECT 
    c.NombreCategoría,
    COUNT(m.IDMaterial) as 'Total Artículos',
    SUM(m.Cantidad) as 'Cantidad Total',
    SUM(m.Cantidad * m.PrecioUnitario) as 'Valor Total'
FROM Materiales m
LEFT JOIN Categorias c ON m.IDCategoría = c.IDCategoría
WHERE m.Activo = TRUE
GROUP BY c.NombreCategoría
ORDER BY 'Valor Total' DESC;

-- ============================================
-- 2. CONSULTAS DE MOVIMIENTOS
-- ============================================

-- Ver últimos movimientos
SELECT * FROM v_movimientos_recientes;

-- Movimientos por material (últimos 30 días)
SELECT 
    m.NombreMaterial,
    SUM(CASE WHEN TipoMovimiento = 'Entrada' THEN Cantidad ELSE 0 END) as Entradas,
    SUM(CASE WHEN TipoMovimiento = 'Salida' THEN Cantidad ELSE 0 END) as Salidas,
    COUNT(*) as 'Total Movimientos'
FROM MovimientosInventario mi
LEFT JOIN Materiales m ON mi.IDMaterial = m.IDMaterial
WHERE mi.FechaMovimiento >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY mi.IDMaterial
ORDER BY 'Total Movimientos' DESC;

-- ============================================
-- 3. CONSULTAS DE COMPRAS
-- ============================================

-- Ver compras pendientes
SELECT * FROM v_compras_pendientes;

-- Compras completadas por proveedor
SELECT 
    p.NombreProveedor,
    COUNT(c.IDCompra) as 'Total Compras',
    SUM(c.Total) as 'Monto Total',
    AVG(c.Total) as 'Promedio por Compra'
FROM Compras c
LEFT JOIN Proveedores p ON c.IDProveedor = p.IDProveedor
WHERE c.Estado = 'Completada'
GROUP BY p.NombreProveedor
ORDER BY 'Monto Total' DESC;

-- Detalle de compras con artículos
SELECT 
    c.IDCompra,
    p.NombreProveedor,
    m.NombreMaterial,
    dc.Cantidad,
    dc.PrecioUnitario,
    dc.Subtotal,
    DATE_FORMAT(c.FechaCompra, '%d/%m/%Y') as Fecha
FROM Compras c
LEFT JOIN Proveedores p ON c.IDProveedor = p.IDProveedor
LEFT JOIN DetalleCompras dc ON c.IDCompra = dc.IDCompra
LEFT JOIN Materiales m ON dc.IDMaterial = m.IDMaterial
WHERE c.Estado = 'Completada'
ORDER BY c.FechaCompra DESC
LIMIT 100;

-- ============================================
-- 4. CONSULTAS DE PRÉSTAMOS
-- ============================================

-- Ver préstamos activos
SELECT * FROM v_prestamos_activos;

-- Préstamos no devueltos
SELECT 
    p.IDPrestamo,
    u.NombreUsuario,
    m.NombreMaterial,
    dp.Cantidad,
    DATE_FORMAT(p.FechaPrestamo, '%d/%m/%Y') as 'Fecha Préstamo',
    DATEDIFF(NOW(), p.FechaPrestamo) as 'Días desde Préstamo'
FROM Prestamos p
LEFT JOIN Usuarios u ON p.IDUsuario = u.IDUsuario
LEFT JOIN DetallePrestamos dp ON p.IDPrestamo = dp.IDPrestamo
LEFT JOIN Materiales m ON dp.IDMaterial = m.IDMaterial
WHERE p.Estado = 'Pendiente'
ORDER BY p.FechaPrestamo ASC;

-- Préstamos por usuario
SELECT 
    u.NombreUsuario,
    COUNT(p.IDPrestamo) as 'Total Préstamos',
    COUNT(CASE WHEN p.Estado = 'Pendiente' THEN 1 END) as 'Pendientes',
    COUNT(CASE WHEN p.Estado = 'Devuelto' THEN 1 END) as 'Devueltos'
FROM Prestamos p
LEFT JOIN Usuarios u ON p.IDUsuario = u.IDUsuario
GROUP BY u.NombreUsuario
ORDER BY 'Total Préstamos' DESC;

-- ============================================
-- 5. CONSULTAS DE MANTENIMIENTO
-- ============================================

-- Próximos mantenimientos
SELECT 
    m.NombreMaterial,
    mt.FechaMantenimiento,
    mt.Descripción,
    mt.Costo,
    mt.TécnicoResponsable,
    mt.ProximoMantenimiento,
    DATEDIFF(mt.ProximoMantenimiento, NOW()) as 'Días para Mantenimiento'
FROM Mantenimientos mt
LEFT JOIN Materiales m ON mt.IDMaterial = m.IDMaterial
WHERE mt.ProximoMantenimiento >= DATE_SUB(NOW(), INTERVAL 7 DAY)
  AND mt.ProximoMantenimiento <= DATE_ADD(NOW(), INTERVAL 30 DAY)
ORDER BY mt.ProximoMantenimiento ASC;

-- Costo total de mantenimientos (últimos 6 meses)
SELECT 
    m.NombreMaterial,
    COUNT(mt.IDMantenimiento) as 'Total Servicios',
    SUM(mt.Costo) as 'Costo Total',
    AVG(mt.Costo) as 'Costo Promedio'
FROM Mantenimientos mt
LEFT JOIN Materiales m ON mt.IDMaterial = m.IDMaterial
WHERE mt.FechaMantenimiento >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY mt.IDMaterial
ORDER BY 'Costo Total' DESC;

-- ============================================
-- 6. CONSULTAS DE USUARIOS Y AUDITORÍA
-- ============================================

-- Usuarios activos por rol
SELECT 
    r.NombreRol,
    COUNT(u.IDUsuario) as 'Total Usuarios'
FROM Usuarios u
LEFT JOIN RolesUsuarios r ON u.IDRol = r.IDRol
WHERE u.Activo = TRUE
GROUP BY r.NombreRol;

-- Historial reciente de cambios (Auditoría)
SELECT 
    TipoOperación,
    NombreTabla,
    UsuarioResponsable,
    DATE_FORMAT(FechaOperación, '%d/%m/%Y %H:%i:%s') as Fecha,
    DescripcionCambio
FROM AuditLog
ORDER BY FechaOperación DESC
LIMIT 50;

-- ============================================
-- 7. REPORTES GERENCIALES
-- ============================================

-- Resumen general del inventario
SELECT 
    COUNT(DISTINCT m.IDMaterial) as 'Total Artículos',
    SUM(m.Cantidad) as 'Cantidad Total',
    SUM(m.Cantidad * m.PrecioUnitario) as 'Valor Total Inventario',
    COUNT(DISTINCT c.IDCompra) as 'Total Compras',
    SUM(c.Total) as 'Monto Total Compras',
    COUNT(DISTINCT p.IDPrestamo) as 'Total Préstamos',
    COUNT(DISTINCT mt.IDMantenimiento) as 'Total Mantenimientos'
FROM Materiales m
LEFT JOIN Compras c ON 1=1
LEFT JOIN Prestamos p ON 1=1
LEFT JOIN Mantenimientos mt ON 1=1;

-- ROI por proveedor (compra vs mantenimiento)
SELECT 
    pr.NombreProveedor,
    SUM(c.Total) as 'Total Invertido',
    SUM(mt.Costo) as 'Costo Mantenimiento',
    (SUM(c.Total) + SUM(mt.Costo)) as 'Costo Total',
    COUNT(DISTINCT dc.IDMaterial) as 'Artículos'
FROM Proveedores pr
LEFT JOIN Compras c ON pr.IDProveedor = c.IDProveedor
LEFT JOIN DetalleCompras dc ON c.IDCompra = dc.IDCompra
LEFT JOIN Materiales m ON dc.IDMaterial = m.IDMaterial
LEFT JOIN Mantenimientos mt ON m.IDMaterial = mt.IDMaterial
GROUP BY pr.IDProveedor
ORDER BY 'Costo Total' DESC;

-- ============================================
-- 8. CONSULTAS DE BÚSQUEDA
-- ============================================

-- Buscar material por nombre
SELECT * FROM Materiales 
WHERE NombreMaterial LIKE '%tuerca%'
AND Activo = TRUE;

-- Materiales por categoría específica
SELECT 
    m.NombreMaterial,
    m.Cantidad,
    m.PrecioUnitario,
    u.NombreUbicación
FROM Materiales m
LEFT JOIN Ubicaciones u ON m.IDUbicación = u.IDUbicación
WHERE m.IDCategoría = 1
AND m.Activo = TRUE
ORDER BY m.NombreMaterial;

-- Materiales en una ubicación específica
SELECT 
    m.NombreMaterial,
    m.Cantidad,
    c.NombreCategoría,
    m.PrecioUnitario * m.Cantidad as 'Valor Total'
FROM Materiales m
LEFT JOIN Categorias c ON m.IDCategoría = c.IDCategoría
LEFT JOIN Ubicaciones u ON m.IDUbicación = u.IDUbicación
WHERE u.NombreUbicación = 'Almacén Principal'
AND m.Activo = TRUE
ORDER BY m.Cantidad DESC;

-- ============================================
-- 9. ANÁLISIS TEMPORAL
-- ============================================

-- Movimientos por mes (últimos 6 meses)
SELECT 
    DATE_FORMAT(FechaMovimiento, '%Y-%m') as Mes,
    TipoMovimiento,
    SUM(Cantidad) as 'Cantidad Total',
    COUNT(*) as 'Total Movimientos'
FROM MovimientosInventario
WHERE FechaMovimiento >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY DATE_FORMAT(FechaMovimiento, '%Y-%m'), TipoMovimiento
ORDER BY Mes DESC;

-- Compras por mes (últimos 12 meses)
SELECT 
    DATE_FORMAT(FechaCompra, '%Y-%m') as Mes,
    COUNT(*) as 'Compras',
    SUM(Total) as 'Monto Total',
    AVG(Total) as 'Promedio'
FROM Compras
WHERE FechaCompra >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(FechaCompra, '%Y-%m')
ORDER BY Mes DESC;

-- ============================================
-- 10. ALERTAS Y NOTIFICACIONES
-- ============================================

-- Materiales que necesitan reorden
SELECT 
    m.NombreMaterial,
    m.Cantidad,
    a.NivelMinimo,
    (a.NivelMinimo - m.Cantidad) as 'Cantidad Faltante',
    m.PrecioUnitario,
    ((a.NivelMinimo - m.Cantidad) * m.PrecioUnitario) as 'Inversión Necesaria'
FROM AlertasStock a
LEFT JOIN Materiales m ON a.IDMaterial = m.IDMaterial
WHERE a.EstadoAlerta IN ('Bajo', 'Agotado')
ORDER BY 'Inversión Necesaria' DESC;

-- Materiales sin movimiento en 90 días
SELECT 
    m.NombreMaterial,
    m.Cantidad,
    m.Cantidad * m.PrecioUnitario as 'Valor Invertido',
    MAX(mi.FechaMovimiento) as 'Último Movimiento',
    DATEDIFF(NOW(), MAX(mi.FechaMovimiento)) as 'Días sin Movimiento'
FROM Materiales m
LEFT JOIN MovimientosInventario mi ON m.IDMaterial = mi.IDMaterial
GROUP BY m.IDMaterial
HAVING 'Días sin Movimiento' >= 90 OR MAX(mi.FechaMovimiento) IS NULL
ORDER BY 'Días sin Movimiento' DESC;

-- ============================================
-- FIN DEL SCRIPT DE CONSULTAS
-- ============================================
