import pygame

def crear_enemigo(x, y, imagenes, pantalla_ancho=800):
    """
    Objetivo:
        Crear un enemigo con animación y comportamiento básico, usando imágenes ya cargadas.

    Parámetros:
        x (int): Posición horizontal inicial del enemigo.
        y (int): Posición vertical inicial del enemigo.
        imagenes (list[pygame.Surface]): Lista de imágenes para animar al enemigo.
        pantalla_ancho (int, opcional): Ancho de la pantalla para limitar el movimiento horizontal. Por defecto 800.

    Salida:
        dict: Diccionario que representa al enemigo, incluyendo imágenes, posición, velocidades y datos para animación.
    """
    return {
        "imagenes": imagenes,
        "index_imagen": 0,
        "rect": imagenes[0].get_rect(topleft=(x, y)),
        "velocidad_x": 1,
        "velocidad_y": 10,
        "contador_animacion": 0,
        "frecuencia_animacion": 20,
        "pantalla_ancho": pantalla_ancho
    }

def actualizar_enemigo(enemigo):
    """
    Objetivo:
        Actualizar la posición del enemigo y manejar su animación y rebote contra los bordes.

    Parámetros:
        enemigo (dict): Diccionario que representa al enemigo. Debe contener su rect, imágenes, velocidades y configuración de animación.

    Salida:
        None: La función modifica el estado del enemigo directamente.
    """
    enemigo["rect"].x += enemigo["velocidad_x"]

    if enemigo["rect"].x < 0 or enemigo["rect"].x > enemigo["pantalla_ancho"] - enemigo["rect"].width:
        enemigo["velocidad_x"] *= -1
        enemigo["rect"].y += enemigo["velocidad_y"]
        if enemigo["rect"].x < 0:
            enemigo["rect"].x = 0
        elif enemigo["rect"].x > enemigo["pantalla_ancho"] - enemigo["rect"].width:
            enemigo["rect"].x = enemigo["pantalla_ancho"] - enemigo["rect"].width

    enemigo["contador_animacion"] += 1
    if enemigo["contador_animacion"] >= enemigo["frecuencia_animacion"]:
        enemigo["contador_animacion"] = 0
        enemigo["index_imagen"] = (enemigo["index_imagen"] + 1) % len(enemigo["imagenes"])

def dibujar_enemigo(pantalla, enemigo):
    """
    Objetivo:
        Dibujar el enemigo en la pantalla utilizando su imagen actual.

    Parámetros:
        pantalla (pygame.Surface): Superficie donde se va a dibujar.
        enemigo (dict): Diccionario con los datos del enemigo, incluyendo su rectángulo e imagen actual.

    Salida:
        None: Dibuja directamente sobre la superficie de la pantalla.
    """
    imagen_actual = enemigo["imagenes"][enemigo["index_imagen"]]
    pantalla.blit(imagen_actual, enemigo["rect"])

def disparo_enemigo(enemigo):
    """
    Objetivo:
        Crear un disparo a partir de la posición del enemigo.

    Parámetros:
        enemigo (dict): Diccionario que representa al enemigo, con información de su rectángulo de posición.

    Salida:
        pygame.Rect: Rectángulo que representa el disparo generado desde el centro inferior del enemigo.
    """
    return pygame.Rect(enemigo["rect"].centerx - 2, enemigo["rect"].bottom, 5, 15)

