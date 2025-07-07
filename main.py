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
    reproducir_sonido_victoria,
    iniciar_musica_fondo,
    detener_musica_fondo,
    reproducir_sonido_explosion_nave
)
from nave import crear_nave, mover_nave, dibujar_nave
from enemigos import actualizar_enemigo, dibujar_enemigo, disparo_enemigo
from puntaje import cargar_highscores, guardar_highscores, actualizar_highscores

# Inicialización de Pygame y configuración general
pygame.init()
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader 🚀")
fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 20)

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Carga de las imágenes
def cargar_imagenes_aliens():
    """
    Objetivo:
        Cargar y escalar las imágenes de los aliens desde la carpeta de assets,
        organizándolas en un diccionario por tipo y frames de animación.

    Parámetros:
        Ninguno.

    Salida:
        dict: Diccionario donde la clave es el número del alien y el valor es una lista de imágenes.
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


def mostrar_texto_nivel(nivel):
    """
    Objetivo:
        Mostrar en pantalla el número del nivel actual durante 2 segundos.

    Parámetros:
        nivel (int): Número del nivel a mostrar.

    Salida:
        None.
    """
    texto = fuente.render(f"Nivel {nivel}", True, BLANCO)
    pantalla.fill(NEGRO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


def mostrar_animacion_y_gameover(enemigos, disparos, disparos_enemigos, explosiones):
    """
    Objetivo:
        Mostrar en pantalla la animación de explosiones y elementos activos antes de la pantalla de Game Over.

    Parámetros:
        enemigos (lista): Lista de enemigos activos.
        disparos (lista): Lista de disparos del jugador.
        disparos_enemigos (lista): Lista de disparos enemigos.
        explosiones (lista): Lista de animaciones de explosión.

    Salida:
        None.
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


def jugar_nivel(nivel_actual, highscore, puntuacion):
    """
    Objetivo:
        Ejecutar un único nivel del juego.

    Parámetros:
        nivel_actual (int): Número del nivel actual.
        highscore (int): Mayor puntaje registrado.
        puntuacion (int): Puntaje actual del jugador.

    Salida:
        tupla: (nivel_superado (bool), nueva_puntuacion (int), seguir_jugando (bool))
    """
    reloj = pygame.time.Clock()

    # Carga el módulo del nivel actual
    try:
        nivel_modulo = importlib.import_module(f"niveles.nivel_{nivel_actual}")
        cargar_nivel = getattr(nivel_modulo, f"cargar_nivel{nivel_actual}")
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error cargando nivel {nivel_actual}: {e}")
        return False, puntuacion, True

    enemigos_config, velocidad_disparo, musica_nivel = cargar_nivel(ANCHO, ALTO, fuente, imagenes_aliens)

    pygame.mixer.music.load(musica_nivel)
    pygame.mixer.music.play(-1)
    mostrar_texto_nivel(nivel_actual)

    nave = crear_nave(ANCHO // 2, ALTO - 40)
    grupo_enemigos = enemigos_config
    disparos = []
    disparos_enemigos = []
    explosiones = []

    while True:
        reloj.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False, puntuacion, False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                disparo = pygame.Rect(nave["rect"].centerx - 2, nave["rect"].top, 5, 15)
                disparos.append(disparo)
                reproducir_sonido_disparo()

        teclas = pygame.key.get_pressed()
        mover_nave(nave, teclas, ANCHO)

        # Movimiento de los disparos del jugador
        for d in disparos:
            d.y -= velocidad_disparo
        disparos = [d for d in disparos if d.y > 0]

        # Movimiento de los disparos del enemigo
        for de in disparos_enemigos:
            de.y += 5
        disparos_enemigos = [d for d in disparos_enemigos if d.y < ALTO]

        if grupo_enemigos:
            # 1) Ordenamos enemigos por posición X (horizontal)
            grupo_enemigos.sort(key=lambda e: e["rect"].x)

            # 2) Filtramos a los enemigos vivos de los que ya fueron eliminados 
            enemigos_vivos = list(filter(lambda e: e.get("vida", 1) > 0, grupo_enemigos))

            # Disparo enemigo aleatorio entre enemigos vivos
            if random.randint(0, 100) < 2 and enemigos_vivos:
                atacante = random.choice(enemigos_vivos)
                disparos_enemigos.append(disparo_enemigo(atacante))

        # Colisiones de disparo entre jugador-enemigo
        for d in disparos[:]:
            for e in grupo_enemigos[:]:
                if e["rect"].colliderect(d):
                    reproducir_sonido_colision()
                    disparos.remove(d)
                    grupo_enemigos.remove(e)
                    explosiones.append((explosion_enemigo_img, e["rect"].center, 15))
                    puntuacion += 10
                    break

        # Colisiones de disparo entre enemigo-jugador
        for d in disparos_enemigos[:]:
            if nave["rect"].colliderect(d):
                reproducir_sonido_explosion_nave()
                explosiones.append((explosion_nave_img, nave["rect"].center, 30))
                mostrar_animacion_y_gameover(grupo_enemigos, disparos, disparos_enemigos, explosiones)
                reproducir_sonido_gameover()
                detener_musica_fondo()
                mostrar_pantalla_gameover(pantalla)

                if puntuacion > highscore:
                    actualizar_highscores(puntuacion)
                    highscore = puntuacion

                lista_highscores = cargar_highscores()
                mostrar_pantalla_highscore(pantalla, puntuacion, lista_highscores)

                return False, puntuacion, True

        # Movimiento de los enemigos
        for e in grupo_enemigos:
            actualizar_enemigo(e)

        # Se Dibujan todos los elementos del juego en pantalla
        pantalla.fill(NEGRO)
        dibujar_nave(pantalla, nave)
        for e in grupo_enemigos:
            dibujar_enemigo(pantalla, e)
        for d in disparos:
            pygame.draw.rect(pantalla, BLANCO, d)
        for d in disparos_enemigos:
            pygame.draw.rect(pantalla, (255, 0, 0), d)

        for exp in explosiones[:]:
            img, centro, t = exp
            pantalla.blit(img, img.get_rect(center=centro))
            t -= 1
            if t <= 0:
                explosiones.remove(exp)
            else:
                idx = explosiones.index(exp)
                explosiones[idx] = (img, centro, t)

        texto_puntaje = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntaje, (10, 10))
        pygame.display.flip()

        # Si se eliminan todos los enemigos, se pasa al siguiente nivel
        if not grupo_enemigos:
            reproducir_sonido_victoria()
            detener_musica_fondo()
            texto = fuente.render("¡Nivel Completado!", True, BLANCO)
            pantalla.fill(NEGRO)
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            return True, puntuacion, True


def main():
    """
    Objetivo:
        Ejecutar el bucle principal del juego.

    Parámetros:
        Ninguno.

    Salida:
        None.
    """
    MAX_NIVELES = 5
    jugando = True

    while jugando:
        iniciar_musica_fondo()
        pantalla_inicio(pantalla)
        detener_musica_fondo()

        nivel_actual = 1
        puntuacion = 0

        try:
            highscores = cargar_highscores()
            highscore = max(highscores) if highscores else 0
        except:
            guardar_highscores([])
            highscores = []
            highscore = 0

        while nivel_actual <= MAX_NIVELES and jugando:
            nivel_superado, puntuacion, seguir_jugando = jugar_nivel(nivel_actual, highscore, puntuacion)
            if not seguir_jugando:
                jugando = False
                break
            if nivel_superado:
                nivel_actual += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()




