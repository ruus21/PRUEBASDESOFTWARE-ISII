"""Producto del TP 1: Valla, Pablo Gastón y Zamorano, Ruth Ayelen."""

from math import isfinite
from numbers import Real


class Producto:
    """Producto con precio numérico finito y no negativo."""

    def __init__(self, nombre, precio, categoria):
        self.nombre = nombre
        self.categoria = categoria
        self.actualizar_precio(precio)

    def actualizar_precio(self, nuevo_precio):
        if isinstance(nuevo_precio, bool) or not isinstance(nuevo_precio, Real):
            raise TypeError("El precio debe ser un número real")
        if not isfinite(nuevo_precio) or nuevo_precio < 0:
            raise ValueError("El precio debe ser finito y no negativo")
        self.precio = nuevo_precio
