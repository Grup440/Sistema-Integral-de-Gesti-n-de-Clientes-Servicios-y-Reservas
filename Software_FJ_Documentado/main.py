"""Punto de entrada. Python 3.10+; únicamente biblioteca estándar."""
# Importa los módulos argparse.
import argparse
# Importa de pathlib los elementos Path.
from pathlib import Path
# Importa de fj.gestion los elementos Gestor, Registro.
from fj.gestion import Gestor, Registro
# Importa de fj.modelos los elementos Sala, Equipo, Asesoria, ValidacionError.
from fj.modelos import Sala, Equipo, Asesoria, ValidacionError
# Importa de fj.demo los elementos simular.
from fj.demo import simular

# Define la operación mostrar.
def mostrar(objetos):
    # Evalúa la condición: not objetos.
    if not objetos:
        # Invoca print con los argumentos indicados.
        print('Sin registros.')
    # Recorre objetos y asigna cada elemento a objeto.
    for objeto in objetos:
        # Invoca print con los argumentos indicados.
        print(objeto.describir())

# Define la operación menu.
def menu(g):
    # Repite el bloque mientras se cumpla: True.
    while True:
        # Invoca print con los argumentos indicados.
        print('\nSOFTWARE FJ | 1 Cliente | 2 Servicio | 3 Reserva | 4 Confirmar | 5 Procesar | 6 Cancelar | 7 Listar | 8 Disponibilidad | 0 Salir')
        # Inicia un bloque cuyas excepciones se gestionan a continuación.
        try:
            # Asigna a opcion el resultado de la expresión indicada.
            opcion = input('Opción: ').strip()
            # Evalúa la condición: opcion == '0'.
            if opcion == '0':
                # Devuelve el control al llamador.
                return

            # Define la operación accion.
            def accion():
                # Evalúa la condición: opcion == '1'.
                if opcion == '1':
                    # Devuelve g.registrar_cliente(documento=input('Documento: '), nombre=input('Nombre: '), correo=input('Correo: '), telefono=input('Teléfono: ')).
                    return g.registrar_cliente(documento=input('Documento: '), nombre=input('Nombre: '), correo=input('Correo: '), telefono=input('Teléfono: '))
                # Evalúa la condición: opcion == '2'.
                if opcion == '2':
                    # Asigna a tipo el resultado de la expresión indicada.
                    tipo = input('Tipo: sala/equipo/asesoria: ').strip().lower()
                    # Asigna a (nombre, tarifa) el resultado de la expresión indicada.
                    nombre, tarifa = (input('Nombre: '), input('Tarifa por hora: '))
                    # Evalúa la condición: tipo == 'sala'.
                    if tipo == 'sala':
                        # Asigna a s el resultado de la expresión indicada.
                        s = Sala(nombre, tarifa, input('Capacidad: '))
                    # Evalúa la condición: tipo == 'equipo'.
                    elif tipo == 'equipo':
                        # Asigna a s el resultado de la expresión indicada.
                        s = Equipo(nombre, tarifa, input('Unidades: '))
                    # Evalúa la condición: tipo == 'asesoria'.
                    elif tipo == 'asesoria':
                        # Asigna a s el resultado de la expresión indicada.
                        s = Asesoria(nombre, tarifa, input('Especialidad: '))
                    # Ejecuta la alternativa; en un try, solo se alcanza si no hubo excepción.
                    else:
                        # Lanza la excepción indicada para detener esta operación.
                        raise ValidacionError('Tipo de servicio desconocido.')
                    # Devuelve g.agregar_servicio(s).
                    return g.agregar_servicio(s)
                # Evalúa la condición: opcion == '3'.
                if opcion == '3':
                    # Invoca mostrar con los argumentos indicados.
                    mostrar(g.clientes)
                    # Asigna a c el resultado de la expresión indicada.
                    c = input('ID cliente: ')
                    # Invoca mostrar con los argumentos indicados.
                    mostrar(g.servicios)
                    # Asigna a s el resultado de la expresión indicada.
                    s = g.buscar('servicio', input('ID servicio: '))
                    # Asigna a duracion el resultado de la expresión indicada.
                    duracion = input('Duración en horas (máximo 24): ')
                    # Evalúa la condición: isinstance(s, Sala).
                    if isinstance(s, Sala):
                        # Asigna a p el resultado de la expresión indicada.
                        p = {'asistentes': input('Asistentes: ')}
                    # Evalúa la condición: isinstance(s, Equipo).
                    elif isinstance(s, Equipo):
                        # Asigna a p el resultado de la expresión indicada.
                        p = {'cantidad': input('Cantidad: ')}
                    # Ejecuta la alternativa; en un try, solo se alcanza si no hubo excepción.
                    else:
                        # Asigna a p el resultado de la expresión indicada.
                        p = {'tema': input('Tema: ')}
                    # Asigna a p['impuesto'] el resultado de la expresión indicada.
                    p['impuesto'] = input('Impuesto (0.19 para 19%; vacío=0): ') or '0'
                    # Asigna a p['descuento'] el resultado de la expresión indicada.
                    p['descuento'] = input('Descuento (0.10 para 10%; vacío=0): ') or '0'
                    # Devuelve g.crear_reserva(c, s.id, duracion, **p).
                    return g.crear_reserva(c, s.id, duracion, **p)
                # Evalúa la condición: opcion in ('4', '5', '6').
                if opcion in ('4', '5', '6'):
                    # Invoca mostrar con los argumentos indicados.
                    mostrar(g.reservas)
                    # Asigna a r el resultado de la expresión indicada.
                    r = g.buscar('reserva', input('ID reserva: '))
                    # Devuelve {'4': r.confirmar, '5': r.procesar, '6': r.cancelar}[opcion]().
                    return {'4': r.confirmar, '5': r.procesar, '6': r.cancelar}[opcion]()
                # Evalúa la condición: opcion == '7'.
                if opcion == '7':
                    # Recorre [('CLIENTES', g.clientes), ('SERVICIOS', g.servicios), ('RESERVAS', g.reservas)] y asigna cada elemento a (nombre, objetos).
                    for nombre, objetos in [('CLIENTES', g.clientes), ('SERVICIOS', g.servicios), ('RESERVAS', g.reservas)]:
                        # Invoca print con los argumentos indicados.
                        print(nombre)
                        # Invoca mostrar con los argumentos indicados.
                        mostrar(objetos)
                    # Devuelve el control al llamador.
                    return
                # Evalúa la condición: opcion == '8'.
                if opcion == '8':
                    # Invoca mostrar con los argumentos indicados.
                    mostrar(g.servicios)
                    # Asigna a s el resultado de la expresión indicada.
                    s = g.buscar('servicio', input('ID servicio: '))
                    # Asigna a respuesta el resultado de la expresión indicada.
                    respuesta = input('Disponible (s/n): ').strip().lower()
                    # Evalúa la condición: respuesta not in ('s', 'n').
                    if respuesta not in ('s', 'n'):
                        # Lanza la excepción indicada para detener esta operación.
                        raise ValidacionError('Responda s o n.')
                    # Devuelve s.cambiar_disponibilidad(respuesta == 's').
                    return s.cambiar_disponibilidad(respuesta == 's')
                # Lanza la excepción indicada para detener esta operación.
                raise ValidacionError('Opción inválida.')
            # Asigna a (ok, resultado) el resultado de la expresión indicada.
            ok, resultado = g.ejecutar('Menú ' + opcion, accion)
            # Evalúa la condición: ok and resultado is not None.
            if ok and resultado is not None:
                # Invoca print con los argumentos indicados.
                print(resultado.describir())
        # Captura (EOFError, KeyboardInterrupt) y ejecuta su tratamiento.
        except (EOFError, KeyboardInterrupt):
            # Invoca g.registro.evento con los argumentos indicados.
            g.registro.evento('Salida solicitada desde teclado')
            # Invoca print con los argumentos indicados.
            print('\nSesión finalizada.')
            # Devuelve el control al llamador.
            return

# Define la operación main.
def main():
    # Asigna a parser el resultado de la expresión indicada.
    parser = argparse.ArgumentParser(description='Gestión de clientes, servicios y reservas de Software FJ')
    # Invoca parser.add_argument con los argumentos indicados.
    parser.add_argument('--demo', action='store_true', help='Ejecuta 31 operaciones de demostración y termina')
    # Asigna a args el resultado de la expresión indicada.
    args = parser.parse_args()
    # Asigna a registro el resultado de la expresión indicada.
    registro = Registro(Path(__file__).resolve().parent / 'logs' / 'software_fj.log')
    # Inicia un bloque cuyas excepciones se gestionan a continuación.
    try:
        # Asigna a g el resultado de la expresión indicada.
        g = Gestor(registro)
        # Evalúa la condición: args.demo.
        if args.demo:
            # Devuelve 0 if simular(g) else 1.
            return 0 if simular(g) else 1
        # Invoca menu con los argumentos indicados.
        menu(g)
        # Devuelve 0.
        return 0
    # Ejecuta la limpieza o contabilización incluso cuando ocurre una excepción.
    finally:
        # Invoca registro.evento con los argumentos indicados.
        registro.evento('Cierre de aplicación')
        # Invoca registro.cerrar con los argumentos indicados.
        registro.cerrar()
# Evalúa la condición: __name__ == '__main__'.
if __name__ == '__main__':
    # Lanza la excepción indicada para detener esta operación.
    raise SystemExit(main())
