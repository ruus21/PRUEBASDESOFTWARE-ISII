from unittest.mock import Mock
from producto import Producto
import pytest
from tienda import ProductoNoEncontradoError, Tienda

def test_inventarios_independientes():
    una, otra = (Tienda(), Tienda())
    assert una.inventario == otra.inventario == []
    assert una.inventario is not otra.inventario

@pytest.mark.parametrize('metodo', ['buscar_producto', 'eliminar_producto'])
@pytest.mark.parametrize('vacia', [True, False])
def test_inexistente_lanza_excepcion(metodo, vacia):
    tienda_aislada = Tienda()
    tienda_aislada.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    tienda = Tienda() if vacia else tienda_aislada
    antes = list(tienda.inventario)
    with pytest.raises(ProductoNoEncontradoError, match='Inexistente'):
        getattr(tienda, metodo)('Inexistente')
    assert tienda.inventario == antes

@pytest.mark.parametrize('porcentaje,esperado', [(0, 1000), (0.01, 999.9), (20, 800), (99.99, 0.1), (100, 0)])
def test_descuento_con_mock(porcentaje, esperado):
    producto_doble = Mock(spec=Producto)
    producto_doble.nombre = 'Arroz'
    producto_doble.precio = 1000
    tienda_aislada = Tienda()
    tienda_aislada.agregar_producto(producto_doble)
    tienda_aislada.aplicar_descuento('Arroz', porcentaje)
    producto_doble.actualizar_precio.assert_called_once_with(pytest.approx(esperado))

@pytest.mark.parametrize('porcentaje', [-0.01, 100.01, float('nan'), float('inf')])
def test_descuento_fuera_de_rango(porcentaje):
    producto_doble = Mock(spec=Producto)
    producto_doble.nombre = 'Arroz'
    producto_doble.precio = 1000
    tienda_aislada = Tienda()
    tienda_aislada.agregar_producto(producto_doble)
    with pytest.raises(ValueError, match='entre 0 y 100'):
        tienda_aislada.aplicar_descuento('Arroz', porcentaje)
    producto_doble.actualizar_precio.assert_not_called()

@pytest.mark.parametrize('porcentaje', ['20', None, True])
def test_descuento_tipo_invalido(porcentaje):
    producto_doble = Mock(spec=Producto)
    producto_doble.nombre = 'Arroz'
    producto_doble.precio = 1000
    tienda_aislada = Tienda()
    tienda_aislada.agregar_producto(producto_doble)
    with pytest.raises(TypeError, match='número real'):
        tienda_aislada.aplicar_descuento('Arroz', porcentaje)
    producto_doble.actualizar_precio.assert_not_called()

def test_descuento_inexistente():
    producto_doble = Mock(spec=Producto)
    producto_doble.nombre = 'Arroz'
    producto_doble.precio = 1000
    tienda_aislada = Tienda()
    tienda_aislada.agregar_producto(producto_doble)
    with pytest.raises(ProductoNoEncontradoError):
        tienda_aislada.aplicar_descuento('Inexistente', 20)
    producto_doble.actualizar_precio.assert_not_called()

def test_busqueda_distingue_mayusculas():
    tienda_aislada = Tienda()
    tienda_aislada.agregar_producto(Producto('Arroz', 1000, 'Alimentos'))
    with pytest.raises(ProductoNoEncontradoError):
        tienda_aislada.buscar_producto('arroz')
