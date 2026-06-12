"""Capa de acceso a datos para todos los módulos de Inventech."""

from dbconexion import get_connection


def _ejecutar(query, params=(), fetch=False, fetchone=False, commit=False):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        if fetch:
            return cursor.fetchall()
        if commit:
            conn.commit()
            return cursor.rowcount
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid is not None else cursor.rowcount
    finally:
        conn.close()


def registrar_auditoria(tipo, tabla, id_registro, usuario, descripcion):
    _ejecutar(
        """INSERT INTO AuditLog (TipoOperación, NombreTabla, IDRegistro, UsuarioResponsable, DescripcionCambio)
           VALUES (?, ?, ?, ?, ?)""",
        (tipo, tabla, id_registro, usuario, descripcion),
        commit=True,
    )


def _actualizar_alerta_stock(id_material, cantidad):
    alerta = _ejecutar(
        "SELECT NivelMinimo FROM AlertasStock WHERE IDMaterial = ?",
        (id_material,),
        fetchone=True,
    )
    nivel = alerta[0] if alerta else 5
    if cantidad <= 0:
        estado = "Agotado"
    elif cantidad <= nivel:
        estado = "Bajo"
    else:
        estado = "Normal"

    if alerta:
        _ejecutar(
            """UPDATE AlertasStock SET CantidadActual = ?, EstadoAlerta = ?, FechaAlerta = CURRENT_TIMESTAMP
               WHERE IDMaterial = ?""",
            (cantidad, estado, id_material),
            commit=True,
        )
    else:
        _ejecutar(
            """INSERT INTO AlertasStock (IDMaterial, CantidadActual, NivelMinimo, EstadoAlerta)
               VALUES (?, ?, ?, ?)""",
            (id_material, cantidad, nivel, estado),
            commit=True,
        )


def _registrar_historial(id_material, anterior, nueva, usuario, motivo):
    _ejecutar(
        """INSERT INTO HistorialInventario (IDMaterial, CantidadAnterior, CantidadNueva, UsuarioResponsable, Motivo)
           VALUES (?, ?, ?, ?, ?)""",
        (id_material, anterior, nueva, usuario, motivo),
        commit=True,
    )


def ajustar_cantidad_material(id_material, delta, usuario="Sistema", motivo="Ajuste de inventario"):
    row = _ejecutar("SELECT Cantidad FROM Materiales WHERE IDMaterial = ?", (id_material,), fetchone=True)
    if not row:
        raise ValueError("Material no encontrado")
    anterior, nueva = row[0], row[0] + delta
    if nueva < 0:
        raise ValueError("Stock insuficiente")
    _ejecutar(
        "UPDATE Materiales SET Cantidad = ?, FechaActualizacion = CURRENT_TIMESTAMP WHERE IDMaterial = ?",
        (nueva, id_material),
        commit=True,
    )
    _registrar_historial(id_material, anterior, nueva, usuario, motivo)
    _actualizar_alerta_stock(id_material, nueva)
    return nueva


# ---------- ROLES Y USUARIOS ----------

def listar_roles():
    return _ejecutar("SELECT IDRol, NombreRol, Descripcion FROM RolesUsuarios ORDER BY IDRol", fetch=True)


def listar_usuarios():
    return _ejecutar(
        """SELECT u.IDUsuario, u.NombreUsuario, r.NombreRol, u.Correo, u.Activo
           FROM Usuarios u JOIN RolesUsuarios r ON u.IDRol = r.IDRol ORDER BY u.IDUsuario""",
        fetch=True,
    )


def crear_usuario(nombre, id_rol, correo):
    rid = _ejecutar(
        "INSERT INTO Usuarios (NombreUsuario, IDRol, Correo) VALUES (?, ?, ?)",
        (nombre, id_rol, correo),
    )
    registrar_auditoria("INSERT", "Usuarios", rid, "Sistema", f"Usuario creado: {nombre}")
    return rid


def eliminar_usuario(id_usuario):
    n = _ejecutar("DELETE FROM Usuarios WHERE IDUsuario = ?", (id_usuario,), commit=True)
    if n:
        registrar_auditoria("DELETE", "Usuarios", id_usuario, "Sistema", "Usuario eliminado")
    return n


# ---------- CATÁLOGOS ----------

def listar_categorias():
    return _ejecutar("SELECT IDCategoría, NombreCategoría, Descripción FROM Categorias ORDER BY IDCategoría", fetch=True)


def crear_categoria(nombre, descripcion=""):
    rid = _ejecutar(
        "INSERT INTO Categorias (NombreCategoría, Descripción) VALUES (?, ?)",
        (nombre, descripcion),
    )
    registrar_auditoria("INSERT", "Categorias", rid, "Sistema", nombre)
    return rid


def actualizar_categoria(id_cat, nombre, descripcion):
    n = _ejecutar(
        "UPDATE Categorias SET NombreCategoría = ?, Descripción = ? WHERE IDCategoría = ?",
        (nombre, descripcion, id_cat),
        commit=True,
    )
    if n:
        registrar_auditoria("UPDATE", "Categorias", id_cat, "Sistema", nombre)
    return n


def eliminar_categoria(id_cat):
    n = _ejecutar("DELETE FROM Categorias WHERE IDCategoría = ?", (id_cat,), commit=True)
    if n:
        registrar_auditoria("DELETE", "Categorias", id_cat, "Sistema", "Categoría eliminada")
    return n


def listar_ubicaciones():
    return _ejecutar(
        "SELECT IDUbicación, NombreUbicación, Responsable, Descripción FROM Ubicaciones ORDER BY IDUbicación",
        fetch=True,
    )


def crear_ubicacion(nombre, responsable="", descripcion=""):
    rid = _ejecutar(
        "INSERT INTO Ubicaciones (NombreUbicación, Responsable, Descripción) VALUES (?, ?, ?)",
        (nombre, responsable, descripcion),
    )
    registrar_auditoria("INSERT", "Ubicaciones", rid, "Sistema", nombre)
    return rid


def actualizar_ubicacion(id_ubi, nombre, responsable, descripcion):
    n = _ejecutar(
        "UPDATE Ubicaciones SET NombreUbicación = ?, Responsable = ?, Descripción = ? WHERE IDUbicación = ?",
        (nombre, responsable, descripcion, id_ubi),
        commit=True,
    )
    if n:
        registrar_auditoria("UPDATE", "Ubicaciones", id_ubi, "Sistema", nombre)
    return n


def eliminar_ubicacion(id_ubi):
    n = _ejecutar("DELETE FROM Ubicaciones WHERE IDUbicación = ?", (id_ubi,), commit=True)
    if n:
        registrar_auditoria("DELETE", "Ubicaciones", id_ubi, "Sistema", "Ubicación eliminada")
    return n


def listar_proveedores():
    return _ejecutar(
        "SELECT IDProveedor, NombreProveedor, Teléfono, Dirección, Correo, Activo FROM Proveedores ORDER BY IDProveedor",
        fetch=True,
    )


def crear_proveedor(nombre, telefono="", direccion="", correo=""):
    rid = _ejecutar(
        "INSERT INTO Proveedores (NombreProveedor, Teléfono, Dirección, Correo) VALUES (?, ?, ?, ?)",
        (nombre, telefono, direccion, correo),
    )
    registrar_auditoria("INSERT", "Proveedores", rid, "Sistema", nombre)
    return rid


def actualizar_proveedor(id_prov, nombre, telefono, direccion, correo):
    n = _ejecutar(
        """UPDATE Proveedores SET NombreProveedor = ?, Teléfono = ?, Dirección = ?, Correo = ?
           WHERE IDProveedor = ?""",
        (nombre, telefono, direccion, correo, id_prov),
        commit=True,
    )
    if n:
        registrar_auditoria("UPDATE", "Proveedores", id_prov, "Sistema", nombre)
    return n


def eliminar_proveedor(id_prov):
    n = _ejecutar("DELETE FROM Proveedores WHERE IDProveedor = ?", (id_prov,), commit=True)
    if n:
        registrar_auditoria("DELETE", "Proveedores", id_prov, "Sistema", "Proveedor eliminado")
    return n


# ---------- MATERIALES ----------

def listar_materiales():
    return _ejecutar(
        """SELECT m.IDMaterial, m.NombreMaterial, m.Cantidad, c.NombreCategoría, u.NombreUbicación, m.FechaIngreso
           FROM Materiales m
           JOIN Categorias c ON m.IDCategoría = c.IDCategoría
           JOIN Ubicaciones u ON m.IDUbicación = u.IDUbicación
           ORDER BY m.IDMaterial""",
        fetch=True,
    )


def listar_materiales_opciones():
    return _ejecutar("SELECT IDMaterial, NombreMaterial, Cantidad FROM Materiales WHERE Activo = 1 ORDER BY NombreMaterial", fetch=True)


def crear_material(nombre, cantidad, id_categoria, id_ubicacion, fecha, descripcion="", precio=0):
    rid = _ejecutar(
        """INSERT INTO Materiales (NombreMaterial, Cantidad, IDCategoría, IDUbicación, FechaIngreso, Descripción, PrecioUnitario)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (nombre, cantidad, id_categoria, id_ubicacion, fecha, descripcion, precio),
    )
    _actualizar_alerta_stock(rid, cantidad)
    registrar_auditoria("INSERT", "Materiales", rid, "Sistema", nombre)
    return rid


def actualizar_material(id_material, datos):
    campos_map = {
        "nombre": "NombreMaterial",
        "cantidad": "Cantidad",
        "categoria": "IDCategoría",
        "ubicacion": "IDUbicación",
        "fecha": "FechaIngreso",
        "descripcion": "Descripción",
        "precio": "PrecioUnitario",
    }
    set_parts, valores = [], []
    for key, col in campos_map.items():
        if key in datos:
            set_parts.append(f"{col} = ?")
            valores.append(datos[key])
    if not set_parts:
        return 0
    set_parts.append("FechaActualizacion = CURRENT_TIMESTAMP")
    valores.append(id_material)
    n = _ejecutar(
        f"UPDATE Materiales SET {', '.join(set_parts)} WHERE IDMaterial = ?",
        tuple(valores),
        commit=True,
    )
    if n and "cantidad" in datos:
        _actualizar_alerta_stock(id_material, datos["cantidad"])
    if n:
        registrar_auditoria("UPDATE", "Materiales", id_material, "Sistema", str(datos))
    return n


def eliminar_material(id_material):
    n = _ejecutar("DELETE FROM Materiales WHERE IDMaterial = ?", (id_material,), commit=True)
    if n:
        registrar_auditoria("DELETE", "Materiales", id_material, "Sistema", "Material eliminado")
    return n


# ---------- MOVIMIENTOS Y ALERTAS ----------

def listar_movimientos():
    return _ejecutar("SELECT * FROM v_movimientos_recientes", fetch=True)


def registrar_movimiento(id_material, tipo, cantidad, motivo="", usuario="Sistema"):
    delta = cantidad if tipo == "Entrada" else -cantidad
    ajustar_cantidad_material(id_material, delta, usuario, motivo or f"Movimiento {tipo}")
    rid = _ejecutar(
        """INSERT INTO MovimientosInventario (IDMaterial, TipoMovimiento, Cantidad, Motivo, UsuarioResponsable)
           VALUES (?, ?, ?, ?, ?)""",
        (id_material, tipo, cantidad, motivo, usuario),
    )
    registrar_auditoria("INSERT", "MovimientosInventario", rid, usuario, f"{tipo} x{cantidad}")
    return rid


def listar_alertas():
    return _ejecutar(
        """SELECT a.IDAlerta, m.NombreMaterial, a.CantidadActual, a.NivelMinimo, a.EstadoAlerta, a.FechaAlerta
           FROM AlertasStock a JOIN Materiales m ON a.IDMaterial = m.IDMaterial
           ORDER BY a.EstadoAlerta DESC, m.NombreMaterial""",
        fetch=True,
    )


def configurar_alerta(id_material, nivel_minimo):
    mat = _ejecutar("SELECT Cantidad FROM Materiales WHERE IDMaterial = ?", (id_material,), fetchone=True)
    if not mat:
        raise ValueError("Material no encontrado")
    existe = _ejecutar("SELECT IDAlerta FROM AlertasStock WHERE IDMaterial = ?", (id_material,), fetchone=True)
    if existe:
        _ejecutar(
            "UPDATE AlertasStock SET NivelMinimo = ? WHERE IDMaterial = ?",
            (nivel_minimo, id_material),
            commit=True,
        )
    else:
        _ejecutar(
            "INSERT INTO AlertasStock (IDMaterial, CantidadActual, NivelMinimo) VALUES (?, ?, ?)",
            (id_material, mat[0], nivel_minimo),
            commit=True,
        )
    _actualizar_alerta_stock(id_material, mat[0])


def listar_historial():
    return _ejecutar(
        """SELECT h.IDHistorial, m.NombreMaterial, h.CantidadAnterior, h.CantidadNueva,
                  h.UsuarioResponsable, h.Motivo, h.FechaCambio
           FROM HistorialInventario h JOIN Materiales m ON h.IDMaterial = m.IDMaterial
           ORDER BY h.FechaCambio DESC LIMIT 100""",
        fetch=True,
    )


def listar_inventario_inicial():
    return _ejecutar(
        """SELECT i.IDInventarioInicial, m.NombreMaterial, i.CantidadInicial, i.FechaRegistro
           FROM InventarioInicial i JOIN Materiales m ON i.IDMaterial = m.IDMaterial
           ORDER BY i.FechaRegistro DESC""",
        fetch=True,
    )


def registrar_inventario_inicial(id_material, cantidad):
    existe = _ejecutar("SELECT IDInventarioInicial FROM InventarioInicial WHERE IDMaterial = ?", (id_material,), fetchone=True)
    if existe:
        raise ValueError("Este material ya tiene inventario inicial registrado")
    rid = _ejecutar(
        "INSERT INTO InventarioInicial (IDMaterial, CantidadInicial) VALUES (?, ?)",
        (id_material, cantidad),
    )
    registrar_auditoria("INSERT", "InventarioInicial", rid, "Sistema", f"Material {id_material}")
    return rid


# ---------- COMPRAS ----------

def listar_compras():
    return _ejecutar(
        """SELECT c.IDCompra, p.NombreProveedor, c.FechaCompra, c.Total, c.Estado, c.Descripción
           FROM Compras c JOIN Proveedores p ON c.IDProveedor = p.IDProveedor
           ORDER BY c.IDCompra DESC""",
        fetch=True,
    )


def listar_detalle_compras(id_compra=None):
    query = """SELECT d.IDDetalleCompra, d.IDCompra, m.NombreMaterial, d.Cantidad, d.PrecioUnitario, d.Subtotal
               FROM DetalleCompras d JOIN Materiales m ON d.IDMaterial = m.IDMaterial"""
    if id_compra:
        return _ejecutar(query + " WHERE d.IDCompra = ? ORDER BY d.IDDetalleCompra", (id_compra,), fetch=True)
    return _ejecutar(query + " ORDER BY d.IDCompra DESC, d.IDDetalleCompra", fetch=True)


def crear_compra(id_proveedor, descripcion="", usuario="Sistema"):
    rid = _ejecutar(
        "INSERT INTO Compras (IDProveedor, Descripción, UsuarioResponsable) VALUES (?, ?, ?)",
        (id_proveedor, descripcion, usuario),
    )
    registrar_auditoria("INSERT", "Compras", rid, usuario, descripcion)
    return rid


def agregar_detalle_compra(id_compra, id_material, cantidad, precio):
    rid = _ejecutar(
        "INSERT INTO DetalleCompras (IDCompra, IDMaterial, Cantidad, PrecioUnitario) VALUES (?, ?, ?, ?)",
        (id_compra, id_material, cantidad, precio),
    )
    _ejecutar(
        "UPDATE Compras SET Total = (SELECT COALESCE(SUM(Subtotal), 0) FROM DetalleCompras WHERE IDCompra = ?) WHERE IDCompra = ?",
        (id_compra, id_compra),
        commit=True,
    )
    return rid


def completar_compra(id_compra, usuario="Sistema"):
    compra = _ejecutar("SELECT Estado FROM Compras WHERE IDCompra = ?", (id_compra,), fetchone=True)
    if not compra:
        raise ValueError("Compra no encontrada")
    if compra[0] != "Pendiente":
        raise ValueError("La compra ya fue procesada")
    detalles = _ejecutar(
        "SELECT IDMaterial, Cantidad FROM DetalleCompras WHERE IDCompra = ?",
        (id_compra,),
        fetch=True,
    )
    if not detalles:
        raise ValueError("La compra no tiene artículos")
    for id_mat, cant in detalles:
        registrar_movimiento(id_mat, "Entrada", cant, f"Compra #{id_compra}", usuario)
    _ejecutar("UPDATE Compras SET Estado = 'Completada' WHERE IDCompra = ?", (id_compra,), commit=True)
    registrar_auditoria("UPDATE", "Compras", id_compra, usuario, "Compra completada")


# ---------- PRÉSTAMOS ----------

def listar_prestamos():
    return _ejecutar(
        "SELECT IDPrestamo, NombreUsuario, FechaPrestamo, Estado, Descripción, Responsable FROM Prestamos ORDER BY IDPrestamo DESC",
        fetch=True,
    )


def listar_detalle_prestamos(id_prestamo=None):
    query = """SELECT d.IDDetallePrestamo, d.IDPrestamo, m.NombreMaterial, d.Cantidad,
                      d.FechaDevolución, d.DevueltoCompletamente
               FROM DetallePrestamos d JOIN Materiales m ON d.IDMaterial = m.IDMaterial"""
    if id_prestamo:
        return _ejecutar(query + " WHERE d.IDPrestamo = ? ORDER BY d.IDDetallePrestamo", (id_prestamo,), fetch=True)
    return _ejecutar(query + " ORDER BY d.IDPrestamo DESC", fetch=True)


def crear_prestamo(nombre_usuario, descripcion="", responsable=""):
    rid = _ejecutar(
        "INSERT INTO Prestamos (NombreUsuario, Descripción, Responsable) VALUES (?, ?, ?)",
        (nombre_usuario, descripcion, responsable),
    )
    registrar_auditoria("INSERT", "Prestamos", rid, responsable or "Sistema", nombre_usuario)
    return rid


def agregar_detalle_prestamo(id_prestamo, id_material, cantidad, usuario="Sistema"):
    rid = _ejecutar(
        "INSERT INTO DetallePrestamos (IDPrestamo, IDMaterial, Cantidad) VALUES (?, ?, ?)",
        (id_prestamo, id_material, cantidad),
    )
    registrar_movimiento(id_material, "Salida", cantidad, f"Préstamo #{id_prestamo}", usuario)
    return rid


def devolver_prestamo(id_prestamo, usuario="Sistema"):
    prestamo = _ejecutar("SELECT Estado FROM Prestamos WHERE IDPrestamo = ?", (id_prestamo,), fetchone=True)
    if not prestamo:
        raise ValueError("Préstamo no encontrado")
    if prestamo[0] != "Pendiente":
        raise ValueError("El préstamo ya fue devuelto o cancelado")
    detalles = _ejecutar(
        "SELECT IDMaterial, Cantidad FROM DetallePrestamos WHERE IDPrestamo = ? AND DevueltoCompletamente = 0",
        (id_prestamo,),
        fetch=True,
    )
    if not detalles:
        raise ValueError("No hay artículos pendientes de devolución")
    for id_mat, cant in detalles:
        registrar_movimiento(id_mat, "Entrada", cant, f"Devolución préstamo #{id_prestamo}", usuario)
    _ejecutar(
        "UPDATE DetallePrestamos SET DevueltoCompletamente = 1, FechaDevolución = date('now') WHERE IDPrestamo = ?",
        (id_prestamo,),
        commit=True,
    )
    _ejecutar("UPDATE Prestamos SET Estado = 'Devuelto' WHERE IDPrestamo = ?", (id_prestamo,), commit=True)
    registrar_auditoria("UPDATE", "Prestamos", id_prestamo, usuario, "Préstamo devuelto")


# ---------- MANTENIMIENTOS ----------

def listar_mantenimientos():
    return _ejecutar(
        """SELECT mn.IDMantenimiento, m.NombreMaterial, mn.FechaMantenimiento, mn.Descripción,
                  mn.Costo, mn.TécnicoResponsable, mn.ProximoMantenimiento
           FROM Mantenimientos mn JOIN Materiales m ON mn.IDMaterial = m.IDMaterial
           ORDER BY mn.FechaMantenimiento DESC""",
        fetch=True,
    )


def crear_mantenimiento(id_material, fecha, descripcion="", costo=0, tecnico="", proximo=""):
    rid = _ejecutar(
        """INSERT INTO Mantenimientos (IDMaterial, FechaMantenimiento, Descripción, Costo, TécnicoResponsable, ProximoMantenimiento)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (id_material, fecha, descripcion, costo, tecnico, proximo or None),
    )
    registrar_auditoria("INSERT", "Mantenimientos", rid, tecnico or "Sistema", descripcion)
    return rid


def eliminar_mantenimiento(id_mant):
    n = _ejecutar("DELETE FROM Mantenimientos WHERE IDMantenimiento = ?", (id_mant,), commit=True)
    if n:
        registrar_auditoria("DELETE", "Mantenimientos", id_mant, "Sistema", "Mantenimiento eliminado")
    return n


# ---------- REPORTES Y AUDITORÍA ----------

def listar_estado_inventario():
    return _ejecutar("SELECT * FROM v_estado_inventario", fetch=True)


def listar_compras_pendientes():
    return _ejecutar("SELECT * FROM v_compras_pendientes", fetch=True)


def listar_prestamos_activos():
    return _ejecutar("SELECT * FROM v_prestamos_activos", fetch=True)


def listar_auditoria():
    return _ejecutar(
        """SELECT IDAudit, TipoOperación, NombreTabla, IDRegistro, UsuarioResponsable,
                  DescripcionCambio, FechaOperación FROM AuditLog ORDER BY FechaOperación DESC LIMIT 200""",
        fetch=True,
    )
