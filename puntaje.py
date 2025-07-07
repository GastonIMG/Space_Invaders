import json
import os

ARCHIVO_HIGHSCORE = "highscore.json"

def cargar_highscore():
    """
    Objetivo:
        Cargar la mejor puntuación (highscore) desde un archivo JSON.

    Parámetros:
        Ninguno.

    Salida:
        int: El valor del highscore almacenado. Si no existe el archivo o está corrupto, devuelve 0.
    """
    if not os.path.exists(ARCHIVO_HIGHSCORE):
        return 0
    try:
        with open(ARCHIVO_HIGHSCORE, "r") as f:
            data = json.load(f)
            return data.get("highscore", 0)
    except (json.JSONDecodeError, IOError):
        return 0

def guardar_highscore(puntuacion):
    """
    Objetivo:
        Guardar la mejor puntuación (highscore) en un archivo JSON.

    Parámetros:
        puntuacion (int): La puntuación a guardar como récord.

    Salida:
        None: Guarda el valor en el archivo, sin retorno.
    """
    try:
        with open(ARCHIVO_HIGHSCORE, "w") as f:
            json.dump({"highscore": puntuacion}, f)
    except IOError:
        pass

def calcular_velocidad_disparo(tiempo_ms):
    """
    Objetivo:
        Calcular la velocidad de disparo de los enemigos en función del tiempo transcurrido en milisegundos.

    Parámetros:
        tiempo_ms (int): Tiempo transcurrido en milisegundos desde el inicio del juego o nivel.

    Salida:
        int: Velocidad calculada para el disparo, que aumenta cada 30 segundos.
    """
    velocidad_base = 5
    incremento = (tiempo_ms // 30000)  # Cada 30 segundos aumenta 1
    return velocidad_base + incremento

