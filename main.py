# -*- coding: utf-8 -*-
# Archivo: main.py
# Archivo principal para ejecutar el Sistema de Gestión Software FJ

from modelos import Cliente
from registro import log

def ejecutar_sistema():
    print("=" * 60)
    print("   SISTEMA DE GESTIÓN DE CLIENTES Y RESERVAS - SOFTWARE FJ")
    print("=" * 60)
    
    try:
        log.info("Iniciando la aplicación principal desde main.py.")
        print("\n[✔] El sistema se ha inicializado correctamente.")
        print("[✔] Los módulos de modelos y excepciones cargaron sin errores.\n")
        
        # Creamos un cliente de prueba usando la clase Cliente de modelos.py
        cliente_prueba = Cliente("Pedro Gomez", "pedrogomez123@gmail.com", "3001234567")
        print(f"Cliente de prueba creado con éxito: {cliente_prueba.nombre}")
        print(f"Correo: {cliente_prueba.correo} | Teléfono: {cliente_prueba.telefono}\n")

    except Exception as e:
        log.error(f"Se produjo un error en el sistema: {e}")
        print(f"[X] Ocurrió un error: {e}")

if __name__ == "__main__":
    ejecutar_sistema()