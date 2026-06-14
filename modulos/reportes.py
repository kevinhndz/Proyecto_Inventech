from ui_helpers import ventana_lista
import repositorio as repo


def reporte_inventario(parent):
    filas = repo.listar_estado_inventario()
    ventana_lista(
        parent, "Estado del Inventario",
        "ID | Material | Cantidad | Categoría | Ubicación | Precio | Valor | Estado",
        filas, "1000x500",
    )


def reporte_compras_pendientes(parent):
    filas = repo.listar_compras_pendientes()
    ventana_lista(parent, "Compras Pendientes", "ID | Proveedor | Fecha | Total | Artículos", filas, "750x400")


def reporte_prestamos_activos(parent):
    filas = repo.listar_prestamos_activos()
    ventana_lista(parent, "Préstamos Activos", "ID | Usuario | Fecha | Artículos | Estado | Descripción", filas, "850x400")


def reporte_auditoria(parent):
    filas = repo.listar_auditoria()
    ventana_lista(
        parent, "Auditoría",
        "ID | Operación | Tabla | Registro | Usuario | Descripción | Fecha",
        filas, "1000x500",
    )


MODULOS_REPORTES = [
    (" Estado Inventario", reporte_inventario),
    (" Compras Pendientes", reporte_compras_pendientes),
    (" Préstamos Activos", reporte_prestamos_activos),
    (" Auditoría", reporte_auditoria),
]
