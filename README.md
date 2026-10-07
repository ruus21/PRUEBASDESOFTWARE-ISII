# TP 1 - Puntos 1, 2 y 3

Participantes: **Valla, Pablo Gastón** y **Zamorano, Ruth Ayelen**.

## Cómo ejecutar los tests

Necesitás Python 3.12 instalado. Abrí PowerShell en la carpeta del proyecto.

La primera vez, creá el entorno e instalá las dependencias:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para correr todos los tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Si todo funciona, al final verás **44 passed**.

## Punto 1: pruebas básicas

**¿Puedes identificar pruebas de unidad y de integración en la práctica realizada?**

Sí. Tomamos cada clase como una unidad:

- **Pruebas de unidad:** comprueban una clase de forma aislada. Por ejemplo, verificar los atributos de `Producto` o que no permita actualizar su precio a un valor negativo. También se aísla `Tienda` al probar el descuento con un producto simulado.
- **Pruebas de integración:** comprueban cómo trabajan juntas las clases. Por ejemplo, crear un `Producto` real, agregarlo a una `Tienda` y verificar que se pueda buscar o eliminar.

## Punto 2: pruebas con excepciones

**¿Podrías haber escrito las pruebas antes de modificar el código? ¿Cómo sería ese proceso?**

Sí. Ese modo de trabajar se llama **TDD** o desarrollo guiado por pruebas. El proceso sería:

1. Escribir un test con el comportamiento esperado. Por ejemplo, que actualizar un precio a `-1` lance `ValueError` y conserve el precio anterior.
2. Ejecutarlo y comprobar que falle porque ese comportamiento todavía no está implementado.
3. Modificar el código para que el test pase.
4. Mejorar el código si hace falta y volver a ejecutar las pruebas para comprobar que todo siga funcionando.

Se repite el ciclo con cada comportamiento nuevo. Esta es una explicación de cómo se podría trabajar; no implica que el proyecto se haya desarrollado siguiendo ese orden.

## Punto 3: dobles de prueba

**¿Puedes identificar controladores y resguardos en el trabajo?**

Sí. Las funciones de test actúan como **controladores**: preparan los datos, llaman al código y comprueban el resultado. `pytest` se encarga de ejecutarlas.

El producto simulado con `Mock(spec=Producto)` cumple el papel de **resguardo**, porque reemplaza al producto real que utiliza `Tienda`. Permite verificar que un descuento del 20 % sobre un precio de 1000 llame una sola vez a `actualizar_precio` con 800. El mock registra esa llamada, pero no actualiza automáticamente su atributo `precio`.

**¿Qué es un test double? ¿Hay otros nombres para los objetos o funciones simulados?**

Un **test double** o doble de prueba es un sustituto de un objeto o función real. Sirve para probar una parte del programa de forma aislada y controlar sus dependencias.

Hay distintos tipos, según lo que hacen:

- **Stub o resguardo:** entrega respuestas preparadas para la prueba.
- **Mock:** permite comprobar llamadas y argumentos esperados. Es el que usamos para los descuentos.
- **Spy o espía:** registra cómo fue utilizado para revisarlo después.
- **Fake:** es una implementación simplificada que funciona, como una base de datos en memoria.
- **Dummy:** completa un parámetro necesario, pero no se utiliza durante la prueba.

Todos son dobles de prueba, aunque no cumplen exactamente la misma función.
