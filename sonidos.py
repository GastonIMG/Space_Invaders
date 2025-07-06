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
    sonido_disparo.play()

def reproducir_sonido_colision():
    sonido_colision.play()

# --- Funciones que requieren detener música de fondo ---
def reproducir_sonido_gameover():
    detener_musica_fondo()
    sonido_gameover.play()

def reproducir_sonido_inicio():
    detener_musica_fondo()
    sonido_inicio.play()

def reproducir_sonido_victoria():
    detener_musica_fondo()
    sonido_victoria.play()
    
def reproducir_sonido_explosion_nave():
    detener_musica_fondo()
    sonido_explosion_nave.play()

# --- Música de fondo ---
def iniciar_musica_fondo():
    pygame.mixer.music.load(musica_fondo)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def detener_musica_fondo():
    pygame.mixer.music.stop()
