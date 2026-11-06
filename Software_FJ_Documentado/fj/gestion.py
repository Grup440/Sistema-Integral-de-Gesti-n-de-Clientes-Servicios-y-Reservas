"""Coordinación y frontera de recuperación de errores de la aplicación."""
# Importa los módulos logging.
import logging
# Importa los módulos sys.
import sys
# Importa de pathlib los elementos Path.
from pathlib import Path
# Importa de modelos los elementos Cliente, Servicio, Reserva, ErrorSistema, DuplicadoError, NoEncontradoError, ValidacionError, Estado.
from .modelos import Cliente, Servicio, Reserva, ErrorSistema, DuplicadoError, NoEncontradoError, ValidacionError, Estado

# Define la clase Registro.
class Registro:

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, ruta):
        # Asigna a self.logger el resultado de la expresión indicada.
        self.logger = logging.getLogger('software_fj.' + str(id(self)))
        # Invoca self.logger.setLevel con los argumentos indicados.
        self.logger.setLevel(logging.INFO)
        # Asigna a self.logger.propagate el resultado de la expresión indicada.
        self.logger.propagate = False
        # Inicia un bloque cuyas excepciones se gestionan a continuación.
        try:
            # Asigna a ruta el resultado de la expresión indicada.
            ruta = Path(ruta)
            # Invoca ruta.parent.mkdir con los argumentos indicados.
            ruta.parent.mkdir(parents=True, exist_ok=True)
            # Asigna a manejador el resultado de la expresión indicada.
            manejador = logging.FileHandler(ruta, encoding='utf-8')
        # Captura OSError y ejecuta su tratamiento.
        except OSError as causa:
            # Invoca print con los argumentos indicados.
            print(f'No se pudo abrir el log ({causa.__class__.__name__}); se usará consola.', file=sys.stderr)
            # Asigna a manejador el resultado de la expresión indicada.
            manejador = logging.StreamHandler(sys.stderr)
        # Invoca manejador.setFormatter con los argumentos indicados.
        manejador.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        # Invoca self.logger.addHandler con los argumentos indicados.
        self.logger.addHandler(manejador)

    # Define la operación evento.
    def evento(self, mensaje):
        # Invoca self.logger.info con los argumentos indicados.
        self.logger.info(mensaje)

    # Define la operación error.
    def error(self, mensaje):
        # Invoca self.logger.exception con los argumentos indicados.
        self.logger.exception(mensaje)

    # Define la operación cerrar.
    def cerrar(self):
        # Recorre self.logger.handlers[:] y asigna cada elemento a manejador.
        for manejador in self.logger.handlers[:]:
            # Invoca manejador.close con los argumentos indicados.
            manejador.close()
            # Invoca self.logger.removeHandler con los argumentos indicados.
            self.logger.removeHandler(manejador)

# Define la clase Gestor.
class Gestor:

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, registro):
        # Asigna a self.registro el resultado de la expresión indicada.
        self.registro = registro
        # Asigna a (self.__clientes, self.__servicios, self.__reservas) el resultado de la expresión indicada.
        self.__clientes, self.__servicios, self.__reservas = ([], [], [])
        # Asigna a self.operaciones el resultado de la expresión indicada.
        self.operaciones = 0

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación clientes.
    def clientes(self):
        # Devuelve tuple(self.__clientes).
        return tuple(self.__clientes)

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación servicios.
    def servicios(self):
        # Devuelve tuple(self.__servicios).
        return tuple(self.__servicios)

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación reservas.
    def reservas(self):
        # Devuelve tuple(self.__reservas).
        return tuple(self.__reservas)

    # Ejecuta una operación con registro de éxitos, errores y finalización.
    def ejecutar(self, descripcion, accion):
        """Toda operación del menú/demo pasa por esta frontera; no registra datos personales."""
        # Inicia un bloque cuyas excepciones se gestionan a continuación.
        try:
            # Asigna a resultado el resultado de la expresión indicada.
            resultado = accion()
        # Captura (ErrorSistema, ValueError, TypeError, ArithmeticError) y ejecuta su tratamiento.
        except (ErrorSistema, ValueError, TypeError, ArithmeticError) as error:
            # Invoca self.registro.error con los argumentos indicados.
            self.registro.error(f'Operación rechazada: {descripcion}')
            # Invoca print con los argumentos indicados.
            print(f'[CONTROLADO] {descripcion}: {error}')
            # Devuelve (False, None).
            return (False, None)
        # Captura Exception y ejecuta su tratamiento.
        except Exception as error:
            # Invoca self.registro.error con los argumentos indicados.
            self.registro.error(f'Error inesperado: {descripcion}')
            # Invoca print con los argumentos indicados.
            print(f'[RECUPERADO] {descripcion}: {type(error).__name__}. Consulte el log.')
            # Devuelve (False, None).
            return (False, None)
        # Ejecuta la alternativa; en un try, solo se alcanza si no hubo excepción.
        else:
            # Invoca self.registro.evento con los argumentos indicados.
            self.registro.evento(f'Operación correcta: {descripcion}')
            # Invoca print con los argumentos indicados.
            print(f'[OK] {descripcion}')
            # Devuelve (True, resultado).
            return (True, resultado)
        # Ejecuta la limpieza o contabilización incluso cuando ocurre una excepción.
        finally:
            # Actualiza self.operaciones con la operación indicada.
            self.operaciones += 1
            # Invoca self.registro.evento con los argumentos indicados.
            self.registro.evento(f'Fin de operación #{self.operaciones}')

    # Valida y agrega un cliente si su documento no está registrado.
    def registrar_cliente(self, **datos):
        # Asigna a cliente el resultado de la expresión indicada.
        cliente = Cliente(**datos)
        # Evalúa la condición: any((c.documento == cliente.documento for c in self.clientes)).
        if any((c.documento == cliente.documento for c in self.clientes)):
            # Lanza la excepción indicada para detener esta operación.
            raise DuplicadoError('El documento ya está registrado.')
        # Invoca self.__clientes.append con los argumentos indicados.
        self.__clientes.append(cliente)
        # Devuelve cliente.
        return cliente

    # Define la operación agregar_servicio.
    def agregar_servicio(self, servicio):
        # Evalúa la condición: not isinstance(servicio, Servicio).
        if not isinstance(servicio, Servicio):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Servicio inválido.')
        # Evalúa la condición: any((s.nombre.casefold() == servicio.nombre.casefold() for s in self.servicios)).
        if any((s.nombre.casefold() == servicio.nombre.casefold() for s in self.servicios)):
            # Lanza la excepción indicada para detener esta operación.
            raise DuplicadoError('Nombre de servicio duplicado.')
        # Invoca self.__servicios.append con los argumentos indicados.
        self.__servicios.append(servicio)
        # Devuelve servicio.
        return servicio

    # Define la operación buscar.
    def buscar(self, tipo, identificador):
        # Asigna a colecciones el resultado de la expresión indicada.
        colecciones = {'cliente': self.clientes, 'servicio': self.servicios, 'reserva': self.reservas}
        # Evalúa la condición: tipo not in colecciones.
        if tipo not in colecciones:
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Tipo de búsqueda inválido.')
        # Recorre colecciones[tipo] y asigna cada elemento a objeto.
        for objeto in colecciones[tipo]:
            # Evalúa la condición: objeto.id == identificador.
            if objeto.id == identificador:
                # Devuelve objeto.
                return objeto
        # Lanza la excepción indicada para detener esta operación.
        raise NoEncontradoError(f'No existe {tipo} con ese identificador.')

    # Relaciona entidades registradas y rechaza servicios con otra reserva activa.
    def crear_reserva(self, cliente_id, servicio_id, duracion, **parametros):
        # Asigna a cliente el resultado de la expresión indicada.
        cliente = self.buscar('cliente', cliente_id)
        # Asigna a servicio el resultado de la expresión indicada.
        servicio = self.buscar('servicio', servicio_id)
        # Evalúa la condición: any((r.servicio is servicio and r.estado in (Estado.PENDIENTE, Estado.CONFIRMADA) for r in self.reservas)).
        if any((r.servicio is servicio and r.estado in (Estado.PENDIENTE, Estado.CONFIRMADA) for r in self.reservas)):
            # Importa de modelos los elementos NoDisponibleError.
            from .modelos import NoDisponibleError
            # Lanza la excepción indicada para detener esta operación.
            raise NoDisponibleError('El servicio ya tiene una reserva activa.')
        # Asigna a reserva el resultado de la expresión indicada.
        reserva = Reserva(cliente, servicio, duracion, **parametros)
        # Invoca self.__reservas.append con los argumentos indicados.
        self.__reservas.append(reserva)
        # Devuelve reserva.
        return reserva
