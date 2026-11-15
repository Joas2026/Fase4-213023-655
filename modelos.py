# -*- coding: utf-8 -*-
# Archivo: modelos.py
# Contiene la clase abstracta EntidadBase y la clase Cliente.

import re  # Herramienta de Python para revisar si un texto tiene cierto formato (la usamos con el correo)
from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas

from excepciones import (CalculoError, ClienteInvalidoError, ReservaError,
                         ServicioInvalidoError, ServicioNoDisponibleError)  # Trae nuestros errores propios
from registro import log  # Trae el registro de eventos (archivo de logs)

# Clase abstracta: es un "molde" general. No se usa directamente, sirve para que otras clases hereden de ella.
class EntidadBase(ABC):
    _contador = 0  # Cuenta cuántas entidades se han creado (lo comparten todas)

    def __init__(self):  # Se ejecuta automáticamente al crear una entidad
        EntidadBase._contador += 1  # Suma 1 al contador
        self._id = EntidadBase._contador  # Guarda ese número como id único de esta entidad

    @property  # Permite leer el id como un dato normal: entidad.id
    def id(self):
        return self._id  # Devuelve el id

    @abstractmethod  # Obliga a las clases hijas a escribir este método
    def describir(self):
        """Cada entidad debe devolver una descripción en texto."""


# Cliente hereda de EntidadBase (herencia)
class Cliente(EntidadBase):
    def __init__(self, nombre, correo, telefono):  # Datos que se piden al crear un cliente
        self.nombre = nombre  # Pasa por las reglas de validación del nombre
        self.correo = correo  # Pasa por las reglas de validación del correo
        self.telefono = telefono  # Pasa por las reglas de validación del teléfono
        super().__init__()  # Llama a la clase padre para asignar el id (solo si todos los datos fueron válidos)

    @property  # Permite leer el nombre: cliente.nombre
    def nombre(self):
        return self._nombre  # Devuelve el nombre guardado

    @nombre.setter  # Se ejecuta cada vez que se asigna un nombre
    def nombre(self, valor):
        # Si no es texto o tiene menos de 3 letras, lanza el error
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        # Si algún carácter es un número, lanza el error
        if any(ch.isdigit() for ch in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self._nombre = valor.strip()  # Guarda el nombre sin espacios sobrantes

    @property  # Permite leer el correo: cliente.correo
    def correo(self):
        return self._correo  # Devuelve el correo guardado

    @correo.setter  # Se ejecuta cada vez que se asigna un correo
    def correo(self, valor):
        # Revisa que tenga la forma texto@dominio.algo
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self._correo = valor  # Guarda el correo

    @property  # Permite leer el teléfono: cliente.telefono
    def telefono(self):
        return self._telefono  # Devuelve el teléfono guardado

    @telefono.setter  # Se ejecuta cada vez que se asigna un teléfono
    def telefono(self, valor):
        # Debe ser texto, solo números y tener entre 7 y 10 dígitos
        if not isinstance(valor, str) or not valor.isdigit() or not (7 <= len(valor) <= 10):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos.")
        self._telefono = valor  # Guarda el teléfono

    def describir(self):  # Cumple lo que exige EntidadBase: devolver una descripción
        return f"Cliente #{self.id}: {self._nombre} | {self._correo} | {self._telefono}"


    # Clase abstracta Servicio: molde general para todos los servicios de la empresa.
# Hereda de EntidadBase (para tener id) y de ABC (para ser abstracta).
class Servicio(EntidadBase, ABC):
    def __init__(self, nombre, tarifa_hora, disponible=True):  # Datos que se piden al crear un servicio
        # Si el nombre no es texto o está vacío, lanza el error
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        # Si la tarifa no es un número o es menor o igual a 0, lanza el error
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número mayor que 0.")
        self._nombre = nombre.strip()  # Guarda el nombre sin espacios sobrantes
        self._tarifa_hora = tarifa_hora  # Guarda el precio por hora
        self._disponible = disponible  # Guarda si el servicio está disponible (True) o no (False)
        super().__init__()  # Llama a la clase padre para asignar el id

    @property  # Permite leer el nombre: servicio.nombre
    def nombre(self):
        return self._nombre  # Devuelve el nombre guardado

    @property  # Permite leer la disponibilidad: servicio.disponible
    def disponible(self):
        return self._disponible  # Devuelve True o False

    @disponible.setter  # Se ejecuta cada vez que se cambia la disponibilidad
    def disponible(self, valor):
        # Solo se aceptan True o False
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self._disponible = valor  # Guarda el nuevo valor

    @abstractmethod  # Obliga a cada servicio a escribir su propia validación
    def validar_parametros(self, horas):
        """Revisa que las horas sean válidas para ese servicio."""

    @abstractmethod  # Obliga a cada servicio a escribir su propio cálculo
    def _costo_base(self, horas):
        """Calcula el costo sin impuestos ni descuentos."""

    # Método sobrecargado: se puede llamar de tres formas gracias a los valores por defecto.
    #   calcular_costo(horas)  |  calcular_costo(horas, impuesto)  |  calcular_costo(horas, impuesto, descuento)
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self.validar_parametros(horas)  # Primero revisa que las horas sean válidas
        # El impuesto y el descuento deben estar entre 0 y 1 (0 % a 100 %)
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
            raise CalculoError("Impuesto y descuento deben estar entre 0 y 1.")
        # Aplica el descuento y luego suma el impuesto al costo base
        total = self._costo_base(horas) * (1 - descuento) * (1 + impuesto)
        # Un costo negativo no tiene sentido
        if total < 0:
            raise CalculoError("El cálculo produjo un costo negativo.")
        return round(total, 2)  # Devuelve el total con 2 decimales

    @staticmethod  # Función de apoyo que no necesita datos del objeto
    def _validar_horas(horas, minimo, maximo):
        # Debe ser un número (y no un True/False)
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise ServicioInvalidoError("Las horas deben ser un número.")
        # Debe estar dentro del rango permitido
        if not (minimo <= horas <= maximo):
            raise ServicioInvalidoError(f"Las horas deben estar entre {minimo} y {maximo}.")


# ReservaSala hereda de Servicio (herencia) y escribe su propia versión de cada método (polimorfismo)
class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad):  # Además de lo general, pide la capacidad
        # La capacidad debe ser un número entero mayor que 0
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser un entero mayor que 0.")
        self._capacidad = capacidad  # Guarda la capacidad de la sala
        super().__init__(nombre, tarifa_hora)  # Llama al constructor de Servicio

    def validar_parametros(self, horas):  # Una sala se reserva entre 1 y 8 horas
        self._validar_horas(horas, 1, 8)

    def _costo_base(self, horas):  # Costo de la sala: tarifa por horas
        return self._tarifa_hora * horas

    def describir(self):  # Descripción propia de la sala
        return f"Sala '{self._nombre}' | capacidad {self._capacidad} | ${self._tarifa_hora}/h"


# AlquilerEquipo también hereda de Servicio, con reglas distintas
class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_hora, deposito):  # Además de lo general, pide un depósito
        # El depósito no puede ser negativo
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError("El depósito no puede ser negativo.")
        self._deposito = deposito  # Guarda el depósito
        super().__init__(nombre, tarifa_hora)  # Llama al constructor de Servicio

    def validar_parametros(self, horas):  # Un equipo se alquila entre 1 y 72 horas
        self._validar_horas(horas, 1, 72)

    def _costo_base(self, horas):  # Costo del equipo: tarifa por horas más el depósito
        return self._tarifa_hora * horas + self._deposito

    def describir(self):  # Descripción propia del equipo
        return f"Equipo '{self._nombre}' | ${self._tarifa_hora}/h + depósito ${self._deposito}"


# AsesoriaEspecializada es el tercer servicio, con su propio cálculo
class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):  # Pide especialidad y nivel
        # El nivel solo puede ser junior o senior
        if nivel not in ("junior", "senior"):
            raise ServicioInvalidoError("El nivel debe ser 'junior' o 'senior'.")
        self._especialidad = especialidad  # Guarda el tema de la asesoría
        self._nivel = nivel  # Guarda el nivel del asesor
        super().__init__(nombre, tarifa_hora)  # Llama al constructor de Servicio

    def validar_parametros(self, horas):  # Una asesoría dura entre 1 y 6 horas
        self._validar_horas(horas, 1, 6)

    def _costo_base(self, horas):  # Si el asesor es senior, cobra 20 % más
        recargo = 1.2 if self._nivel == "senior" else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self):  # Descripción propia de la asesoría
        return f"Asesoría '{self._nombre}' ({self._especialidad}, {self._nivel}) | ${self._tarifa_hora}/h"


# Reserva junta un cliente, un servicio y una duración, y controla su estado
class Reserva(EntidadBase):
    PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"  # Los tres estados posibles

    def __init__(self, cliente, servicio, horas):  # Datos que se piden al crear una reserva
        # Debe haber un cliente válido
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva necesita un cliente válido.")
        # Debe haber un servicio válido
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva necesita un servicio válido.")
        # El servicio debe estar disponible
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        try:  # Intenta validar las horas
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as error:  # Si fallan, atrapa ese error
            # "from error" encadena las excepciones: conserva la causa original
            raise ReservaError("Duración de la reserva inválida.") from error
        self._cliente = cliente  # Guarda el cliente
        self._servicio = servicio  # Guarda el servicio
        self._horas = horas  # Guarda la duración
        self._estado = Reserva.PENDIENTE  # Toda reserva nueva empieza pendiente
        super().__init__()  # Llama a la clase padre para asignar el id

    @property  # Permite leer el estado: reserva.estado
    def estado(self):
        return self._estado  # Devuelve el estado actual

    def confirmar(self):  # Pasa la reserva de pendiente a confirmada
        if self._estado != Reserva.PENDIENTE:  # Solo se confirma si estaba pendiente
            raise ReservaError(f"No se puede confirmar una reserva en estado {self._estado}.")
        self._estado = Reserva.CONFIRMADA  # Cambia el estado
        log.info("Reserva #%s confirmada.", self.id)  # Lo anota en el archivo de logs

    def cancelar(self):  # Cancela la reserva
        if self._estado == Reserva.CANCELADA:  # No se puede cancelar dos veces
            raise ReservaError("La reserva ya estaba cancelada.")
        self._estado = Reserva.CANCELADA  # Cambia el estado
        log.info("Reserva #%s cancelada.", self.id)  # Lo anota en el archivo de logs

    def procesar(self, impuesto=0.0, descuento=0.0):  # Calcula el costo final de la reserva
        try:  # Intenta hacer el proceso
            if self._estado != Reserva.CONFIRMADA:  # Solo se procesan reservas confirmadas
                raise ReservaError("Solo se procesan reservas confirmadas.")
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)  # Calcula el costo
        except (CalculoError, ServicioInvalidoError) as error:  # Si el cálculo falla, atrapa el error
            raise ReservaError("No fue posible calcular el costo.") from error  # Lo convierte y encadena
        else:  # Se ejecuta solo si NO hubo errores
            log.info("Reserva #%s procesada. Costo: %s", self.id, costo)  # Anota el éxito
            return costo  # Devuelve el costo final
        finally:  # Se ejecuta siempre, haya error o no
            log.info("Fin del procesamiento de la reserva #%s.", self.id)  # Anota que terminó

    def describir(self):  # Descripción de la reserva
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} "
                f"| {self._horas} h | {self._estado}")