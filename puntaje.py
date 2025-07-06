import json
import os

ARCHIVO_HIGHSCORE = "highscore.json"


def cargar_highscore():
    """
    Carga el highscore desde un archivo JSON.
    Si el archivo no existe o está corrupto, devuelve 0.
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
    Guarda el highscore en un archivo JSON.
    """
    try:
        with open(ARCHIVO_HIGHSCORE, "w") as f:
            json.dump({"highscore": puntuacion}, f)
    except IOError:
        pass

def calcular_velocidad_disparo(tiempo_ms):
    """
    Calcula la velocidad de disparo de los enemigos en función del tiempo transcurrido.
    Por ejemplo, aumenta la velocidad cada 30 segundos.
    """
    velocidad_base = 5
    incremento = (tiempo_ms // 30000)  # Cada 30 segundos aumenta 1
    return velocidad_base + incremento
