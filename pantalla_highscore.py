import pygame
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

def mostrar_pantalla_highscore(pantalla, puntuacion_actual, lista_highscores):
    """
    Objetivo:
        Mostrar en pantalla la lista de los 10 mejores puntajes junto con la puntuación actual.

    Parámetros:
        pantalla (pygame.Surface): La superficie donde se dibujará.
        puntuacion_actual (int): La puntuación que acaba de obtener el jugador.
        lista_highscores (list): Lista de los 10 mejores puntajes.

    Salida:
        None: Muestra la pantalla hasta que el jugador presione una tecla.
    """
    fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 20)
    pantalla.fill(NEGRO)

    # Título
    texto_titulo = fuente.render("Highscores", True, BLANCO)
    pantalla.blit(texto_titulo, (pantalla.get_width() // 2 - texto_titulo.get_width() // 2, 50))

    # Puntaje actual
    texto_puntaje = fuente.render(f"Tu Puntaje: {puntuacion_actual}", True, BLANCO)
    pantalla.blit(texto_puntaje, (pantalla.get_width() // 2 - texto_puntaje.get_width() // 2, 100))

    # Highscores
    y = 160
    for idx, score in enumerate(lista_highscores[:10], start=1):
        texto_score = fuente.render(f"{idx}. {score}", True, BLANCO)
        pantalla.blit(texto_score, (pantalla.get_width() // 2 - texto_score.get_width() // 2, y))
        y += 30

    # Mensaje de continuar
    texto_continuar = fuente.render("Presiona una tecla para continuar", True, BLANCO)
    pantalla.blit(texto_continuar, (pantalla.get_width() // 2 - texto_continuar.get_width() // 2, y + 20))

    pygame.display.flip()

    # Espera una tecla para volver al menú principal
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False #Vuelve al menu
                else:
                    return True #Continua jugando o reinicia
                

