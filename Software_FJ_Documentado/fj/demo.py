"""Simulación reproducible: éxitos, errores esperados y recuperación inesperada."""
# Importa de decimal los elementos Decimal.
from decimal import Decimal
# Importa de modelos los elementos Sala, Equipo, Asesoria.
from .modelos import Sala, Equipo, Asesoria

# Define la operación simular.
def simular(g):
    # Asigna a (contexto, resultados) el resultado de la expresión indicada.
    contexto, resultados = ({}, [])

    # Define la operación paso.
    def paso(nombre, accion, exito=True, clave=None):
        # Asigna a (ok, valor) el resultado de la expresión indicada.
        ok, valor = g.ejecutar(nombre, accion)
        # Invoca resultados.append con los argumentos indicados.
        resultados.append(ok == exito)
        # Evalúa la condición: ok and clave.
        if ok and clave:
            # Asigna a contexto[clave] el resultado de la expresión indicada.
            contexto[clave] = valor

    # Define la operación cliente.
    def cliente(**cambios):
        # Asigna a datos el resultado de la expresión indicada.
        datos = dict(documento='100001', nombre='Ana Torres', correo='ana@example.com', telefono='3001234567')
        # Invoca datos.update con los argumentos indicados.
        datos.update(cambios)
        # Devuelve g.registrar_cliente(**datos).
        return g.registrar_cliente(**datos)
    # Invoca paso con los argumentos indicados.
    paso('Registrar cliente válido', cliente, clave='c')
    # Invoca paso con los argumentos indicados.
    paso('Rechazar correo inválido', lambda: cliente(documento='100002', correo='incorrecto'), False)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar documento duplicado', cliente, False)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar parámetros faltantes', lambda: g.registrar_cliente(), False)
    # Invoca paso con los argumentos indicados.
    paso('Crear sala', lambda: g.agregar_servicio(Sala('Sala Norte', 50000, 10)), clave='s')
    # Invoca paso con los argumentos indicados.
    paso('Crear equipo', lambda: g.agregar_servicio(Equipo('Proyector', 20000, 3)), clave='e')
    # Invoca paso con los argumentos indicados.
    paso('Crear asesoría', lambda: g.agregar_servicio(Asesoria('Consultoría', 80000, 'Sistemas')), clave='a')
    # Invoca paso con los argumentos indicados.
    paso('Rechazar tarifa negativa', lambda: g.agregar_servicio(Sala('Inválida', -1, 10)), False)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar capacidad fraccionaria', lambda: Sala('Inválida', 100, 2.5), False)
    # Invoca paso con los argumentos indicados.
    paso('Costo con impuesto y descuento', lambda: contexto['s'].calcular_costo(2, impuesto='.19', descuento='.10', asistentes=5))
    # Invoca paso con los argumentos indicados.
    paso('Rechazar cálculo no finito', lambda: contexto['s'].calcular_costo('NaN', asistentes=5), False)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar descuento fuera de rango', lambda: contexto['s'].calcular_costo(2, descuento=2, asistentes=5), False)

    # Define la operación reservar.
    def reservar(clave, duracion=2, **p):
        # Devuelve g.crear_reserva(contexto['c'].id, contexto[clave].id, duracion, **p).
        return g.crear_reserva(contexto['c'].id, contexto[clave].id, duracion, **p)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar exceso de asistentes', lambda: reservar('s', asistentes=20), False)
    # Invoca paso con los argumentos indicados.
    paso('Crear reserva de sala', lambda: reservar('s', asistentes=5), clave='r')
    # Invoca paso con los argumentos indicados.
    paso('Rechazar doble reserva activa', lambda: reservar('s', asistentes=2), False)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar procesamiento sin confirmar', lambda: contexto['r'].procesar(), False)
    # Invoca paso con los argumentos indicados.
    paso('Confirmar reserva', lambda: contexto['r'].confirmar())
    # Invoca paso con los argumentos indicados.
    paso('Procesar reserva', lambda: contexto['r'].procesar())
    # Invoca paso con los argumentos indicados.
    paso('Rechazar cancelación posterior al proceso', lambda: contexto['r'].cancelar(), False)
    # Invoca paso con los argumentos indicados.
    paso('Rechazar cantidad de equipos excesiva', lambda: reservar('e', cantidad=4), False)
    # Invoca paso con los argumentos indicados.
    paso('Reservar equipos', lambda: reservar('e', cantidad=2), clave='re')
    # Invoca paso con los argumentos indicados.
    paso('Cancelar equipos', lambda: contexto['re'].cancelar())
    # Invoca paso con los argumentos indicados.
    paso('Reservar asesoría', lambda: reservar('a', tema='Arquitectura'), clave='ra')
    # Invoca paso con los argumentos indicados.
    paso('Confirmar asesoría', lambda: contexto['ra'].confirmar())
    # Invoca paso con los argumentos indicados.
    paso('Deshabilitar asesoría', lambda: contexto['a'].cambiar_disponibilidad(False))
    # Invoca paso con los argumentos indicados.
    paso('Error encadenado al procesar servicio deshabilitado', lambda: contexto['ra'].procesar(), False)
    # Invoca paso con los argumentos indicados.
    paso('Habilitar asesoría', lambda: contexto['a'].cambiar_disponibilidad(True))
    # Invoca paso con los argumentos indicados.
    paso('Procesar asesoría recuperada', lambda: contexto['ra'].procesar())
    # Invoca paso con los argumentos indicados.
    paso('Rechazar cliente inexistente', lambda: g.crear_reserva('inexistente', contexto['s'].id, 2, asistentes=1), False)

    # Define la operación inesperado.
    def inesperado():
        # Lanza la excepción indicada para detener esta operación.
        raise RuntimeError('Fallo técnico simulado para probar la frontera exterior')
    # Invoca paso con los argumentos indicados.
    paso('Recuperar fallo técnico inesperado', inesperado, False)
    # Invoca paso con los argumentos indicados.
    paso('Continuar después del fallo grave', lambda: cliente(documento='100003', nombre='Luis Pérez'))
    # Comprueba la condición esperada y señala una discrepancia si no se cumple.
    assert contexto['s'].calcular_costo(2, impuesto='.19', descuento='.10', asistentes=5) == Decimal('107100.00')
    # Invoca print con los argumentos indicados.
    print(f'\nSIMULACIÓN: {len(resultados)} operaciones; {sum(resultados)} resultados coinciden con lo esperado.')
    # Devuelve all(resultados).
    return all(resultados)
