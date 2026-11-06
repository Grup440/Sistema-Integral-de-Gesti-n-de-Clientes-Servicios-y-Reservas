**Empieza por `EMPIEZA_AQUI.md` para ejecutar y subir el proyecto paso a paso.**

# Software FJ — Sistema integral de clientes, servicios y reservas

**Ejercicio 1 · Programación orientada a objetos · Python 3.10 o superior**

## Inicio rápido

1. Descomprimir el archivo ZIP.
2. Abrir una terminal dentro de la carpeta `Software_FJ_Documentado`.
3. Ejecutar `python main.py` para abrir el menú interactivo.
4. Ejecutar `python main.py --demo` para observar la simulación completa.
5. Ejecutar `python -m unittest discover -s tests -v` para verificar el sistema.

En algunos equipos el comando es `python3` o `py`, en lugar de `python`.
No se requieren paquetes externos, conexión a Internet ni bases de datos.
En Windows también se puede abrir `INICIAR.bat` con doble clic, si Python está instalado.

## Entrega incluida

- `main.py`: aplicación de consola y manejo de cierre.
- `fj/modelos.py`: entidades, validadores, excepciones y reglas del negocio.
- `fj/gestion.py`: listas internas, búsquedas y recuperación de errores.
- `fj/demo.py`: 31 operaciones reproducibles con verificación de resultados esperados.
- `tests/test_sistema.py`: 17 pruebas automatizadas.
- `DOCUMENTACION.md`: explicación técnica, reglas, fórmulas y correspondencia con la consigna.
- `diagrama.mmd`: diagrama de clases en formato Mermaid.
- `evidencias/simulacion.txt`: salida real de la simulación ejecutada.
- `evidencias/pruebas.txt`: salida real de las pruebas ejecutadas.
- `logs/software_fj.log`: registro real de eventos, errores y causas encadenadas.

Los mensajes CONTROLADO y RECUPERADO de la demostración son resultados esperados: muestran cómo se maneja un error y se ejecuta la operación siguiente.

## Uso del menú

1. Registrar un cliente con documento de 5 a 15 dígitos, nombre, correo y teléfono.
2. Crear un servicio de tipo `sala`, `equipo` o `asesoria`.
3. Consultar los identificadores con la opción 7 y usarlos al crear una reserva.
4. Indicar duración y el parámetro del servicio: asistentes, cantidad o tema.
5. Ingresar tasas decimales: `0.19` significa 19 % y `0.10` significa 10 %.
6. Confirmar y después procesar la reserva. Alternativamente, cancelarla antes del procesamiento.
7. Usar la opción 8 para cambiar la disponibilidad de un servicio.
8. Escribir 0 para salir.

Ejemplo: sala con tarifa 50000, duración 2, asistentes 5, descuento 0.10 e impuesto 0.19. Total: **107100.00**.
Use punto como separador decimal y escriba las tarifas sin separadores de miles.

## Alcance

Los clientes, servicios y reservas permanecen únicamente en memoria. Al cerrar el programa se eliminan; no se cargan desde el log. El log es exclusivamente una bitácora técnica.
La demostración se ejecuta en una sesión independiente y finaliza al terminar sus 31 operaciones.
La política de disponibilidad es secuencial: cada servicio admite una reserva pendiente o confirmada a la vez; se libera al procesarla o cancelarla. No se modelan fechas, calendarios ni reservas simultáneas de unidades parciales.

Validación secuencial: `python validar_etapas.py`. Código documentado por instrucción. Se corrigió la aceptación de tasas de valor cero recibidas como texto desde el menú.
