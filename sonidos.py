import pygame

# Inicializar el mixer de pygame para sonido
pygame.mixer.init()

# Cargar sonidos individuales
sonido_disparo = pygame.mixer.Sound("assets/sonidos/laser.wav")
sonido_colision = pygame.mixer.Sound("assets/sonidos/explosion.wav")
sonido_gameover = pygame.mixer.Sound("assets/sonidos/game_over.mp3")
sonido_inicio = pygame.mixer.Sound("assets/sonidos/tecla_inicio.mp3")
sonido_victoria = pygame.mixer.Sound("assets/sonidos/victoria.mp3")
sonido_explosion_nave = pygame.mixer.Sound ("assets/sonidos/explosion_nave.mp3")

# Música de fondo
musica_fondo = "assets/sonidos/musica_fondo.mp3"

# --- Funciones de sonido simples ---

def reproducir_sonido_disparo():
    """
    Objetivo:
        Reproducir el sonido de disparo.

    Parámetros:
        Ninguno.

    Salida:
        None: Reproduce el sonido inmediatamente.
    """
    sonido_disparo.play()

def reproducir_sonido_colision():
    """
    Objetivo:
        Reproducir el sonido de colisión o explosión.

    Parámetros:
        Ninguno.

    Salida:
        None: Reproduce el sonido inmediatamente.
    """
    sonido_colision.play()

# --- Funciones que requieren detener música de fondo ---

def reproducir_sonido_gameover():
    """
    Objetivo:
        Detener la música de fondo y reproducir el sonido de Game Over.

    Parámetros:
        Ninguno.

    Salida:
        None: Detiene la música y reproduce el sonido.
    """
    detener_musica_fondo()
    sonido_gameover.play()

def reproducir_sonido_inicio():
    """
    Objetivo:
        Detener la música de fondo y reproducir el sonido de inicio.

    Parámetros:
        Ninguno.

    Salida:
        None: Detiene la música y reproduce el sonido.
    """
    detener_musica_fondo()
    sonido_inicio.play()

def reproducir_sonido_victoria():
    """
    Objetivo:
        Detener la música de fondo y reproducir el sonido de victoria.

    Parámetros:
        Ninguno.

    Salida:
        None: Detiene la música y reproduce el sonido.
    """
    detener_musica_fondo()
    sonido_victoria.play()
    
def reproducir_sonido_explosion_nave():
    """
    Objetivo:
        Detener la música de fondo y reproducir el sonido de explosión de la nave.

    Parámetros:
        Ninguno.

    Salida:
        None: Detiene la música y reproduce el sonido.
    """
    detener_musica_fondo()
    sonido_explosion_nave.play()

# --- Música de fondo ---

def iniciar_musica_fondo():
    """
    Objetivo:
        Cargar y reproducir la música de fondo en bucle continuo con volumen moderado.

    Parámetros:
        Ninguno.

    Salida:
        None: Inicia la reproducción de la música de fondo.
    """
    pygame.mixer.music.load(musica_fondo)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def detener_musica_fondo():
    """
    Objetivo:
        Detener la música de fondo si está sonando.

    Parámetros:
        Ninguno.

    Salida:
        None: Detiene la reproducción de la música.
    """
    pygame.mixer.music.stop()


