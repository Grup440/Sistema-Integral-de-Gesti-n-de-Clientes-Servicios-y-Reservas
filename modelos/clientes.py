from modelos.entidades import Entidad
from modelos.excepciones import ClienteInvalidoError

class Cliente(Entidad):

    def __init__(self, id, nombre, correo):
        super().__init__(id)

        if not nombre.strip():
            raise ClienteInvalidoError(
                "El nombre no puede estar vacío"
            )

        if "@" not in correo:
            raise ClienteInvalidoError(
                "El correo no es válido"
            )

        self.__nombre = nombre
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"
