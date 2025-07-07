import json
import os

ARCHIVO_HIGHSCORE = "highscore.json"

def cargar_highscores(filename=ARCHIVO_HIGHSCORE):
    """
    Objetivo:
        Cargar la lista de highscores desde un archivo JSON.

    Parámetros:
        filename (str): Nombre del archivo de highscores. Por defecto "highscore.json".

    Salida:
        list: Lista de puntajes. Si el archivo no existe o está corrupto, devuelve una lista vacía.
    """
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data.get("highscores", [])
    except (json.JSONDecodeError, IOError):
        return []

def guardar_highscores(highscores, filename=ARCHIVO_HIGHSCORE):
    """
    Objetivo:
        Guardar la lista de highscores en un archivo JSON.

    Parámetros:
        highscores (list): Lista de puntajes.
        filename (str): Nombre del archivo donde se guardarán los datos. Por defecto "highscore.json".

    Salida:
        None
    """
    try:
        with open(filename, "w") as f:
            json.dump({"highscores": highscores}, f)
    except IOError:
        pass

def actualizar_highscores(nuevo_puntaje, filename=ARCHIVO_HIGHSCORE):
    """
    Objetivo:
        Agregar un nuevo puntaje, ordenarlo y guardar el top 10.

    Parámetros:
        nuevo_puntaje (int): El nuevo puntaje a agregar.
        filename (str): Nombre del archivo donde se guardarán los datos. Por defecto "highscore.json".

    Salida:
        list: Lista actualizada de highscores.
    """
    highscores = cargar_highscores(filename)
    highscores.append(nuevo_puntaje)
    highscores = sorted(highscores, reverse=True)[:10]
    guardar_highscores(highscores, filename)
    return highscores




