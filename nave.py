import pygame

def crear_nave(x, y):
    """
    Objetivo:
        Crear un diccionario que representa a la nave del jugador, con imagen escalada y posición inicial.

    Parámetros:
        x (int): Posición horizontal del centro de la nave.
        y (int): Posición vertical del centro de la nave.

    Salida:
        dict: Diccionario que contiene la imagen escalada de la nave, su rectángulo de posición y la velocidad de movimiento.
    """
    imagen_original = pygame.image.load("assets/nave.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_original, (80, 60))  # Tamaño ajustado
    rect = imagen_escalada.get_rect(center=(x, y))
    return {
        "imagen": imagen_escalada,
        "rect": rect,
        "velocidad": 5
    }

def mover_nave(nave, teclas, ancho_pantalla):
    """
    Objetivo:
        Mover la nave hacia la izquierda o derecha dentro de los límites de la pantalla, según las teclas presionadas.

    Parámetros:
        nave (dict): Diccionario con la información de la nave, incluyendo su rectángulo y velocidad.
        teclas (list[bool]): Lista de teclas presionadas (usualmente obtenida con pygame.key.get_pressed()).
        ancho_pantalla (int): Ancho de la pantalla del juego para limitar el movimiento.

    Salida:
        None: La función modifica la posición de la nave directamente.
    """
    if teclas[pygame.K_LEFT] and nave["rect"].left > 0:
        nave["rect"].x -= nave["velocidad"]
    if teclas[pygame.K_RIGHT] and nave["rect"].right < ancho_pantalla:
        nave["rect"].x += nave["velocidad"]

def dibujar_nave(pantalla, nave):
    """
    Objetivo:
        Dibujar la nave del jugador en la superficie del juego.

    Parámetros:
        pantalla (pygame.Surface): Superficie donde se va a dibujar la nave.
        nave (dict): Diccionario que contiene la imagen y el rectángulo de la nave.

    Salida:
        None: Dibuja directamente sobre la superficie de la pantalla.
    """
    pantalla.blit(nave["imagen"], nave["rect"])

