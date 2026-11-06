# Software FJ: ejecución y entrega paso a paso

## 1. Preparar el proyecto en tu computador

1. Descarga y descomprime el ZIP. Haz clic derecho y selecciona **Extraer todo**.
2. Entra a `Software_FJ_Documentado`; debes ver `main.py` y la carpeta `fj`.
3. En Windows, haz clic en la barra de direcciones de esa carpeta, escribe `cmd` y pulsa Enter.
4. Escribe `py --version`. Se necesita Python 3.10 o superior. Si no se reconoce `py`, prueba `python --version`.
5. Si ninguno funciona, instala Python antes de continuar.

## 2. Ejecutar cada segmento en orden

En la terminal de la carpeta escribe:

```bash
py validar_etapas.py
```

Si tu equipo usa `python` o `python3`, reemplaza `py` por ese comando.
Se ejecutan, en orden: clientes y abstracción; servicios y costos; reservas; excepciones y logs; y la simulación integrada de 31 operaciones.
El proceso se detiene si una etapa falla. Los errores CONTROLADO y RECUPERADO de la demostración son intencionales; la línea final debe indicar 31 resultados coincidentes.

Para repetir todas las pruebas de forma independiente:

```bash
py -m unittest discover -s tests -v
```

## 3. Probar el menú

```bash
py main.py
```

Registra un cliente, crea un servicio y utiliza los identificadores que aparecen con la opción 7 para crear una reserva. Confírmala con la opción 4 y procésala con la 5. La opción 6 permite cancelar antes del procesamiento y la 8 cambia la disponibilidad. Usa 0 para cerrar.

Puedes ejecutar únicamente la demostración:

```bash
py main.py --demo
```

Los datos se borran al cerrar porque permanecen solo en memoria. El archivo `logs/software_fj.log` registra los eventos y errores; no es una base de datos ni permite recuperar clientes.

## 4. Entrar al repositorio con tu cuenta

Repositorio del grupo:
https://github.com/Grup440/Sistema-Integral-de-Gesti-n-de-Clientes-Servicios-y-Reservas

1. Abre el repositorio en la ventana donde ya tienes iniciada tu sesión personal.
2. Comprueba en tu foto de perfil que estás con tu usuario.
3. Si te enviaron una invitación, acéptala desde el correo o el aviso de GitHub.
4. Si no tienes permiso para subir, quien administra Grup440 debe agregarte desde Settings → Collaborators → Add people. No basta con poder ver un repositorio público.

## 5. Organizar los cinco aportes

Antes de cargar archivos, acuerden la distribución. Este paquete es una base de trabajo para revisar, ejecutar y desarrollar entre los integrantes. Sus cuentas e historial deben reflejar los cambios que realmente realiza cada persona.

| Integrante | Parte para revisar y desarrollar | Evidencia técnica |
| --- | --- | --- |
| 1 | Entidad, Cliente y validadores de datos | Pruebas de cliente y actualización de contacto |
| 2 | Servicio, Sala, Equipo y Asesoria | Validaciones, polimorfismo y fórmulas |
| 3 | Reserva y Estado | Confirmación, cancelación y procesamiento |
| 4 | Gestor, Registro y menú | Listas, manejo de errores y bitácora |
| 5 | Pruebas, simulación y documentación | Validación secuencial y resultados |

Los integrantes 1, 2 y 3 trabajan sobre secciones distintas de `fj/modelos.py`. Integren esos cambios de forma secuencial: cada uno descarga la versión más reciente antes de editar para no reemplazar el aporte anterior. Para trabajo simultáneo conviene utilizar ramas y solicitudes de incorporación.

## 6. Cargar los archivos desde GitHub

Si el equipo acuerda que cargues la base inicial y ya tienes permiso:

1. Abre el repositorio y pulsa **Add file / Agregar archivo**.
2. Selecciona **Upload files / Subir archivos**.
3. Arrastra el contenido de `Software_FJ_Documentado`: `main.py`, la carpeta `fj`, `tests`, las guías, etc. Deben quedar `main.py` y `fj` en el mismo nivel.
4. No cargues el ZIP como sustituto del código. Excluye `__pycache__` y datos personales. `logs` es una bitácora de ejemplo que se regenera al ejecutar.
5. Conserva el título y descripción del grupo al combinar el nuevo README con el archivo inicial.
6. Escribe un mensaje que describa el cambio real, por ejemplo: **Agregar base ejecutable de Software FJ y guía de validación**.
7. Pulsa **Commit changes / Confirmar cambios**. Si GitHub propone un fork, estás creando una copia: revisa primero el permiso en el repositorio del grupo.
8. Cada integrante realiza después su revisión y aporte desde su propia cuenta, documenta sus cambios y vuelve a probarlos.

Esta sesión de asistencia tiene permiso de lectura en el repositorio; los archivos de este paquete no se han subido automáticamente.

## 7. Evidencias y entrega

Guarda capturas reales del resultado de las pruebas, del resumen de la demostración y del historial de aportes. Incluye la dirección del repositorio en el documento de entrega si el aula lo solicita. Las instrucciones compartidas no permiten determinar si además se exige video o una plantilla institucional; verifica ese apartado en la guía completa.

El ZIP contiene el código comentado por instrucción, la documentación técnica, un diagrama de clases y las salidas reales generadas durante la comprobación. Los comentarios explican clases, métodos, decisiones, asignaciones y tratamiento de excepciones; los docstrings documentan los módulos y contratos.
