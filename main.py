import pygame
import sys
import random
import importlib
import os

from pantalla_inicio import pantalla_inicio
from pantalla_gameover import mostrar_pantalla_gameover
from pantalla_highscore import mostrar_pantalla_highscore
from sonidos import (
    reproducir_sonido_disparo,
    reproducir_sonido_colision,
    reproducir_sonido_gameover,
    reproducir_sonido_inicio,
    reproducir_sonido_victoria,
    iniciar_musica_fondo,
    detener_musica_fondo,
    reproducir_sonido_explosion_nave
)
from nave import crear_nave, mover_nave, dibujar_nave
from enemigos import crear_enemigo, actualizar_enemigo, dibujar_enemigo, disparo_enemigo
from puntaje import cargar_highscore, guardar_highscore

# Inicialización de Pygame y configuración del juego
pygame.init()
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader 🚀")
fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 20)

# Colores usados
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Carga de imágenes
def cargar_imagenes_aliens():
    """
    Objetivo:
        Cargar y escalar las imágenes de los aliens desde la carpeta de assets,
        organizándolas en un diccionario por tipo y frames de animación.

    Parámetros:
        Ninguno.

    Salida:
        dict: Diccionario donde la clave es el número del alien (int) y el valor es una lista de
              pygame.Surface con los frames de animación para ese alien.
    """
    imagenes = {}
    for i in range(1, 5):
        frames = []
        for j in range(1, 4):
            path = f"assets/aliens/alien_{i}" + (f"_frame_{j}.png" if j > 1 else ".png")
            if os.path.exists(path):
                imagen = pygame.image.load(path).convert_alpha()
                imagen = pygame.transform.scale(imagen, (40, 40))
                frames.append(imagen)
        if frames:
            imagenes[i] = frames
    return imagenes

imagenes_aliens = cargar_imagenes_aliens()
explosion_enemigo_img = pygame.transform.scale(pygame.image.load("assets/explosion_enemigos.png").convert_alpha(), (60, 60))
explosion_nave_img = pygame.transform.scale(pygame.image.load("assets/explosion_nave.png").convert_alpha(), (60, 60))

# Muestra el texto de nivel
def mostrar_texto_nivel(nivel):
    """
    Objetivo:
        Mostrar en pantalla el texto del nivel actual durante 2 segundos, centrado.

    Parámetros:
        nivel (int): Número del nivel a mostrar.

    Salida:
        None: Muestra el texto en pantalla y pausa la ejecución temporalmente.
    """
    texto = fuente.render(f"Nivel {nivel}", True, BLANCO)
    pantalla.fill(NEGRO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

# Bucle principal
def main():
    """
    Objetivo:
        Ejecutar el bucle principal del juego Space Invader, controlando el flujo de niveles,
        la interacción del jugador, la lógica de enemigos, disparos, colisiones, puntaje y sonidos.

    Parámetros:
        Ninguno.

    Salida:
        None: Ejecuta el juego hasta que el jugador cierre la ventana o termine los niveles.
    """
    reloj = pygame.time.Clock()
    MAX_NIVELES = 5
    jugando = True

    while jugando:
        iniciar_musica_fondo()
        pantalla_inicio(pantalla)
        detener_musica_fondo()

        nivel_actual = 1
        puntuacion = 0

        try:
            highscore = cargar_highscore()
        except:
            guardar_highscore(0)
            highscore = 0

        while nivel_actual <= MAX_NIVELES and jugando:
            # Carga dinámica del módulo por niveles
            try:
                nivel_modulo = importlib.import_module(f"niveles.nivel_{nivel_actual}")
                cargar_nivel = getattr(nivel_modulo, f"cargar_nivel{nivel_actual}")
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error cargando nivel {nivel_actual}: {e}")
                break

            enemigos_config, velocidad_disparo, musica_nivel = cargar_nivel(ANCHO, ALTO, fuente, imagenes_aliens)

            pygame.mixer.music.load(musica_nivel)
            pygame.mixer.music.play(-1)
            mostrar_texto_nivel(nivel_actual)

            nave = crear_nave(ANCHO // 2, ALTO - 40)
            grupo_enemigos = enemigos_config
            disparos = []
            disparos_enemigos = []
            explosiones = []

            nivel_en_curso = True
            while nivel_en_curso:
                reloj.tick(60)

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        nivel_en_curso = False
                        jugando = False
                    elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        disparo = pygame.Rect(nave["rect"].centerx - 2, nave["rect"].top, 5, 15)
                        disparos.append(disparo)
                        reproducir_sonido_disparo()

                teclas = pygame.key.get_pressed()
                mover_nave(nave, teclas, ANCHO)

                # Disparos del jugador
                for d in disparos:
                    d.y -= velocidad_disparo
                disparos = [d for d in disparos if d.y > 0]


                # Disparos del enemigo
                for de in disparos_enemigos:
                    de.y += 5
                disparos_enemigos = list(filter(lambda d: d.y < ALTO, disparos_enemigos))

                # Los enemigos disparan aleatoriamente
                if random.randint(0, 100) < 2 and grupo_enemigos:
                    grupo_enemigos.sort(key=lambda e: e["rect"].x)
                    atacante = random.choice(grupo_enemigos)
                    disparos_enemigos.append(disparo_enemigo(atacante))

                # Colisiones: disparos jugador a enemigos
                for d in disparos[:]:
                    for e in grupo_enemigos[:]:
                        if e["rect"].colliderect(d):
                            reproducir_sonido_colision()
                            disparos.remove(d)
                            grupo_enemigos.remove(e)
                            explosiones.append((explosion_enemigo_img, e["rect"].center, 15))
                            puntuacion += 10
                            break

                # Colisiones: disparos enemigos a jugador
                for d in disparos_enemigos[:]:
                    if nave["rect"].colliderect(d):
                        reproducir_sonido_explosion_nave()
                        explosiones.append((explosion_nave_img, nave["rect"].center, 30))
                        mostrar_animacion_y_gameover(grupo_enemigos, disparos, disparos_enemigos, explosiones)
                        reproducir_sonido_gameover()
                        detener_musica_fondo()
                        mostrar_pantalla_gameover(pantalla)

                        if puntuacion > highscore:
                            guardar_highscore(puntuacion)
                            highscore = puntuacion

                        mostrar_pantalla_highscore(pantalla, puntuacion, highscore)
                        nivel_en_curso = False
                        break

                # Movimiento de los enemigos
                for e in grupo_enemigos:
                    actualizar_enemigo(e)

                # Render
                pantalla.fill(NEGRO)
                dibujar_nave(pantalla, nave)
                for e in grupo_enemigos:
                    dibujar_enemigo(pantalla, e)
                for d in disparos:
                    pygame.draw.rect(pantalla, BLANCO, d)
                for d in disparos_enemigos:
                    pygame.draw.rect(pantalla, (255, 0, 0), d)

                # Explosiones animadas
                for exp in explosiones[:]:
                    img, centro, t = exp
                    pantalla.blit(img, img.get_rect(center=centro))
                    t -= 1
                    if t <= 0:
                        explosiones.remove(exp)
                    else:
                        idx = explosiones.index(exp)
                        explosiones[idx] = (img, centro, t)

                # Puntaje
                texto_puntaje = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
                pantalla.blit(texto_puntaje, (10, 10))

                pygame.display.flip()

                if not grupo_enemigos:
                    reproducir_sonido_victoria()
                    detener_musica_fondo()
                    texto = fuente.render("¡Nivel Completado!", True, BLANCO)
                    pantalla.fill(NEGRO)
                    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    nivel_en_curso = False
                    nivel_actual += 1

    pygame.quit()
    sys.exit()

# Muestra la animación de explosión final antes de game over
def mostrar_animacion_y_gameover(enemigos, disparos, disparos_enemigos, explosiones):
    """
    Objetivo:
        Mostrar en pantalla la animación de explosiones y elementos activos antes de la pantalla de Game Over.

    Parámetros:
        enemigos (list): Lista de enemigos activos en pantalla.
        disparos (list): Lista de disparos activos del jugador.
        disparos_enemigos (list): Lista de disparos activos de los enemigos.
        explosiones (list): Lista de tuplas con imágenes y posiciones para animar explosiones.

    Salida:
        None: Dibuja la animación en pantalla y detiene la ejecución momentáneamente.
    """
    pantalla.fill(NEGRO)
    for enemigo in enemigos:
        dibujar_enemigo(pantalla, enemigo)
    for d in disparos:
        pygame.draw.rect(pantalla, BLANCO, d)
    for d in disparos_enemigos:
        pygame.draw.rect(pantalla, (255, 0, 0), d)
    for img, centro, _ in explosiones:
        pantalla.blit(img, img.get_rect(center=centro))
    pygame.display.flip()
    pygame.time.delay(1000)

if __name__ == "__main__":
    main()


