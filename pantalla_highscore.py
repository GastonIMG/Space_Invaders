import pygame

def mostrar_pantalla_highscore(pantalla, puntuacion, highscore):
    """
    Muestra en pantalla la puntuación actual y el highscore.
    Espera a que el jugador presione una tecla para continuar.
    """

    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)

    ancho, alto = pantalla.get_size()
    fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 25)

    pantalla.fill(NEGRO)

    texto_titulo = fuente.render("Highscore", True, BLANCO)
    texto_puntuacion = fuente.render(f"Tu Puntuación: {puntuacion}", True, BLANCO)
    texto_record = fuente.render(f"Récord: {highscore}", True, BLANCO)
    texto_instrucciones = fuente.render("Presioná cualquier tecla para salir", True, BLANCO)

    # Centramos textos en pantalla
    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, alto // 4))
    pantalla.blit(texto_puntuacion, (ancho // 2 - texto_puntuacion.get_width() // 2, alto // 4 + 60))
    pantalla.blit(texto_record, (ancho // 2 - texto_record.get_width() // 2, alto // 4 + 120))
    pantalla.blit(texto_instrucciones, (ancho // 2 - texto_instrucciones.get_width() // 2, alto // 4 + 200))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False
