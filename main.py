""" Archivo principal para ejecutar el juego 'Preguntados'.Este módulo inicializa Pygame, configura la ventana y llama a la función principal
del juego, que gestiona el bucle principal y las distintas pantallas."""

from Constantes import *
import pygame
from game_core import principal

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Preguntados")
    principal()