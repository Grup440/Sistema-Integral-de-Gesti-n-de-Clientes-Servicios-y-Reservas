"""Ejecuta las pruebas por segmentos en orden y después la demostración integrada."""
# Importa el ejecutor de procesos y el intérprete actual.
import subprocess
import sys
# Permite resolver rutas sin depender de la carpeta desde la cual se abre el archivo.
from pathlib import Path

# Ejecuta las etapas solo cuando este archivo se abre como programa principal.
if __name__ == '__main__':
    # Usa la carpeta del proyecto como ubicación de trabajo.
    raiz = Path(__file__).resolve().parent
    # Distribuye las pruebas existentes por responsabilidad funcional.
    etapas = [
        # Comprueba entidades abstractas, contacto, encapsulación y duplicados.
        ('1. Clientes y entidades', ['SistemaTests.test_abstraccion', 'SistemaTests.test_contacto_atomico', 'SistemaTests.test_identidad_encapsulada', 'SistemaTests.test_duplicado_sin_mutacion']),
        # Comprueba los servicios, parámetros, números, costos y tasas del menú.
        ('2. Servicios y costos', ['SistemaTests.test_sobrecarga_opcionales', 'SistemaTests.test_polimorfismo', 'SistemaTests.test_numeros_invalidos', 'SistemaTests.test_parametros_obligatorios', 'SistemaTests.test_calculo_inconsistente', 'TasasMenuTests']),
        # Comprueba estados, ocupación, atomicidad y recuperación de reservas.
        ('3. Reservas', ['SistemaTests.test_ciclo_reserva', 'SistemaTests.test_cancelacion_libera', 'SistemaTests.test_fallo_no_inserta_reserva', 'SistemaTests.test_causa_y_estado_conservado']),
        # Comprueba la causa original de errores y su registro con continuidad.
        ('4. Excepciones y logs', ['SistemaTests.test_cadena_conversion', 'SistemaTests.test_recuperacion_y_log']),
    ]
    # Ejecuta cada grupo en el orden definido.
    for titulo, pruebas in etapas:
        # Muestra el segmento que se está verificando.
        print('\nETAPA ' + titulo, flush=True)
        # Construye identificadores de pruebas para el ejecutor unittest.
        nombres = ['test_sistema.' + prueba for prueba in pruebas]
        # Añade la carpeta de pruebas al buscador de módulos y ejecuta el grupo.
        comando = [sys.executable, '-c', "import sys, unittest; sys.path.insert(0, 'tests'); unittest.main(module=None, argv=['validacion', '-v'] + sys.argv[1:])", *nombres]
        # Espera la finalización antes de pasar a la siguiente etapa.
        resultado = subprocess.run(comando, cwd=raiz, check=False)
        # Detiene la validación para que se corrija cualquier fallo detectado.
        if resultado.returncode:
            # Devuelve un código de salida que indica validación fallida.
            raise SystemExit(resultado.returncode)
    # Anuncia la verificación integrada de las 31 operaciones.
    print('\nETAPA 5. Simulación completa', flush=True)
    # Ejecuta la demostración usando el mismo intérprete de Python.
    resultado = subprocess.run([sys.executable, 'main.py', '--demo'], cwd=raiz, check=False)
    # Propaga el resultado de la simulación al sistema operativo.
    raise SystemExit(resultado.returncode)
