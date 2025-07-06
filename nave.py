import pygame

def crear_nave(x, y):
    imagen_original = pygame.image.load("assets/nave.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_original, (80, 60))  # Tamaño ajustado
    rect = imagen_escalada.get_rect(center=(x, y))
    return {
        "imagen": imagen_escalada,
        "rect": rect,
        "velocidad": 5
    }

def mover_nave(nave, teclas, ancho_pantalla):
    if teclas[pygame.K_LEFT] and nave["rect"].left > 0:
        nave["rect"].x -= nave["velocidad"]
    if teclas[pygame.K_RIGHT] and nave["rect"].right < ancho_pantalla:
        nave["rect"].x += nave["velocidad"]

def dibujar_nave(pantalla, nave):
    pantalla.blit(nave["imagen"], nave["rect"])


