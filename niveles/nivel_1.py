import random
import pygame
from enemigos import actualizar_enemigo, dibujar_enemigo, disparo_enemigo

def crear_enemigo (x, y, imagenes, pantalla_ancho):
    enemigo = {
        "rect": pygame.Rect(x, y, imagenes[0].get_width(), imagenes[0].get_height()),
        "imagenes": imagenes,
        "index_imagen": 0,
        "velocidad_x": 5,
        "velocidad_y": 10,
        "pantalla_ancho": pantalla_ancho,
        "contador_animacion": 0,
        "frecuencia_animacion": 10,
    }
    return enemigo


def cargar_nivel1(ANCHO, ALTO, fuente, imagenes_aliens):
    lista_enemigos = []
    for fila in range(4):
        for columna in range(6):
            x = 100 + columna * 100
            y = 50 + fila * 70

            tipo_alien = random.choice([1, 2, 3, 4])  # Elegir tipo alien válido
            imagenes_para_enemigo = imagenes_aliens[tipo_alien]  # Obtener sus imágenes

            enemigo = crear_enemigo(x, y, imagenes_para_enemigo, ANCHO)
            lista_enemigos.append(enemigo)

    velocidad_disparo = 15
    musica_nivel = "assets/sonidos/nivel_1.mp3"

    return lista_enemigos, velocidad_disparo, musica_nivel

