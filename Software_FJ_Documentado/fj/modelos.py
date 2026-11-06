"""Modelo de dominio: objetos en memoria, sin persistencia de datos personales."""
# Importa de abc los elementos ABC, abstractmethod.
from abc import ABC, abstractmethod
# Importa de decimal los elementos Decimal, InvalidOperation, ROUND_HALF_UP.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
# Importa de enum los elementos Enum.
from enum import Enum
# Importa los módulos re.
import re
# Importa de uuid los elementos uuid4.
from uuid import uuid4

# Define la clase ErrorSistema, que hereda de Exception.
class ErrorSistema(Exception):
    """Base de errores de negocio controlables."""

# Define la clase ValidacionError, que hereda de ErrorSistema.
class ValidacionError(ErrorSistema):
    # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
    pass

# Define la clase NoDisponibleError, que hereda de ErrorSistema.
class NoDisponibleError(ErrorSistema):
    # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
    pass

# Define la clase EstadoError, que hereda de ErrorSistema.
class EstadoError(ErrorSistema):
    # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
    pass

# Define la clase NoEncontradoError, que hereda de ErrorSistema.
class NoEncontradoError(ErrorSistema):
    # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
    pass

# Define la clase DuplicadoError, que hereda de ErrorSistema.
class DuplicadoError(ErrorSistema):
    # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
    pass

# Define la clase CalculoError, que hereda de ErrorSistema.
class CalculoError(ErrorSistema):
    # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
    pass

# Convierte y valida un número finito dentro del rango admitido.
def numero(valor, campo, minimo=Decimal('0'), maximo=None):
    # Inicia un bloque cuyas excepciones se gestionan a continuación.
    try:
        # Evalúa la condición: isinstance(valor, bool).
        if isinstance(valor, bool):
            # Lanza la excepción indicada para detener esta operación.
            raise ValueError('Los booleanos no son números de negocio')
        # Asigna a resultado el resultado de la expresión indicada.
        resultado = Decimal(str(valor))
        # Evalúa la condición: not resultado.is_finite() or resultado <= minimo.
        if not resultado.is_finite() or resultado <= minimo:
            # Lanza la excepción indicada para detener esta operación.
            raise ValueError('Fuera del rango permitido')
        # Evalúa la condición: maximo is not None and resultado > maximo.
        if maximo is not None and resultado > maximo:
            # Lanza la excepción indicada para detener esta operación.
            raise ValueError('Supera el máximo permitido')
    # Captura (InvalidOperation, ValueError, TypeError) y ejecuta su tratamiento.
    except (InvalidOperation, ValueError, TypeError) as causa:
        # Lanza la excepción indicada y conserva su causa original.
        raise ValidacionError(f'{campo}: valor inválido.') from causa
    # Devuelve resultado.
    return resultado

# Exige texto no vacío y retira espacios de los extremos.
def texto(valor, campo):
    # Evalúa la condición: not isinstance(valor, str) or not valor.strip().
    if not isinstance(valor, str) or not valor.strip():
        # Lanza la excepción indicada para detener esta operación.
        raise ValidacionError(f'{campo} es obligatorio.')
    # Devuelve valor.strip().
    return valor.strip()

# Valida una tasa decimal entre cero y uno, incluyendo cero recibido como texto.
def porcentaje(valor, campo):
    # Conserva la causa de errores de conversión para incluirla en el log.
    try:
        # Evita interpretar True y False como tasas numéricas.
        if isinstance(valor, bool):
            # Rechaza un tipo incompatible con una tasa de negocio.
            raise ValueError('Una tasa no puede ser booleana')
        # Convierte también los valores escritos en el menú, por ejemplo "0".
        tasa = Decimal(str(valor))
        # Exige un número finito dentro del intervalo cerrado [0, 1].
        if not tasa.is_finite() or not Decimal('0') <= tasa <= Decimal('1'):
            # Señala valores negativos, mayores de uno o no finitos.
            raise ValueError('Tasa fuera de rango')
    # Captura las conversiones inválidas y las tasas rechazadas.
    except (InvalidOperation, ValueError, TypeError) as causa:
        # Encadena el error de dominio a la causa original.
        raise ValidacionError(f'{campo}: use una tasa entre 0 y 1.') from causa
    # Devuelve la tasa validada sin redondearla prematuramente.
    return tasa

# Define la clase Entidad, que hereda de ABC.
class Entidad(ABC):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self):
        # Asigna a self.__id el resultado de la expresión indicada.
        self.__id = uuid4().hex[:12]

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación id.
    def id(self):
        # Devuelve self.__id.
        return self.__id

    # Obliga a las clases concretas a implementar este método.
    @abstractmethod
    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
        pass

# Define la clase Cliente, que hereda de Entidad.
class Cliente(Entidad):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, documento=None, nombre=None, correo=None, telefono=None):
        # Invoca super().__init__ con los argumentos indicados.
        super().__init__()
        # Asigna a documento el resultado de la expresión indicada.
        documento = texto(documento, 'Documento')
        # Evalúa la condición: not re.fullmatch('\\d{5,15}', documento).
        if not re.fullmatch('\\d{5,15}', documento):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Documento: debe contener entre 5 y 15 dígitos.')
        # Asigna a self.__documento el resultado de la expresión indicada.
        self.__documento = documento
        # Invoca self.actualizar_contacto con los argumentos indicados.
        self.actualizar_contacto(nombre, correo, telefono)

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación documento.
    def documento(self):
        # Devuelve self.__documento.
        return self.__documento

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación nombre.
    def nombre(self):
        # Devuelve self.__nombre.
        return self.__nombre

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación correo.
    def correo(self):
        # Devuelve self.__correo.
        return self.__correo

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación telefono.
    def telefono(self):
        # Devuelve self.__telefono.
        return self.__telefono

    # Valida todos los datos de contacto antes de modificarlos.
    def actualizar_contacto(self, nombre, correo, telefono):
        # Asigna a nombre el resultado de la expresión indicada.
        nombre = texto(nombre, 'Nombre')
        # Asigna a correo el resultado de la expresión indicada.
        correo = texto(correo, 'Correo')
        # Asigna a telefono el resultado de la expresión indicada.
        telefono = texto(telefono, 'Teléfono')
        # Evalúa la condición: len(nombre) < 3 or not all((c.isalpha() or c in " '-" for c in nombre)).
        if len(nombre) < 3 or not all((c.isalpha() or c in " '-" for c in nombre)):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Nombre: mínimo 3 caracteres; use letras.')
        # Evalúa la condición: not re.fullmatch('[^\\s@]+@[^\\s@]+\\.[^\\s@]+', correo).
        if not re.fullmatch('[^\\s@]+@[^\\s@]+\\.[^\\s@]+', correo):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Correo inválido.')
        # Evalúa la condición: not re.fullmatch('\\+?\\d{7,15}', telefono).
        if not re.fullmatch('\\+?\\d{7,15}', telefono):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Teléfono: entre 7 y 15 dígitos, con + opcional.')
        # Asigna a (self.__nombre, self.__correo, self.__telefono) el resultado de la expresión indicada.
        self.__nombre, self.__correo, self.__telefono = (nombre, correo, telefono)

    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Devuelve f'{self.id} | {self.nombre}'.
        return f'{self.id} | {self.nombre}'

# Define la clase Servicio, que hereda de Entidad.
class Servicio(Entidad):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, nombre=None, tarifa=None):
        # Invoca super().__init__ con los argumentos indicados.
        super().__init__()
        # Asigna a self.__nombre el resultado de la expresión indicada.
        self.__nombre = texto(nombre, 'Nombre del servicio')
        # Asigna a self.__tarifa el resultado de la expresión indicada.
        self.__tarifa = numero(tarifa, 'Tarifa por hora')
        # Asigna a self.__disponible el resultado de la expresión indicada.
        self.__disponible = True

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación nombre.
    def nombre(self):
        # Devuelve self.__nombre.
        return self.__nombre

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación tarifa.
    def tarifa(self):
        # Devuelve self.__tarifa.
        return self.__tarifa

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación disponible.
    def disponible(self):
        # Devuelve self.__disponible.
        return self.__disponible

    # Define la operación cambiar_disponibilidad.
    def cambiar_disponibilidad(self, disponible):
        # Evalúa la condición: type(disponible) is not bool.
        if type(disponible) is not bool:
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Disponibilidad debe ser booleana.')
        # Asigna a self.__disponible el resultado de la expresión indicada.
        self.__disponible = disponible

    # Obliga a las clases concretas a implementar este método.
    @abstractmethod
    # Comprueba los parámetros específicos de este tipo de servicio.
    def validar_parametros(self, duracion, **parametros):
        # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
        pass

    # Obliga a las clases concretas a implementar este método.
    @abstractmethod
    # Calcula el valor antes de aplicar descuento e impuesto.
    def calcular_base(self, duracion, **parametros):
        # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
        pass

    # Obliga a las clases concretas a implementar este método.
    @abstractmethod
    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Deja el cuerpo sin implementación adicional; utiliza el contrato o comportamiento heredado.
        pass

    # Calcula el precio con las variantes opcionales de impuesto y descuento.
    def calcular_costo(self, duracion, *, impuesto=0, descuento=0, **parametros):
        """Variantes: base, con impuesto, con descuento o ambos (sobrecarga por opcionales)."""
        # Invoca self.validar_parametros con los argumentos indicados.
        self.validar_parametros(duracion, **parametros)
        # Asigna a impuesto el resultado de la expresión indicada.
        impuesto = porcentaje(impuesto, 'Impuesto')
        # Asigna a descuento el resultado de la expresión indicada.
        descuento = porcentaje(descuento, 'Descuento')
        # Inicia un bloque cuyas excepciones se gestionan a continuación.
        try:
            # Asigna a total el resultado de la expresión indicada.
            total = self.calcular_base(numero(duracion, 'Duración'), **parametros)
            # Asigna a total el resultado de la expresión indicada.
            total = total * (1 - descuento) * (1 + impuesto)
            # Evalúa la condición: not total.is_finite() or total < 0.
            if not total.is_finite() or total < 0:
                # Lanza la excepción indicada para detener esta operación.
                raise ValueError('Resultado inconsistente')
            # Devuelve total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP).
            return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # Captura (InvalidOperation, ArithmeticError, ValueError, TypeError) y ejecuta su tratamiento.
        except (InvalidOperation, ArithmeticError, ValueError, TypeError) as causa:
            # Lanza la excepción indicada y conserva su causa original.
            raise CalculoError('No fue posible calcular el costo.') from causa

    # Define la operación _validar.
    def _validar(self, duracion, parametros, permitidos):
        # Invoca numero con los argumentos indicados.
        numero(duracion, 'Duración en horas', maximo=Decimal('24'))
        # Evalúa la condición: set(parametros) - set(permitidos).
        if set(parametros) - set(permitidos):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Parámetros desconocidos para el servicio.')
        # Evalúa la condición: not self.disponible.
        if not self.disponible:
            # Lanza la excepción indicada para detener esta operación.
            raise NoDisponibleError('Servicio deshabilitado.')

# Define la clase Sala, que hereda de Servicio.
class Sala(Servicio):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, nombre=None, tarifa=None, capacidad=None):
        # Invoca super().__init__ con los argumentos indicados.
        super().__init__(nombre, tarifa)
        # Asigna a self.__capacidad el resultado de la expresión indicada.
        self.__capacidad = int(numero(capacidad, 'Capacidad', maximo=Decimal('500')))
        # Evalúa la condición: Decimal(str(capacidad)) != self.__capacidad.
        if Decimal(str(capacidad)) != self.__capacidad:
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Capacidad debe ser entera.')

    # Comprueba los parámetros específicos de este tipo de servicio.
    def validar_parametros(self, duracion, **parametros):
        # Invoca self._validar con los argumentos indicados.
        self._validar(duracion, parametros, {'asistentes'})
        # Asigna a asistentes el resultado de la expresión indicada.
        asistentes = numero(parametros.get('asistentes'), 'Asistentes', maximo=Decimal(self.__capacidad))
        # Evalúa la condición: asistentes != int(asistentes).
        if asistentes != int(asistentes):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Asistentes debe ser entero.')

    # Calcula el valor antes de aplicar descuento e impuesto.
    def calcular_base(self, duracion, **parametros):
        # Devuelve self.tarifa * duracion.
        return self.tarifa * duracion

    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Devuelve f'{self.id} | Sala: {self.nombre}; capacidad {self.__capacidad}; $ {self.tarifa}/hora'.
        return f'{self.id} | Sala: {self.nombre}; capacidad {self.__capacidad}; $ {self.tarifa}/hora'

# Define la clase Equipo, que hereda de Servicio.
class Equipo(Servicio):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, nombre=None, tarifa=None, unidades=None):
        # Invoca super().__init__ con los argumentos indicados.
        super().__init__(nombre, tarifa)
        # Asigna a cantidad el resultado de la expresión indicada.
        cantidad = numero(unidades, 'Unidades', maximo=Decimal('1000'))
        # Evalúa la condición: cantidad != int(cantidad).
        if cantidad != int(cantidad):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Unidades debe ser entero.')
        # Asigna a self.__unidades el resultado de la expresión indicada.
        self.__unidades = int(cantidad)

    # Comprueba los parámetros específicos de este tipo de servicio.
    def validar_parametros(self, duracion, **parametros):
        # Invoca self._validar con los argumentos indicados.
        self._validar(duracion, parametros, {'cantidad'})
        # Asigna a cantidad el resultado de la expresión indicada.
        cantidad = numero(parametros.get('cantidad'), 'Cantidad', maximo=Decimal(self.__unidades))
        # Evalúa la condición: cantidad != int(cantidad).
        if cantidad != int(cantidad):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Cantidad debe ser entera.')

    # Calcula el valor antes de aplicar descuento e impuesto.
    def calcular_base(self, duracion, **parametros):
        # Devuelve self.tarifa * duracion * Decimal(str(parametros['cantidad'])).
        return self.tarifa * duracion * Decimal(str(parametros['cantidad']))

    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Devuelve f'{self.id} | Equipo: {self.nombre}; unidades {self.__unidades}; $ {self.tarifa}/hora/unidad'.
        return f'{self.id} | Equipo: {self.nombre}; unidades {self.__unidades}; $ {self.tarifa}/hora/unidad'

# Define la clase Asesoria, que hereda de Servicio.
class Asesoria(Servicio):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, nombre=None, tarifa=None, especialidad=None):
        # Invoca super().__init__ con los argumentos indicados.
        super().__init__(nombre, tarifa)
        # Asigna a self.__especialidad el resultado de la expresión indicada.
        self.__especialidad = texto(especialidad, 'Especialidad')

    # Comprueba los parámetros específicos de este tipo de servicio.
    def validar_parametros(self, duracion, **parametros):
        # Invoca self._validar con los argumentos indicados.
        self._validar(duracion, parametros, {'tema'})
        # Invoca texto con los argumentos indicados.
        texto(parametros.get('tema'), 'Tema de asesoría')

    # Calcula el valor antes de aplicar descuento e impuesto.
    def calcular_base(self, duracion, **parametros):
        # Devuelve self.tarifa * duracion.
        return self.tarifa * duracion

    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Devuelve f'{self.id} | Asesoría: {self.nombre}; {self.__especialidad}; $ {self.tarifa}/hora'.
        return f'{self.id} | Asesoría: {self.nombre}; {self.__especialidad}; $ {self.tarifa}/hora'

# Define la clase Estado, que hereda de Enum.
class Estado(Enum):
    # Asigna a PENDIENTE el resultado de la expresión indicada.
    PENDIENTE = 'pendiente'
    # Asigna a CONFIRMADA el resultado de la expresión indicada.
    CONFIRMADA = 'confirmada'
    # Asigna a PROCESADA el resultado de la expresión indicada.
    PROCESADA = 'procesada'
    # Asigna a CANCELADA el resultado de la expresión indicada.
    CANCELADA = 'cancelada'

# Define la clase Reserva, que hereda de Entidad.
class Reserva(Entidad):

    # Inicializa los datos y valida la creación del objeto.
    def __init__(self, cliente=None, servicio=None, duracion=None, *, impuesto=0, descuento=0, **parametros):
        # Invoca super().__init__ con los argumentos indicados.
        super().__init__()
        # Evalúa la condición: not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio).
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            # Lanza la excepción indicada para detener esta operación.
            raise ValidacionError('Se requieren un cliente y un servicio válidos.')
        # Asigna a self.__total el resultado de la expresión indicada.
        self.__total = servicio.calcular_costo(duracion, impuesto=impuesto, descuento=descuento, **parametros)
        # Asigna a (self.__cliente, self.__servicio) el resultado de la expresión indicada.
        self.__cliente, self.__servicio = (cliente, servicio)
        # Asigna a self.__duracion el resultado de la expresión indicada.
        self.__duracion = numero(duracion, 'Duración')
        # Asigna a self.__parametros el resultado de la expresión indicada.
        self.__parametros = dict(parametros)
        # Asigna a self.__estado el resultado de la expresión indicada.
        self.__estado = Estado.PENDIENTE

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación cliente.
    def cliente(self):
        # Devuelve self.__cliente.
        return self.__cliente

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación servicio.
    def servicio(self):
        # Devuelve self.__servicio.
        return self.__servicio

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación duracion.
    def duracion(self):
        # Devuelve self.__duracion.
        return self.__duracion

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación estado.
    def estado(self):
        # Devuelve self.__estado.
        return self.__estado

    # Expone el siguiente método como una propiedad de lectura.
    @property
    # Define la operación total.
    def total(self):
        # Devuelve self.__total.
        return self.__total

    # Confirma la reserva después de comprobar su estado y disponibilidad.
    def confirmar(self):
        # Evalúa la condición: self.estado != Estado.PENDIENTE.
        if self.estado != Estado.PENDIENTE:
            # Lanza la excepción indicada para detener esta operación.
            raise EstadoError('Solo se confirma una reserva pendiente.')
        # Invoca self.servicio.validar_parametros con los argumentos indicados.
        self.servicio.validar_parametros(self.duracion, **self.__parametros)
        # Asigna a self.__estado el resultado de la expresión indicada.
        self.__estado = Estado.CONFIRMADA

    # Cancela una reserva únicamente desde un estado permitido.
    def cancelar(self):
        # Evalúa la condición: self.estado not in (Estado.PENDIENTE, Estado.CONFIRMADA).
        if self.estado not in (Estado.PENDIENTE, Estado.CONFIRMADA):
            # Lanza la excepción indicada para detener esta operación.
            raise EstadoError('No se puede cancelar una reserva cancelada o procesada.')
        # Asigna a self.__estado el resultado de la expresión indicada.
        self.__estado = Estado.CANCELADA

    # Procesa la reserva confirmada y conserva el estado si falla la validación.
    def procesar(self):
        # Evalúa la condición: self.estado != Estado.CONFIRMADA.
        if self.estado != Estado.CONFIRMADA:
            # Lanza la excepción indicada para detener esta operación.
            raise EstadoError('Se debe confirmar antes de procesar.')
        # Inicia un bloque cuyas excepciones se gestionan a continuación.
        try:
            # Invoca self.servicio.validar_parametros con los argumentos indicados.
            self.servicio.validar_parametros(self.duracion, **self.__parametros)
        # Captura ErrorSistema y ejecuta su tratamiento.
        except ErrorSistema as causa:
            # Lanza la excepción indicada y conserva su causa original.
            raise NoDisponibleError('La reserva no puede procesarse actualmente.') from causa
        # Ejecuta la alternativa; en un try, solo se alcanza si no hubo excepción.
        else:
            # Asigna a self.__estado el resultado de la expresión indicada.
            self.__estado = Estado.PROCESADA

    # Devuelve una descripción legible del objeto.
    def describir(self):
        # Devuelve f'{self.id} | {self.cliente.nombre} | {self.servicio.nombre} | {self.duracion} h | {self.estado.value} | $ {self.total}'.
        return f'{self.id} | {self.cliente.nombre} | {self.servicio.nombre} | {self.duracion} h | {self.estado.value} | $ {self.total}'
