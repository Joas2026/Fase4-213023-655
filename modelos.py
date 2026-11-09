# -*- coding: utf-8 -*-
# Archivo: modelos.py
# Contiene la clase abstracta EntidadBase y la clase Cliente.

import re  # Herramienta de Python para revisar si un texto tiene cierto formato (la usamos con el correo)
from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas

from excepciones import ClienteInvalidoError  # Trae nuestro error propio desde excepciones.py


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