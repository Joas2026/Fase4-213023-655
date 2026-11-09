# -*- coding: utf-8 -*-
# Archivo: registro.py
# Configura el archivo de logs donde se guardan los errores y eventos del sistema.

import logging  # Módulo de Python para registrar mensajes (logs)

# Configuración general del registro de eventos
logging.basicConfig(
    filename="software_fj.log",  # Nombre del archivo donde se guardan los mensajes
    level=logging.INFO,  # Guarda mensajes desde nivel INFO hacia arriba (INFO, WARNING, ERROR)
    format="%(asctime)s | %(levelname)s | %(message)s",  # Formato: fecha y hora | nivel | mensaje
    encoding="utf-8",  # Permite guardar tildes y ñ correctamente
)

# Crea el objeto "log" que usarán los demás archivos para escribir en el registro
log = logging.getLogger("software_fj")