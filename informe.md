TRABAJO PRÁCTICO 1 · 2026

Pruebas del software

Uso de un framework de testing
Puntos 1, 2 y 3

Universidad Nacional de Tucumán · Facultad de Ciencias Exactas y Tecnología

Ingeniería de Software 1 (PU) / Ingeniería de Software 2 (LI / II)

## Participantes

Valla, Pablo Gastón
Zamorano, Ruth Ayelen

## Alcance de esta versión

Se resuelven únicamente las actividades obligatorias y las preguntas conceptuales de los puntos 1, 2 y 3 de la consigna: configuración y pruebas básicas; excepciones; y dobles para probar descuentos. Se excluyen el ejercicio opcional del punto 3 y los puntos 4 y 5.

La carpeta etapa_1 conserva el código base y sus retornos None y False para productos ausentes. Los módulos producto.py y tienda.py contienen la versión con excepciones y descuentos. Cada test prepara localmente sus objetos; no se utilizan fixtures. Los únicos mocks se encuentran en las pruebas de aplicar_descuento.

## Diseño de las pruebas

Se seleccionan casos normales, productos presentes y ausentes, precios negativos, cero y positivos, y descuentos en los extremos del intervalo permitido. Cada prueba define un resultado esperado y, cuando corresponde, verifica que un error no modifique el estado. Se sigue el enfoque de clases de equivalencia y valores límite presentado en [1], pp. 13-16, y [2], sección 2.

## Decisiones de implementación

Se conserva el inventario como lista y la comparación exacta de nombres. Ante duplicados se opera sobre la primera coincidencia. El precio cero es válido y los descuentos se aceptan entre 0 y 100 inclusive. Como validación adicional se rechazan números no finitos, booleanos y tipos no numéricos. Se usan int y float sin redondeo monetario, con pytest.approx para resultados decimales.

Se esperan nombres y categorías de tipo cadena. No se incorporan stock, persistencia ni interfaz gráfica. El proyecto contiene código, pruebas, instrucciones de ejecución y evidencia de 44 casos aprobados.

# 1 y 2 · Pruebas básicas y excepciones

## 1. Configuración inicial y actividad práctica

Se eligió pytest por sus aserciones directas, parametrización y comprobación de excepciones. Los dobles se construyen con unittest.mock, incluido en Python, sin dependencias adicionales para esa funcionalidad. Las versiones y comandos están en la página 4 y en README.md.

etapa_1/producto.py y etapa_1/tienda.py conservan el comportamiento de la consigna: buscar un nombre ausente devuelve None y eliminarlo devuelve False. tests/test_etapa_1.py verifica atributos, inventario vacío, incorporación, búsqueda existente e inexistente y eliminación exitosa o fallida. Se comprueba también el estado restante y las ausencias en listas vacías y no vacías.

## ¿Cuáles son pruebas unitarias y cuáles de integración?

Tomamos la clase como unidad, según la teoría de OO [3], sección 5.2.1. Verificar nombre, precio y categoría de Producto es una prueba unitaria. La prueba de aplicar_descuento con un doble de Producto aísla Tienda para comprobar el cálculo y la llamada al colaborador. Cuando una prueba crea productos reales y los agrega, busca o elimina mediante Tienda, ejercita la colaboración entre dos clases y aquí se clasifica como integración de alcance pequeño. La clasificación depende del límite de la unidad elegido; no de que el test sea corto o use pytest.

## 2. Cambios y comprobación de excepciones

En la versión final, buscar_producto y eliminar_producto lanzan ProductoNoEncontradoError, subclase de LookupError, si no existe el nombre. Una eliminación exitosa sigue devolviendo True. Producto.actualizar_precio valida antes de asignar; un precio negativo produce ValueError y deja el precio anterior intacto. El constructor final reutiliza esa validación.

```python
def test_precio_invalido_conserva_estado():
    producto = Producto("Arroz", 1000, "Alimentos")
    with pytest.raises(ValueError):
        producto.actualizar_precio(-0.01)
    assert producto.precio == 1000
```

Las pruebas reales parametrizan también precios cero, positivos, no finitos y tipos incorrectos. Para búsquedas y eliminaciones ausentes se comprueban la clase de excepción, un mensaje identificable y el inventario sin cambios. Los tests históricos se ejecutan sobre etapa_1; los finales esperan el contrato nuevo.

## ¿Se podrían escribir primero los tests? Proceso TDD

Sí. Primero se escribe una prueba de una regla todavía no implementada; por ejemplo, que actualizar_precio(-1) lance ValueError y conserve 1000. Se ejecuta y se comprueba que falle por esa funcionalidad faltante (rojo). Luego se implementa lo mínimo para satisfacerla y se ejecuta nuevamente (verde). Finalmente se mejora el diseño sin cambiar el comportamiento y se repite toda la suite (refactorización y regresión). Después se incorpora otra regla, como aceptar cero.

Este es el proceso propuesto para trabajar con pruebas primero; la entrega no afirma disponer de un historial registrado de ciclos rojo-verde. La teoría admite diseñar las pruebas antes o después del código [1], p. 32. Probar detecta el fallo; depurar busca y corrige su causa [2], sección 4.

# 3 · Dobles para aislar unidades

## Actividad: descuento y verificación de la llamada

aplicar_descuento(nombre, porcentaje) busca el producto, calcula precio_actual × (1 - porcentaje / 100) y delega la asignación en actualizar_precio. Se prueban 0 %, 0,01 %, 20 %, 99,99 % y 100 %, además de entradas inválidas y productos ausentes.

```python
doble = Mock(spec=Producto)
doble.nombre = "Arroz"
doble.precio = 1000
tienda = Tienda()
tienda.agregar_producto(doble)

tienda.aplicar_descuento("Arroz", 20)
doble.actualizar_precio.assert_called_once_with(800)
```

No se crea una instancia real de Producto. spec=Producto restringe los métodos accesibles al contrato de la clase; los atributos creados en __init__ se configuran explícitamente en el doble. La aserción verifica el importe y exactamente una llamada. En porcentajes inválidos se exige assert_not_called().

El mock no cambia automáticamente su atributo precio al recibir actualizar_precio. Por eso esta prueba demuestra el cálculo y la interacción esperada, la actualización real de un precio se comprueba por separado en las pruebas de Producto. No se incluyen los tests opcionales de agregar, buscar y eliminar con dobles. Las llamadas necesarias para preparar o ejecutar el descuento no constituyen pruebas independientes de esas operaciones.

## ¿Qué controladores y resguardos se identifican?

Los controladores (drivers o conductores) son las funciones de prueba, ejecutadas por pytest: preparan entradas, invocan la unidad y comparan resultados con los esperados. El runner organiza la ejecución. El doble de Producto ocupa el lugar del colaborador llamado por Tienda y desempeña el papel de resguardo. Además permite registrar y verificar interacciones. No debe confundirse el controlador de prueba con una clase controladora de la aplicación [1], pp. 32-33 y 62; [2], sección 3.4.

## ¿Qué es un test double? ¿Qué otros nombres existen?

Es un sustituto de una dependencia real que permite controlar una prueba y aislar la unidad. La denominación general incluye distintas funciones, que conviene distinguir:

| Tipo | Función en una prueba |
| --- | --- |
| Dummy | Completa un argumento obligatorio, pero su comportamiento no se utiliza. |
| Stub / resguardo | Entrega respuestas predeterminadas para controlar una dependencia. |
| Spy / espía | Registra llamadas para comprobar después cómo se usó el colaborador. |
| Mock | Permite establecer o verificar interacciones esperadas, como una llamada y sus argumentos. |
| Fake | Implementación simplificada que funciona, como un repositorio en memoria. |

En este trabajo se usa Mock como colaborador configurable y se verifican llamadas; los términos no son sinónimos exactos, aunque informalmente se diga “simulado” a cualquiera de ellos.

# Ejecución, resultados y referencias

## Entorno e instrucciones

Verificado con Python 3.12.14 y pytest 8.3.5. La aplicación utiliza la biblioteca estándar de Python; pytest es la única dependencia externa para las pruebas. Desde esta carpeta, en Windows PowerShell:

```python
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

Para ejecutar solo un grupo, agregar tests/test_etapa_1.py, tests/test_producto.py o tests/test_tienda.py al comando de pytest. En Linux/macOS se puede crear el entorno con python3 y usar .venv/bin/python.

## Evidencia de ejecución

Se ejecutaron 44 casos y todos aprobaron: 11 de la etapa inicial, 14 de Producto y 19 de Tienda. Las variantes parametrizadas cuentan individualmente. La salida está en evidencias/pruebas.txt y los resultados estructurados en evidencias/resultados.xml.

Los tests de la etapa inicial verifican atributos, altas, búsquedas y bajas con productos reales. Los de Producto comprueban actualizaciones, validación y conservación del precio ante errores. Los de Tienda comprueban inventarios independientes, excepciones, comparación exacta de nombres y descuentos con mocks.

Que las pruebas pasen no garantiza ausencia de defectos. Los resultados indican que los casos ejecutados coincidieron con sus resultados esperados. Esta versión no incluye la actividad de cobertura ni el flujo de carrito del punto 5.

## Referencias del material de clase

[1] Valdecantos, Héctor A. Pruebas del Software. Archivo 01.pruebas.del.software.pdf. Diseño de casos: pp. 13-16; pruebas de unidad y dobles: pp. 30-33; orientación a objetos: pp. 58-62.

[2] Mentz, María Isabel. Ingeniería de Software / Ingeniería de Software II, año 2014. Apuntes.01.pdf. Sección 2: técnicas de prueba; sección 3.4: pruebas de unidad, conductores y resguardos; sección 4: depuración.

[3] Apuntes.02.pdf. Secciones 5.2.1 y 5.2.2: unidad e integración en orientación a objetos. Se considera a la clase como unidad y se distinguen pruebas aisladas y colaboración entre clases.

[4] Pruebas del software: uso de un framework de testing. Trabajo Práctico 1, 16 de septiembre de 2026. En esta entrega se resuelven los puntos 1, 2 y 3, sin la actividad opcional.

# Anexo · Código de los puntos 2 y 3

El código inicial del punto 1 y todos los tests se entregan en sus archivos correspondientes.

## producto.py

```python
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
```

## tienda.py

```python
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
```
