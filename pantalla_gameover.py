import pygame


def mostrar_pantalla_gameover(pantalla):
    ANCHO, ALTO = pantalla.get_size()
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)

    fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 24)
    texto_gameover = fuente.render("GAME OVER", True, BLANCO)

    pantalla.fill(NEGRO)
    pantalla.blit(texto_gameover, (ANCHO // 2 - texto_gameover.get_width() // 2, ALTO // 2 - 20))
    pygame.display.flip()
    pygame.time.delay(3000)
