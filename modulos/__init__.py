from modulos.catalogos import MODULOS_CATALOGOS
from modulos.materiales import MODULOS_MATERIALES
from modulos.inventario import MODULOS_INVENTARIO
from modulos.compras import MODULOS_COMPRAS
from modulos.prestamos import MODULOS_PRESTAMOS
from modulos.mantenimientos import MODULOS_MANTENIMIENTOS
from modulos.usuarios import MODULOS_USUARIOS
from modulos.reportes import MODULOS_REPORTES

MODULOS_SIDEBAR = [
    ("Catálogos", MODULOS_CATALOGOS),
    ("Inventario", MODULOS_MATERIALES + MODULOS_INVENTARIO),
    ("Operaciones", MODULOS_COMPRAS + MODULOS_PRESTAMOS + MODULOS_MANTENIMIENTOS),
    ("Sistema", MODULOS_USUARIOS + MODULOS_REPORTES),
]
