# -*- coding: utf-8 -*-
# Archivo: excepciones.py
# Define las excepciones personalizadas del sistema Sofware Fase4-213023-655.


# Clase base: todas las excepciones del sistema heredan de ella (herencia).
# Exception es la clase que Python ofrece para crear errores propios.
class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""
    # No necesita más código: solo sirve de "padre" para las demás.


# Se lanza cuando los datos de un cliente no son válidos.
class ClienteInvalidoError(SoftwareFJError):
    """Nombre, correo o teléfono inválidos."""


# Se lanza cuando los parámetros de un servicio son incorrectos.
class ServicioInvalidoError(SoftwareFJError):
    """Tarifa, horas o datos del servicio fuera de rango."""


# Se lanza cuando se intenta reservar un servicio no disponible.
class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no está disponible para reservar."""


# Se lanza cuando una operación de reserva no está permitida.
class ReservaError(SoftwareFJError):
    """Reserva incorrecta o estado no permitido."""


# Se lanza cuando un cálculo de costos es inconsistente.
class CalculoError(SoftwareFJError):
    """Impuesto o descuento inválidos, o costo negativo."""