from abc import ABC, abstractmethod
from modelos.excepciones import ServicioInvalidoError


class Servicio(ABC):

    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


class Sala(Servicio):

    def __init__(self, nombre, costo_hora):
        super().__init__(nombre)

        if costo_hora <= 0:
            raise ServicioInvalidoError(
                "Costo por hora inválido"
            )

        self.costo_hora = costo_hora

    def calcular_costo(self, horas=1):
        return self.costo_hora * horas

    def descripcion(self):
        return "Reserva de salas empresariales"


class Equipo(Servicio):

    def __init__(self, nombre, costo_dia):
        super().__init__(nombre)

        if costo_dia <= 0:
            raise ServicioInvalidoError(
                "Costo por día inválido"
            )

        self.costo_dia = costo_dia

    def calcular_costo(self, dias=1):
        return self.costo_dia * dias

    def descripcion(self):
        return "Alquiler de equipos tecnológicos"


class Asesoria(Servicio):

    def __init__(self, nombre, tarifa_hora):
        super().__init__(nombre)

        if tarifa_hora <= 0:
            raise ServicioInvalidoError(
                "Tarifa inválida"
            )

        self.tarifa_hora = tarifa_hora

    def calcular_costo(self, horas=1):
        return self.tarifa_hora * horas

    def descripcion(self):
        return "Asesoría especializada"