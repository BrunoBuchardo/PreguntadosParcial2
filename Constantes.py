"""Este módulo define las constantes globales utilizadas en el juego, incluyendo colores, dimensiones de la pantalla,
estados del juego, configuraciones iniciales y parámetros de las dificultades. Estas constantes son utilizadas
por otros módulos para mantener consistencia en la configuración del juego."""
#COLORES
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 240, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

#DIMENSIONES
ANCHO = 800
ALTO = 700

#ESTADOS 
MENU = "menu"
JUEGO = "juego"
GAME_OVER = "game_over"
RANKINGS = "rankings"
CONFIGURACION = "configuracion"
FIN_JUEGO = "fin_juego"
OPCIONES_DE_JUEGO = "opciones_de_juego"
INICIO_JUEGO = "inicio_juego"

#CONFIGURACIONES
PUNTAJE_INICIAL = 0
VIDAS_INICIALES = 3
CORRECTAS_SEGUIDAS_INICIAL = 0
VOLUMEN_INICIAL = 0.5
LIMITE_NOMBRE = 20
X2_USADO_INICIAL = False
DOBLE_CHANCE_USADO_INICIAL = False
PASAR_USADO_INICIAL = False
FPS = 30

#DIFICULTADES
DIFICULTADES = {
    "FACIL": {"puntos_aciertos": 15, "puntos_errores": -3, "vidas": 5, "tiempo_pregunta": 45},
    "MEDIO": {"puntos_aciertos": 10, "puntos_errores": -5, "vidas": 3, "tiempo_pregunta": 30},
    "DIFICIL": {"puntos_aciertos": 20, "puntos_errores": -10, "vidas": 2, "tiempo_pregunta": 20}
}