# Documentación del proyecto Software FJ

## 1. Objetivo

Desarrollar una aplicación de consola que permita gestionar clientes, salas, equipos, asesorías y reservas mediante objetos y listas, aplicando los principios de programación orientada a objetos y el manejo controlado de excepciones. Los archivos se utilizan para registrar eventos, errores y evidencias de ejecución, sin almacenar un repositorio de clientes o reservas.

## 2. Arquitectura

La presentación se encuentra en `main.py`, el dominio en `fj/modelos.py` y la coordinación en `fj/gestion.py`. `fj/demo.py` utiliza la misma lógica del menú para demostrar casos válidos e inválidos. Las pruebas están separadas del código de producción.

El gestor mantiene tres listas privadas. Sus propiedades devuelven tuplas para impedir que una operación externa inserte o retire elementos directamente de las colecciones. Los objetos siguen siendo entidades mutables mediante sus métodos autorizados.

## 3. Aplicación de la programación orientada a objetos

| Principio o requisito | Implementación |
| --- | --- |
| Abstracción general | `Entidad(ABC)` define identidad y el contrato abstracto `describir()` |
| Abstracción de servicios | `Servicio(Entidad)` exige validación, cálculo base y descripción |
| Herencia | `Sala`, `Equipo` y `Asesoria` heredan de `Servicio`; `Cliente` y `Reserva` heredan de `Entidad` |
| Polimorfismo | Una reserva invoca `servicio.calcular_costo()` sin conocer el tipo concreto; cada servicio valida y calcula con su implementación |
| Sobrescritura | Las tres especializaciones redefinen `validar_parametros`, `calcular_base` y `describir` |
| Encapsulación | Datos privados con doble guion bajo, propiedades de lectura y métodos de modificación validados |
| Variantes de métodos | `calcular_costo(duracion, *, impuesto=0, descuento=0, **parametros)` acepta costo base, impuesto, descuento o ambos |
| Composición | `Reserva` conserva referencias a un cliente y a un servicio |
| Colecciones internas | Listas privadas de clientes, servicios y reservas en `Gestor` |
| Excepciones propias | Jerarquía con base `ErrorSistema` y seis excepciones especializadas |

### Precisión sobre la sobrecarga en Python

Python no selecciona automáticamente métodos por distintas firmas como Java. Declarar varias veces un método con el mismo nombre reemplazaría su definición anterior. En este proyecto se implementan las variantes solicitadas mediante parámetros opcionales, opción expresamente permitida por la consigna. No se utiliza `typing.overload` como si proporcionara despacho en ejecución.

Ejemplos sobre una sala ya creada:

```python
sala.calcular_costo(2, asistentes=5)
sala.calcular_costo(2, impuesto='0.19', asistentes=5)
sala.calcular_costo(2, descuento='0.10', asistentes=5)
sala.calcular_costo(2, impuesto='0.19', descuento='0.10', asistentes=5)
```

## 4. Validaciones y reglas del negocio

- Documento: cadena de 5 a 15 dígitos y única en el gestor.
- Nombre: mínimo 3 caracteres; letras, espacios, apóstrofos y guiones.
- Correo: validación estructural básica; no verifica la existencia de la cuenta.
- Teléfono: 7 a 15 dígitos, con prefijo + opcional.
- Tarifas: números finitos estrictamente positivos.
- Duración: mayor que cero y máximo 24 horas; se aceptan fracciones.
- Impuestos y descuentos: tasas entre cero y uno, ambos extremos incluidos.
- Capacidad: entero entre 1 y 500. Asistentes: entero positivo que no excede capacidad.
- Unidades: entero entre 1 y 1000. Cantidad: entero positivo que no excede existencias.
- Asesoría: especialidad y tema obligatorios.
- Se rechazan parámetros desconocidos, números no finitos y booleanos usados como números.
- Un servicio puede deshabilitarse con un booleano validado.
- Cada servicio admite una reserva activa a la vez. Los estados pendiente y confirmada lo ocupan; procesada y cancelada lo liberan.
- Una reserva fallida no se incorpora a la lista. La actualización del contacto se realiza solo después de validar todos los campos.

Las restricciones son decisiones explícitas del ejercicio, no reglas legales de una empresa real. Los valores del impuesto son ejemplos configurables, no asesoría tributaria.

## 5. Cálculos

Se utiliza `Decimal` para evitar errores habituales de representación binaria al calcular dinero. El valor final se redondea a dos decimales mediante `ROUND_HALF_UP`.

- Sala: base = tarifa por hora × duración.
- Equipo: base = tarifa por hora y unidad × duración × cantidad.
- Asesoría: base = tarifa por hora × duración.
- Total = base × (1 − descuento) × (1 + impuesto).

El descuento se aplica antes del impuesto. Ejemplo: 50000 × 2 × 0.90 × 1.19 = 107100.00.
El método verifica que el resultado sea finito y no negativo. Un resultado inconsistente genera `CalculoError` con su causa original.

## 6. Ciclo de vida de una reserva

| Estado actual | Operación permitida | Estado siguiente |
| --- | --- | --- |
| Pendiente | Confirmar | Confirmada |
| Pendiente | Cancelar | Cancelada |
| Confirmada | Procesar, si el servicio continúa disponible | Procesada |
| Confirmada | Cancelar | Cancelada |
| Procesada | Ninguna transición | Se conserva |
| Cancelada | Ninguna transición | Se conserva |

La confirmación y el procesamiento vuelven a validar el servicio. Si un servicio se deshabilita después de confirmar, el procesamiento falla sin cambiar el estado; después de habilitarlo puede reintentarse.

## 7. Manejo avanzado de excepciones

| Excepción | Situación |
| --- | --- |
| `ValidacionError` | Datos incompletos, tipos incorrectos, rangos o parámetros inválidos |
| `DuplicadoError` | Documento o nombre de servicio duplicado |
| `NoEncontradoError` | Identificador inexistente |
| `NoDisponibleError` | Servicio deshabilitado, ocupado o imposibilidad de procesamiento |
| `EstadoError` | Transición de reserva no permitida |
| `CalculoError` | Resultado monetario inconsistente o error aritmético |

`numero()` utiliza `try/except` y `raise ... from causa` para conservar la causa de conversiones fallidas. `Reserva.procesar()` utiliza `try/except/else`: solo cambia el estado cuando la validación termina correctamente. La imposibilidad de procesar se encadena a la excepción original.

`Gestor.ejecutar()` utiliza `try/except/else/finally`: captura errores de negocio y fallos técnicos inesperados, registra el traceback, comunica el resultado y contabiliza siempre la operación. `main()` utiliza `try/finally` para cerrar los manejadores del log. La salida por teclado se trata expresamente.

Las operaciones de la interfaz y la demostración pasan por `Gestor.ejecutar`. Los métodos de dominio lanzan excepciones para que esta frontera las registre y controle; si se usa el dominio fuera de la aplicación, el llamador debe aplicar esa misma frontera.

La bitácora registra fecha, nivel, operación y traceback con causas encadenadas. No se imprimen documentos, correos ni teléfonos en los mensajes de log. Si el archivo no puede abrirse al iniciar, se informa y se utiliza la consola como alternativa. Sin permisos de escritura o con un disco no disponible no puede garantizarse que exista un archivo de log; la alternativa permite conservar mensajes visibles y seguir operando. Tampoco se pretende recuperarse de apagados, terminación del proceso o daños del sistema operativo.

## 8. Verificación ejecutada

Se ejecutaron **17 pruebas automatizadas**, todas satisfactorias. Cubren abstracción, encapsulación, atomicidad de actualizaciones, cuatro variantes de costo, polimorfismo, valores no finitos, parámetros faltantes, duplicados, ciclo de reserva, liberación de servicios, ausencia de inserciones fallidas, causa encadenada, recuperación con log y cálculos inconsistentes.

La demostración ejecutó **31 operaciones**. Sus 31 resultados coincidieron con lo esperado. Incluye registros válidos e inválidos, servicios correctos e incorrectos, reservas exitosas y fallidas, exceso de asistentes, doble reserva, sobrecantidad de equipos, servicio deshabilitado, procesamiento reintentado y un `RuntimeError` simulado seguido de un registro exitoso. Las salidas reales se incluyen en `evidencias`.

## 9. Extensibilidad

Para incorporar otro servicio se deriva de `Servicio` y se implementan sus tres contratos abstractos. El cálculo total y las reservas reutilizan la misma lógica. Se añade la opción de creación correspondiente a la interfaz. Para ampliar el negocio con fechas sería necesario introducir intervalos y validación de solapamientos; el alcance actual utiliza ocupación secuencial por servicio.

## 10. Distribución sugerida para cinco integrantes

Esta tabla propone responsabilidades para estudiar y sustentar el proyecto; no afirma participación real de personas determinadas.

| Integrante | Responsabilidad sugerida |
| --- | --- |
| 1 | Entidad, Cliente y encapsulación |
| 2 | Servicio y sus tres especializaciones |
| 3 | Reserva y transiciones de estado |
| 4 | Gestor, interfaz y manejo de excepciones |
| 5 | Pruebas, demostración y documentación |

## 11. Guía breve de sustentación

1. Explicar el objetivo y la ausencia de base de datos.
2. Mostrar las clases abstractas y los atributos encapsulados.
3. Comparar cómo se calcula el costo de los tres servicios.
4. Explicar las cuatro variantes del método de costo.
5. Ejecutar `python main.py --demo` y señalar errores controlados y operaciones posteriores.
6. Abrir el log y localizar el error encadenado de la asesoría.
7. Ejecutar las pruebas y explicar el ciclo de vida de una reserva.
