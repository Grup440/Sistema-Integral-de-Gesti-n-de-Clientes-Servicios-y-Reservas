from modelos.excepciones import ReservaError

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ReservaError(
                "La duración debe ser mayor que cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):

        try:
            costo = self.servicio.calcular_costo(
                self.duracion
            )

        except Exception as e:
            raise ReservaError(
                "Error al procesar la reserva"
            ) from e

        return costo

    def mostrar_reserva(self):
        return (f"Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | "
                f"Estado: {self.estado}")

