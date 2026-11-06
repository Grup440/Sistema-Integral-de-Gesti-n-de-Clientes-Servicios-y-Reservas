# Importa los módulos tempfile.
import tempfile
# Importa los módulos unittest.
import unittest
# Importa de pathlib los elementos Path.
from pathlib import Path
# Importa de decimal los elementos Decimal.
from decimal import Decimal
# Importa de fj.modelos los elementos *.
from fj.modelos import *
# Importa de fj.gestion los elementos Gestor, Registro.
from fj.gestion import Gestor, Registro

# Define la clase SistemaTests, que hereda de unittest.TestCase.
class SistemaTests(unittest.TestCase):

    # Define la operación setUp.
    def setUp(self):
        # Asigna a self.tmp el resultado de la expresión indicada.
        self.tmp = tempfile.TemporaryDirectory()
        # Asigna a self.log el resultado de la expresión indicada.
        self.log = Registro(Path(self.tmp.name) / 'prueba.log')
        # Asigna a self.g el resultado de la expresión indicada.
        self.g = Gestor(self.log)
        # Asigna a self.c el resultado de la expresión indicada.
        self.c = self.g.registrar_cliente(documento='123456', nombre='Ana López', correo='ana@example.com', telefono='3001234567')
        # Asigna a self.s el resultado de la expresión indicada.
        self.s = self.g.agregar_servicio(Sala('Sala', 100, 5))

    # Define la operación tearDown.
    def tearDown(self):
        # Invoca self.log.cerrar con los argumentos indicados.
        self.log.cerrar()
        # Invoca self.tmp.cleanup con los argumentos indicados.
        self.tmp.cleanup()

    # Define la operación reserva.
    def reserva(self):
        # Devuelve self.g.crear_reserva(self.c.id, self.s.id, 2, asistentes=3).
        return self.g.crear_reserva(self.c.id, self.s.id, 2, asistentes=3)

    # Define la operación test_abstraccion.
    def test_abstraccion(self):
        # Recorre (Entidad, Servicio) y asigna cada elemento a clase.
        for clase in (Entidad, Servicio):
            # Abre un contexto que libera sus recursos al terminar.
            with self.assertRaises(TypeError):
                # Invoca clase con los argumentos indicados.
                clase()

    # Define la operación test_contacto_atomico.
    def test_contacto_atomico(self):
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(ValidacionError):
            # Invoca self.c.actualizar_contacto con los argumentos indicados.
            self.c.actualizar_contacto('Otro Nombre', 'mal', '3001234567')
        # Invoca self.assertEqual con los argumentos indicados.
        self.assertEqual(self.c.nombre, 'Ana López')

    # Define la operación test_identidad_encapsulada.
    def test_identidad_encapsulada(self):
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(AttributeError):
            # Asigna a self.c.documento el resultado de la expresión indicada.
            self.c.documento = '999999'
        # Invoca self.assertIsInstance con los argumentos indicados.
        self.assertIsInstance(self.g.clientes, tuple)

    # Define la operación test_sobrecarga_opcionales.
    def test_sobrecarga_opcionales(self):
        # Recorre [({}, '200'), ({'impuesto': '.19'}, '238'), ({'descuento': '.10'}, '180'), ({'impuesto': '.19', 'descuento': '.10'}, '214.20')] y asigna cada elemento a (opciones, esperado).
        for opciones, esperado in [({}, '200'), ({'impuesto': '.19'}, '238'), ({'descuento': '.10'}, '180'), ({'impuesto': '.19', 'descuento': '.10'}, '214.20')]:
            # Invoca self.assertEqual con los argumentos indicados.
            self.assertEqual(self.s.calcular_costo(2, asistentes=2, **opciones), Decimal(esperado))

    # Define la operación test_polimorfismo.
    def test_polimorfismo(self):
        # Asigna a casos el resultado de la expresión indicada.
        casos = [(self.s, {'asistentes': 2}, '200'), (Equipo('E', 20, 3), {'cantidad': 2}, '80'), (Asesoria('A', 80, 'TI'), {'tema': 'POO'}, '160')]
        # Recorre casos y asigna cada elemento a (servicio, p, esperado).
        for servicio, p, esperado in casos:
            # Invoca self.assertEqual con los argumentos indicados.
            self.assertEqual(servicio.calcular_costo(2, **p), Decimal(esperado))

    # Define la operación test_numeros_invalidos.
    def test_numeros_invalidos(self):
        # Recorre ('NaN', 'Infinity', '-Infinity', 0, -1, True, None, 'abc', 25) y asigna cada elemento a valor.
        for valor in ('NaN', 'Infinity', '-Infinity', 0, -1, True, None, 'abc', 25):
            # Abre un contexto que libera sus recursos al terminar.
            with self.subTest(valor=valor), self.assertRaises(ValidacionError):
                # Invoca self.s.calcular_costo con los argumentos indicados.
                self.s.calcular_costo(valor, asistentes=1)

    # Define la operación test_parametros_obligatorios.
    def test_parametros_obligatorios(self):
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(ValidacionError):
            # Invoca self.s.calcular_costo con los argumentos indicados.
            self.s.calcular_costo(2)
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(ValidacionError):
            # Invoca self.s.calcular_costo con los argumentos indicados.
            self.s.calcular_costo(2, asistentes=1, desconocido=3)

    # Define la operación test_duplicado_sin_mutacion.
    def test_duplicado_sin_mutacion(self):
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(DuplicadoError):
            # Invoca self.g.registrar_cliente con los argumentos indicados.
            self.g.registrar_cliente(documento='123456', nombre='Ana López', correo='a@b.co', telefono='3001234567')
        # Invoca self.assertEqual con los argumentos indicados.
        self.assertEqual(len(self.g.clientes), 1)

    # Define la operación test_ciclo_reserva.
    def test_ciclo_reserva(self):
        # Asigna a r el resultado de la expresión indicada.
        r = self.reserva()
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(EstadoError):
            # Invoca r.procesar con los argumentos indicados.
            r.procesar()
        # Invoca r.confirmar con los argumentos indicados.
        r.confirmar()
        # Invoca r.procesar con los argumentos indicados.
        r.procesar()
        # Invoca self.assertEqual con los argumentos indicados.
        self.assertEqual(r.estado, Estado.PROCESADA)
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(EstadoError):
            # Invoca r.cancelar con los argumentos indicados.
            r.cancelar()
        # Invoca self.reserva con los argumentos indicados.
        self.reserva()

    # Define la operación test_cancelacion_libera.
    def test_cancelacion_libera(self):
        # Asigna a r el resultado de la expresión indicada.
        r = self.reserva()
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(NoDisponibleError):
            # Invoca self.reserva con los argumentos indicados.
            self.reserva()
        # Invoca r.cancelar con los argumentos indicados.
        r.cancelar()
        # Invoca self.reserva con los argumentos indicados.
        self.reserva()
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(EstadoError):
            # Invoca r.confirmar con los argumentos indicados.
            r.confirmar()

    # Define la operación test_fallo_no_inserta_reserva.
    def test_fallo_no_inserta_reserva(self):
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(ValidacionError):
            # Invoca self.g.crear_reserva con los argumentos indicados.
            self.g.crear_reserva(self.c.id, self.s.id, 2, asistentes=20)
        # Invoca self.assertEqual con los argumentos indicados.
        self.assertEqual(len(self.g.reservas), 0)

    # Define la operación test_causa_y_estado_conservado.
    def test_causa_y_estado_conservado(self):
        # Asigna a r el resultado de la expresión indicada.
        r = self.reserva()
        # Invoca r.confirmar con los argumentos indicados.
        r.confirmar()
        # Invoca self.s.cambiar_disponibilidad con los argumentos indicados.
        self.s.cambiar_disponibilidad(False)
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(NoDisponibleError) as captura:
            # Invoca r.procesar con los argumentos indicados.
            r.procesar()
        # Invoca self.assertIsInstance con los argumentos indicados.
        self.assertIsInstance(captura.exception.__cause__, NoDisponibleError)
        # Invoca self.assertEqual con los argumentos indicados.
        self.assertEqual(r.estado, Estado.CONFIRMADA)
        # Invoca self.s.cambiar_disponibilidad con los argumentos indicados.
        self.s.cambiar_disponibilidad(True)
        # Invoca r.procesar con los argumentos indicados.
        r.procesar()

    # Define la operación test_cadena_conversion.
    def test_cadena_conversion(self):
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(ValidacionError) as captura:
            # Invoca numero con los argumentos indicados.
            numero('abc', 'Duración')
        # Invoca self.assertIsNotNone con los argumentos indicados.
        self.assertIsNotNone(captura.exception.__cause__)

    # Define la operación test_recuperacion_y_log.
    def test_recuperacion_y_log(self):

        # Define la operación fallo.
        def fallo():
            # Lanza la excepción indicada para detener esta operación.
            raise RuntimeError('simulado')
        # Invoca self.assertFalse con los argumentos indicados.
        self.assertFalse(self.g.ejecutar('Fallo simulado', fallo)[0])
        # Invoca self.assertTrue con los argumentos indicados.
        self.assertTrue(self.g.ejecutar('Siguiente operación', lambda: 10)[0])
        # Asigna a contenido el resultado de la expresión indicada.
        contenido = (Path(self.tmp.name) / 'prueba.log').read_text(encoding='utf-8')
        # Invoca self.assertIn con los argumentos indicados.
        self.assertIn('RuntimeError', contenido)
        # Invoca self.assertIn con los argumentos indicados.
        self.assertIn('Fin de operación #2', contenido)

    # Define la operación test_calculo_inconsistente.
    def test_calculo_inconsistente(self):

        # Define la clase SalaDefectuosa, que hereda de Sala.
        class SalaDefectuosa(Sala):

            # Calcula el valor antes de aplicar descuento e impuesto.
            def calcular_base(self, duracion, **p):
                # Devuelve Decimal('-1').
                return Decimal('-1')
        # Abre un contexto que libera sus recursos al terminar.
        with self.assertRaises(CalculoError):
            # Invoca SalaDefectuosa('X', 100, 5).calcular_costo con los argumentos indicados.
            SalaDefectuosa('X', 100, 5).calcular_costo(2, asistentes=1)
# Evalúa la condición: __name__ == '__main__'.
# Comprueba tasas procedentes del menú, que siempre se reciben como texto.
class TasasMenuTests(unittest.TestCase):
    # Verifica que dejar impuesto y descuento en cero permite crear la reserva.
    def test_tasas_cero_desde_menu(self):
        # Crea una sala con tarifa y capacidad conocidas.
        sala = Sala('Sala de prueba', 100, 5)
        # Contrasta tres representaciones textuales válidas de cero.
        for cero in ('0', '0.0', '0.00'):
            # El costo conserva su base cuando ambas tasas son cero.
            self.assertEqual(sala.calcular_costo(2, impuesto=cero, descuento=cero, asistentes=1), Decimal('200.00'))

    # Verifica que las conversiones nuevas mantengan las restricciones.
    def test_tasas_invalidas(self):
        # Recorre entradas fuera del contrato de las tasas.
        for valor in (True, False, '-0.1', '1.1', 'NaN', 'Infinity', None, 'abc'):
            # Todas deben fallar con una excepción de validación.
            with self.subTest(valor=valor), self.assertRaises(ValidacionError):
                # Aplica directamente el validador compartido.
                porcentaje(valor, 'Impuesto')

if __name__ == '__main__':
    # Invoca unittest.main con los argumentos indicados.
    unittest.main()
