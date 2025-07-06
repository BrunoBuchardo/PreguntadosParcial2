"""Módulo principal para Preguntados.

Este módulo inicializa el juego, carga recursos multimedia (imágenes, sonidos, GIFs), y ejecuta el bucle
principal que delega el manejo de los estados a los módulos correspondientes (menú, juego, configuración, etc.).
"""

from Constantes import *
# main.py
"""
Módulo principal ligero que inicia el juego Preguntados.
"""
import pygame
from game_core import principal

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Preguntados")
    principal()