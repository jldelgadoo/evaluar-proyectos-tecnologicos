"""Verificar propiedades de la plantilla y del auditor sin datos de proyectos."""

import csv
import itertools
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from lectura_xlsx import leer_hojas
from proyectos import CAMPOS, CERO, Periodo, auditar, auditar_excel, preparar_plantilla, resumir


class ContratoDelModelo(unittest.TestCase):
    def test_plantilla_en_blanco(self):
        with TemporaryDirectory() as ruta:
            destino = Path(ruta) / "plantilla.xlsx"
            preparar_plantilla(destino)
            self.assertEqual(destino.read_bytes(), (RAIZ / "assets/evaluacion-tecnologica.xlsx").read_bytes())
            with self.assertRaises(FileExistsError):
                preparar_plantilla(destino)
            with ZipFile(destino) as libro:
                self.assertIsNone(libro.testzip())
            hojas = leer_hojas(destino, {"Supuestos", "Resumen", "Flujo mensual", "Sensibilidad", "Viabilidad"})
            for columna, fila in itertools.product("CDE", range(12, 27)):
                self.assertIn(hojas["Supuestos"].get(f"{columna}{fila}"), (None, ""))
            self.assertEqual(hojas["Resumen"]["B20"], "Pendiente")
            with self.assertRaisesRegex(ValueError, "Modelo pendiente"):
                auditar_excel(destino)

    def test_invariantes_de_caja(self):
        for movimientos in itertools.product((-1, 0, 1), repeat=4):
            with self.subTest(movimientos=movimientos):
                valores = [Decimal(x) for x in movimientos]
                serie = [Periodo(i, max(CERO, -x), max(CERO, x), CERO) for i, x in enumerate(valores)]
                totales = resumir(serie, CERO)
                acumulados = list(itertools.accumulate(valores))
                self.assertEqual(totales["caja_neta"], sum(valores))
                self.assertEqual(totales["van"], sum(valores))
                self.assertEqual(totales["deficit_maximo"], max(CERO, -min(acumulados)))
                self.assertEqual(totales["caja_neta"], totales["beneficios_de_caja"] - totales["desembolsos"])
                cruces = [i for i in range(1, len(valores)) if acumulados[i-1] < 0 <= acumulados[i]]
                self.assertEqual(totales["payback_mes"], min(cruces) if cruces else None)
                self.assertEqual(totales["deficit_posterior_a_recuperacion"], bool(cruces) and min(acumulados[cruces[0]:]) < 0)

    def test_horas_y_tasa_pendientes(self):
        periodo = Periodo(0, CERO, CERO, CERO)
        con_horas = resumir([periodo, Periodo(1, CERO, CERO, Decimal(1))], CERO)
        sin_horas = resumir([periodo, Periodo(1, CERO, CERO, None)], None)
        self.assertEqual(con_horas["caja_neta"], sin_horas["caja_neta"])
        self.assertIsNone(sin_horas["horas_liberadas"])
        self.assertIsNone(sin_horas["van"])
        self.assertIsNone(sin_horas["roi_simple"])

    def test_integridad_serie_csv(self):
        def registro(mes):
            fila = dict.fromkeys(CAMPOS, "0")
            fila.update(alternativa="A", escenario="B", moneda="M", mes=str(mes))
            return fila

        with TemporaryDirectory() as ruta:
            archivo = Path(ruta) / "flujos.csv"
            for cambios in ({"mes": "0"}, {"mes": "2"}, {"moneda": "N"}, {"implementacion": "1"}, {"gasto_retirado": ""}):
                with self.subTest(cambios=cambios):
                    with archivo.open("w", newline="", encoding="utf-8") as salida:
                        escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
                        escritor.writeheader()
                        escritor.writerows([registro(0), {**registro(1), **cambios}])
                    with self.assertRaises(ValueError):
                        auditar(archivo, CERO)


if __name__ == "__main__":
    unittest.main()
