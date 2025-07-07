import unittest
import os
from puntaje import cargar_highscore, guardar_highscore, calcular_velocidad_disparo

class TestPuntaje(unittest.TestCase):
    
    def setUp(self):
        # Archivo temporal para las pruebas
        self.test_file = "test_highscore.txt"
        self.original_file = "highscore.txt"
        # Backup si existe
        if os.path.exists(self.original_file):
            os.rename(self.original_file, self.original_file + ".bak")
    
    def tearDown(self):
        # Elimina el archivo de prueba
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # Restaura el backup
        if os.path.exists(self.original_file + ".bak"):
            os.rename(self.original_file + ".bak", self.original_file)

    def test_guardar_y_cargar_highscore(self):
        guardar_highscore(100, self.test_file)
        resultado = cargar_highscore(self.test_file)
        self.assertEqual(resultado, 100)

    def test_highscore_no_existente(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        resultado = cargar_highscore(self.test_file)
        self.assertEqual(resultado, 0)

    def test_calculo_velocidad_disparo(self):
        self.assertEqual(calcular_velocidad_disparo(0), 5)
        self.assertEqual(calcular_velocidad_disparo(10000), 7)
        self.assertEqual(calcular_velocidad_disparo(25000), 10)

if __name__ == "__main__":
    unittest.main()


###### hacemos modificaciones, lo hacemos directamenteen el main o hacemos modificaciones aca cambiando a assert xq lo que tenemos ahora es de obecto

