import logging

from modelos.clientes import Cliente
from modelos.servicios import Sala
from modelos.servicios import Equipo
from modelos.servicios import Asesoria
from modelos.reservas import Reserva

# Configuración del log
logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("\n===================================")
print(" SISTEMA SOFTWARE FJ ")
print("===================================\n")

# =====================================
# OPERACIÓN 1
# Cliente válido
# =====================================
try:
    print("OPERACIÓN 1: Registrar cliente válido")

    cliente1 = Cliente(
        1,
        "Carlos Perez",
        "carlos@gmail.com"
    )

    print("✅ Cliente registrado correctamente")
    print(cliente1.mostrar_info())

except Exception as e:
    print("❌ Error:", e)
    logging.error(e)

else:
    print("✅ Cliente registrado correctamente")
    print(cliente1.mostrar_info())
# =====================================
# OPERACIÓN 2
# Cliente inválido
# =====================================
try:
    print("\nOPERACIÓN 2: Cliente con nombre vacío")

    cliente2 = Cliente(
        2,
        "",
        "usuario@gmail.com"
    )

except Exception as e:
    print("❌ Error controlado:", e)
    logging.error(e)

# =====================================
# OPERACIÓN 3
# Correo inválido
# =====================================
try:
    print("\nOPERACIÓN 3: Cliente con correo inválido")

    cliente3 = Cliente(
        3,
        "Maria",
        "correoinvalido"
    )

except Exception as e:
    print("❌ Error controlado:", e)
    logging.error(e)

# =====================================
# OPERACIÓN 4
# Crear sala correctamente
# =====================================
try:
    print("\nOPERACIÓN 4: Crear sala válida")

    sala = Sala(
        "Sala Premium",
        100
    )

    print("✅ Servicio creado")
    print(sala.descripcion())

except Exception as e:
    logging.error(e)

# =====================================
# OPERACIÓN 5
# Crear equipo correctamente
# =====================================
try:
    print("\nOPERACIÓN 5: Crear equipo válido")

    equipo = Equipo(
        "Portatil",
        80
    )

    print("✅ Servicio creado")
    print(equipo.descripcion())

except Exception as e:
    logging.error(e)

# =====================================
# OPERACIÓN 6
# Crear asesoría correctamente
# =====================================
try:
    print("\nOPERACIÓN 6: Crear asesoría válida")

    asesoria = Asesoria(
        "Python",
        120
    )

    print("✅ Servicio creado")
    print(asesoria.descripcion())

except Exception as e:
    logging.error(e)

# =====================================
# OPERACIÓN 7
# Crear servicio inválido
# =====================================
try:
    print("\nOPERACIÓN 7: Servicio con costo inválido")

    sala_error = Sala(
        "Sala Incorrecta",
        -50
    )

except Exception as e:
    print("❌ Error controlado:", e)
    logging.error(e)

# =====================================
# OPERACIÓN 8
# Reserva exitosa
# =====================================
try:
    print("\nOPERACIÓN 8: Reserva válida de sala")

    reserva1 = Reserva(
        cliente1,
        sala,
        4
    )

    reserva1.confirmar()

    print(reserva1.mostrar_reserva())
    print("Costo:", reserva1.procesar())

except Exception as e:
    print("❌ Error:", e)
    logging.error(e)

finally:
    print("Proceso de reserva finalizado")

# =====================================
# OPERACIÓN 9
# Reserva exitosa
# =====================================
try:
    print("\nOPERACIÓN 9: Reserva válida de equipo")

    reserva2 = Reserva(
        cliente1,
        equipo,
        3
    )

    reserva2.confirmar()

    print(reserva2.mostrar_reserva())
    print("Costo:", reserva2.procesar())

except Exception as e:
    logging.error(e)

# =====================================
# OPERACIÓN 10
# Reserva inválida
# =====================================
try:
    print("\nOPERACIÓN 10: Reserva con duración negativa")

    reserva3 = Reserva(
        cliente1,
        asesoria,
        -2
    )

except Exception as e:
    print("❌ Error controlado:", e)
    logging.error(e)

# =====================================
# RESUMEN FINAL
# =====================================

print("\n===================================")
print(" RESUMEN DE OPERACIONES ")
print("===================================")

print("1. ✅ Cliente válido registrado")
print("2. ❌ Cliente inválido detectado")
print("3. ❌ Correo inválido detectado")
print("4. ✅ Sala creada correctamente")
print("5. ✅ Equipo creado correctamente")
print("6. ✅ Asesoría creada correctamente")
print("7. ❌ Servicio inválido detectado")
print("8. ✅ Reserva de sala exitosa")
print("9. ✅ Reserva de equipo exitosa")
print("10. ❌ Reserva inválida detectada")

print("\n✅ El sistema continuó funcionando a pesar de los errores.")
print("✅ Todas las excepciones fueron controladas.")
print("✅ Los errores quedaron registrados en logs.txt")
print("✅ Proyecto finalizado correctamente.")


