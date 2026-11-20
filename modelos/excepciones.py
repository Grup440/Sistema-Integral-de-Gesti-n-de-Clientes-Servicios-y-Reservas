class ErrorSistema(Exception):
    pass

class ClienteInvalidoError(ErrorSistema):
    pass

class ServicioInvalidoError(ErrorSistema):
    pass

class ReservaError(ErrorSistema):
    pass

class ServicioNoDisponibleError(ErrorSistema):
    pass
    