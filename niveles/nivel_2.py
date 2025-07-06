import random
import pygame
from enemigos import actualizar_enemigo, dibujar_enemigo, disparo_enemigo


def crear_enemigo(x, y, imagenes, pantalla_ancho):
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

def cargar_nivel2(ANCHO, ALTO, fuente, imagenes_aliens):
    lista_enemigos = []
    for fila in range(5):
        for columna in range(7):
            x = 70 + columna * 90
            y = 40 + fila * 65
            
            tipo_alien = random.choice([1, 2, 3, 4])
            imagenes_para_enemigo = imagenes_aliens[tipo_alien]

            enemigo = crear_enemigo(x, y, imagenes_para_enemigo, ANCHO)
            lista_enemigos.append(enemigo)

    velocidad_disparo = 25
    musica_nivel = "assets/sonidos/nivel_2.mp3"

    return lista_enemigos, velocidad_disparo, musica_nivel

