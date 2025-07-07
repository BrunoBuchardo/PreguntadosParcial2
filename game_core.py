import pygame
from PIL import Image
from Constantes import *
from Funciones import *
from Menu import mostrar_menu
from Inicio_Juego import mostrar_inicio_juego
from Juego import mostrar_juego
from Game_Over import mostrar_game_over
from Rankings import mostrar_puntajes
from Configuracion import mostrar_configuracion
from Opciones_de_Juego import mostrar_opciones_de_juego
from Fin_Juego import mostrar_fin_juego

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración básica de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Preguntados")

# Icono y fuentes
icono = pygame.image.load("Imagenes/icono.png")
pygame.display.set_icon(icono)
fuente = pygame.font.SysFont("Monserrat", 24)
fuente_game_over = pygame.font.SysFont("Monserrat", 36)
reloj = pygame.time.Clock()

def cargar_recursos():
    """
    Carga los recursos multimedia del juego: sonidos, imágenes, GIFs.

    Retorna:
        dict: Un diccionario con todos los recursos cargados.
    """
    recursos = {}
    # Sonidos
    try:
        recursos["musica_principal"] = pygame.mixer.Sound("Sonidos/musica_principal.wav")
        recursos["musica_principal"].set_volume(VOLUMEN_INICIAL)
        recursos["musica_preguntas"] = pygame.mixer.Sound("Sonidos/musica_preguntas.wav")
        recursos["musica_preguntas"].set_volume(VOLUMEN_INICIAL)
        recursos["incorrecto"] = pygame.mixer.Sound("Sonidos/incorrecto.wav")
        recursos["correcto"] = pygame.mixer.Sound("Sonidos/correcto.wav")
        recursos["game_over"] = pygame.mixer.Sound("Sonidos/game_over.wav")
        recursos["uno_dos_tres"] = pygame.mixer.Sound("Sonidos/uno_dos_tres.wav")
    except FileNotFoundError:
        # Si falla la carga, asigna None a cada sonido
        for key in ["musica_principal", "musica_preguntas", "incorrecto", "correcto", "game_over", "uno_dos_tres"]:
            recursos[key] = None

    # Fondo animado
    try:
        gif = Image.open("Imagenes/fondopreguntados.png")
        frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            img = gif.copy().convert("RGBA").resize((ANCHO, ALTO))
            frames.append(pygame.image.fromstring(img.tobytes(), img.size, img.mode))
        recursos.update({
            "gif_frame_count": gif.n_frames,
            "gif_frame_delay": gif.info.get('duration', 100),
            "gif_frames": frames,
        })
    except Exception:
        # En caso de error, fondo blanco
        s = pygame.Surface((ANCHO, ALTO)).convert_alpha()
        s.fill(BLANCO)
        recursos.update({"gif_frame_count": 1, "gif_frame_delay": 100, "gif_frames": [s]})

    # Animación de Toasty
    try:
        tg = Image.open("Imagenes/preguntados_senalando.gif")
        toasty = []
        for frame in range(tg.n_frames):
            tg.seek(frame)
            img = tg.copy().convert("RGBA").resize((100, 100))
            toasty.append(pygame.image.fromstring(img.tobytes(), img.size, img.mode))
        recursos.update({
            "toasty_frame_count": tg.n_frames,
            "toasty_frame_delay": tg.info.get('duration', 50),
            "toasty_frames": toasty,
        })
    except Exception:
        # Si falla, superficie blanca de 100x100
        s2 = pygame.Surface((100, 100)).convert_alpha()
        s2.fill(BLANCO)
        recursos.update({"toasty_frame_count": 1, "toasty_frame_delay": 50, "toasty_frames": [s2]})

    # Fondo estático de juego
    try:
        recursos["juego_background"] = pygame.transform.scale(
            pygame.image.load("Imagenes/preguntados_3.png"), (ANCHO, ALTO)
        )
    except FileNotFoundError:
        sf = pygame.Surface((ANCHO, ALTO)).convert_alpha()
        sf.fill(BLANCO)
        recursos["juego_background"] = sf

    return recursos

def principal():
    """
    Bucle principal del juego.  
    Controla el estado del juego y delega en las pantallas correspondientes:
    menú, juego, rankings, configuración, etc.

    Además:
    - Carga recursos.
    - Controla las animaciones (GIF y Toasty).
    - Gestiona música y efectos sonoros.
    """
    # Inicializa datos del estado del juego
    datos_juego = {
        "ejecutando": True,
        "estado": MENU,
        "puntaje": PUNTAJE_INICIAL,
        "vidas": DIFICULTADES["MEDIO"]["vidas"],
        "correctas_seguidas": CORRECTAS_SEGUIDAS_INICIAL,
        "pregunta_actual": None,
        "opciones": [],
        "respuesta_correcta": "",
        "bomba_usada": False,
        "x2_usado": X2_USADO_INICIAL,
        "doble_chance_usado": DOBLE_CHANCE_USADO_INICIAL,
        "doble_chance_activo": False,
        "opciones_restantes": [],
        "pasar_usado": PASAR_USADO_INICIAL,
        "nombre_jugador": "",
        "entrada_nombre": "",
        "juego_terminado_por_preguntas": False,
        "mensaje_comodin": "",
        "mensaje_comodin_tiempo": 0,
        "tiempo_inicio": 0,
        "dificultad_seleccionada": "MEDIO",
        "cuenta_regresiva": 3,
        "cuenta_regresiva_tiempo": 0,
        "gif_frame_index": 0,
        "gif_last_update": 0,
        "toasty_active": False,
        "toasty_type": None,
        "toasty_x": -100,
        "toasty_direction": "ida",
        "toasty_frame_index": 0,
        "toasty_last_update": 0,
        "ultimo_click_tiempo": 0,
        "musica_sonando": True,
        "volumen_musica": VOLUMEN_INICIAL,
        "musica_actual": None,
        "preguntas": cargar_preguntas(),
    }
    # Carga los recursos multimedia
    datos_juego.update(cargar_recursos())
    datos_juego["musica_actual"] = datos_juego["musica_principal"]
    if datos_juego["musica_actual"]:
        datos_juego["musica_actual"].play(-1)

    # Asociación de estados con sus respectivas funciones
    estado_funciones = {
        MENU: mostrar_menu,
        INICIO_JUEGO: mostrar_inicio_juego,
        JUEGO: mostrar_juego,
        GAME_OVER: mostrar_game_over,
        RANKINGS: mostrar_puntajes,
        CONFIGURACION: mostrar_configuracion,
        OPCIONES_DE_JUEGO: mostrar_opciones_de_juego,
        FIN_JUEGO: mostrar_fin_juego
    }
    # Bucle principal
    while datos_juego["ejecutando"]:
        now = pygame.time.get_ticks()

        # Actualiza el frame del GIF de fondo
        if datos_juego["estado"] not in [JUEGO, GAME_OVER] and now - datos_juego["gif_last_update"] > datos_juego["gif_frame_delay"]:
            datos_juego["gif_frame_index"] = (datos_juego["gif_frame_index"] + 1) % datos_juego["gif_frame_count"]
            datos_juego["gif_last_update"] = now

        # Animación Toasty
        if datos_juego["toasty_active"]:
            toasty_rect = pygame.Rect(datos_juego["toasty_x"], ALTO//2, 100, 100)
            opciones_rect = pygame.Rect(200, 150, 400, 180)
            if datos_juego["toasty_direction"] == "ida":
                datos_juego["toasty_x"] += (ANCHO + 200) / (2.0 * FPS)  # ida ~2s
                if toasty_rect.colliderect(opciones_rect):
                    datos_juego["toasty_direction"] = "vuelta"
            else:
                datos_juego["toasty_x"] -= (ANCHO + 200) / (2.5 * FPS)  # vuelta ~2.5s
            if now - datos_juego["toasty_last_update"] > datos_juego["toasty_frame_delay"]:
                datos_juego["toasty_frame_index"] = (datos_juego["toasty_frame_index"] + 1) % datos_juego["toasty_frame_count"]
                datos_juego["toasty_last_update"] = now
            # Finaliza la animación si ya pasó suficiente tiempo o llegó al final
            if datos_juego["toasty_direction"] == "vuelta" and datos_juego["toasty_x"] <= -100 or now - datos_juego["toasty_start_time"] > 4500:
                datos_juego["toasty_active"] = False
                datos_juego["toasty_x"] = -100
                datos_juego["toasty_direction"] = "ida"
                datos_juego["toasty_frame_index"] = 0

        # Limpia mensaje de comodín después de 2 segundos
        if datos_juego["mensaje_comodin"] and now - datos_juego["mensaje_comodin_tiempo"] > 2000:
            datos_juego["mensaje_comodin"] = ""

        # Eventos
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                datos_juego["ejecutando"] = False

        # Ejecuta la función correspondiente al estado actual
        estado_anterior = datos_juego["estado"]
        datos_juego["estado"] = estado_funciones[datos_juego["estado"]](
            pantalla, eventos, datos_juego, fuente, fuente_game_over
        )

        # Cambios de estado: música y sonidos
        if datos_juego["estado"] != estado_anterior:
            if datos_juego["estado"] == JUEGO and datos_juego["musica_preguntas"] and datos_juego["musica_sonando"]:
                if datos_juego["musica_actual"] != datos_juego["musica_preguntas"] or not pygame.mixer.get_busy():
                    if datos_juego["musica_actual"]:
                        datos_juego["musica_actual"].stop()
                    datos_juego["musica_actual"] = datos_juego["musica_preguntas"]
                    datos_juego["musica_actual"].set_volume(datos_juego["volumen_musica"])
                    datos_juego["musica_actual"].play(-1)
            elif datos_juego["estado"] == GAME_OVER and datos_juego["game_over"]:
                pygame.mixer.stop()
                datos_juego["game_over"].play()
            elif datos_juego["estado"] == INICIO_JUEGO and datos_juego["uno_dos_tres"]:
                pygame.mixer.stop()
                datos_juego["uno_dos_tres"].play()
                datos_juego["cuenta_regresiva"] = 3
                datos_juego["cuenta_regresiva_tiempo"] = now
            elif datos_juego["musica_principal"] and datos_juego["musica_sonando"]:
                if datos_juego["musica_actual"] != datos_juego["musica_principal"] or not pygame.mixer.get_busy():
                    if datos_juego["musica_actual"]:
                        datos_juego["musica_actual"].stop()
                    datos_juego["musica_actual"] = datos_juego["musica_principal"]
                    datos_juego["musica_actual"].set_volume(datos_juego["volumen_musica"])
                    datos_juego["musica_actual"].play(-1)

        # Dibuja Toasty si está activo
        if datos_juego["toasty_active"]:
            pantalla.blit(
                datos_juego["toasty_frames"][datos_juego["toasty_frame_index"]],
                (datos_juego["toasty_x"], ALTO//2)
            )

        pygame.display.flip()
        reloj.tick(FPS)

    # Finaliza Pygame al salir
    pygame.quit()
