import pygame

def mostrar_pantalla_gameover(pantalla):
    """
    Objetivo:
        Mostrar una pantalla de "Game Over" centrada en negro con texto blanco durante 3 segundos.

    Parámetros:
        pantalla (pygame.Surface): Superficie donde se mostrará el mensaje de Game Over.

    Salida:
        None: La función actualiza la pantalla y detiene la ejecución temporalmente.
    """
    ANCHO, ALTO = pantalla.get_size()
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)

    fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 24)
    texto_gameover = fuente.render("GAME OVER", True, BLANCO)

    pantalla.fill(NEGRO)
    pantalla.blit(texto_gameover, (ANCHO // 2 - texto_gameover.get_width() // 2, ALTO // 2 - 20))
    pygame.display.flip()
    pygame.time.delay(3000)

