import pytest
from producto import Producto

def test_atributos():
    producto = Producto('Arroz', 1000, 'Alimentos')
    assert (producto.nombre, producto.precio, producto.categoria) == ('Arroz', 1000, 'Alimentos')

@pytest.mark.parametrize('precio', [0, 0.01, 750, 1250.5])
def test_actualizar_precio_valido(precio):
    producto = Producto('Arroz', 1000, 'Alimentos')
    producto.actualizar_precio(precio)
    assert producto.precio == precio
    assert (producto.nombre, producto.categoria) == ('Arroz', 'Alimentos')

@pytest.mark.parametrize('precio', [-0.01, -100, float('nan'), float('inf'), -float('inf')])
def test_precio_invalido_conserva_estado(precio):
    producto = Producto('Arroz', 1000, 'Alimentos')
    with pytest.raises(ValueError, match='finito y no negativo'):
        producto.actualizar_precio(precio)
    assert producto.precio == 1000

@pytest.mark.parametrize('precio', ['100', None, True])
def test_tipo_precio_invalido(precio):
    producto = Producto('Arroz', 1000, 'Alimentos')
    with pytest.raises(TypeError, match='número real'):
        producto.actualizar_precio(precio)
    assert producto.precio == 1000

def test_constructor_rechaza_negativo():
    with pytest.raises(ValueError):
        Producto('Arroz', -1, 'Alimentos')
