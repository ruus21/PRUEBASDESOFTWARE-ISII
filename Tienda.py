"""Inventario en memoria y operaciones de la tienda."""

from math import isfinite
from numbers import Real


class ProductoNoEncontradoError(LookupError):
    """El nombre solicitado no se encuentra en el inventario."""


class Tienda:
    def __init__(self):
        self.inventario = []

    def agregar_producto(self, producto):
        self.inventario.append(producto)

    def buscar_producto(self, nombre):
        for producto in self.inventario:
            if producto.nombre == nombre:
                return producto
        raise ProductoNoEncontradoError(f"Producto no encontrado: {nombre}")

    def eliminar_producto(self, nombre):
        for producto in self.inventario:
            if producto.nombre == nombre:
                self.inventario.remove(producto)
                return True
        raise ProductoNoEncontradoError(f"Producto no encontrado: {nombre}")

    def aplicar_descuento(self, nombre, porcentaje):
        if isinstance(porcentaje, bool) or not isinstance(porcentaje, Real):
            raise TypeError("El porcentaje debe ser un número real")
        if not isfinite(porcentaje) or not 0 <= porcentaje <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100")
        producto = self.buscar_producto(nombre)
        nuevo_precio = producto.precio * (1 - porcentaje / 100)
        producto.actualizar_precio(nuevo_precio)

