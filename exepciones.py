# -*- coding: utf-8 -*-
# Archivo: excepciones.py
# Define las excepciones personalizadas del sistema Software Fase4-213023-655.

class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Nombre, correo o teléfono inválidos."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Tarifa, horas o datos del servicio fuera de rango."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no está disponible para reservar."""
    pass


class ReservaError(SoftwareFJError):
    """Reserva incorrecta o estado no permitido."""
    pass


class CalculoError(SoftwareFJError):
    """Impuesto o descuento inválidos, o costo negativo."""
    pass
