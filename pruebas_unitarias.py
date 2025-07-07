from puntaje import cargar_highscores, guardar_highscores
import os

# Archivo temporal para las pruebas
test_file = "test_highscore.txt"

# Prueba guardar y cargar highscores
"""
Objetivo:
    Probar que se puede guardar y cargar correctamente una lista de highscores desde un archivo JSON.

Procedimiento:
    1. Se guarda una lista de puntajes en un archivo temporal.
    2. Se carga la lista y se verifica que los datos coincidan.
"""

guardar_highscores([100, 80, 60], test_file)
resultado = cargar_highscores(test_file)
assert resultado == [100, 80, 60], f"Error: Se esperaba [100, 80, 60] pero se obtuvo {resultado}"

# Prueba cargar highscores cuando no existe el archivo
"""
Objetivo:
    Verificar que si el archivo no existe, la función devuelva una lista vacía.

Procedimiento:
    1. Se elimina el archivo de prueba si existe.
    2. Se llama a cargar_highscores y se espera una lista vacía.
"""

if os.path.exists(test_file):
    os.remove(test_file)

resultado_no_archivo = cargar_highscores(test_file)
assert resultado_no_archivo == [], f"Error: Se esperaba [] pero se obtuvo {resultado_no_archivo}"

print("Todas las pruebas pasaron correctamente.")






