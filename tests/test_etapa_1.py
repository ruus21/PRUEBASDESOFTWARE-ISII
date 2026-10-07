import pytest
from etapa_1.producto import Producto
from etapa_1.tienda import Tienda

def test_atributos_producto_base():
    producto = Producto('Arroz', 1000, 'Alimentos')
    assert (producto.nombre, producto.precio, producto.categoria) == ('Arroz', 1000, 'Alimentos')

def test_tienda_base_vacia():
    assert Tienda().inventario == []

def test_agregar_base():
    tienda_base = Tienda()
    tienda_base.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    tienda_base.agregar_producto(Producto('Leche', 1500, 'Alimentos'))
    producto = Producto('Jabon', 800, 'Limpieza')
    tienda_base.agregar_producto(producto)
    assert tienda_base.inventario[-1] is producto
    assert len(tienda_base.inventario) == 3

@pytest.mark.parametrize('nombre', ['Arroz', 'Leche'])
def test_buscar_base(nombre):
    tienda_base = Tienda()
    tienda_base.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    tienda_base.agregar_producto(Producto('Leche', 1500, 'Alimentos'))
    assert tienda_base.buscar_producto(nombre).nombre == nombre

@pytest.mark.parametrize('vacia', [True, False])
def test_buscar_base_inexistente(vacia):
    tienda_base = Tienda()
    tienda_base.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    tienda_base.agregar_producto(Producto('Leche', 1500, 'Alimentos'))
    tienda = Tienda() if vacia else tienda_base
    assert tienda.buscar_producto('Inexistente') is None

@pytest.mark.parametrize('nombre,restante', [('Arroz', 'Leche'), ('Leche', 'Arroz')])
def test_eliminar_base(nombre, restante):
    tienda_base = Tienda()
    tienda_base.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    tienda_base.agregar_producto(Producto('Leche', 1500, 'Alimentos'))
    assert tienda_base.eliminar_producto(nombre) is True
    assert [p.nombre for p in tienda_base.inventario] == [restante]

@pytest.mark.parametrize('vacia', [True, False])
def test_eliminar_base_inexistente(vacia):
    tienda_base = Tienda()
    tienda_base.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    tienda_base.agregar_producto(Producto('Leche', 1500, 'Alimentos'))
    tienda = Tienda() if vacia else tienda_base
    antes = list(tienda.inventario)
    assert tienda.eliminar_producto('Inexistente') is False
    assert tienda.inventario == antes
