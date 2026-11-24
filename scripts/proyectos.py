#!/usr/bin/env python3
"""Preparar la plantilla de evaluación y comprobar series mensuales de caja."""

import argparse
import csv
import json
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, DecimalException, InvalidOperation
from pathlib import Path

from lectura_xlsx import leer_hojas

RAIZ = Path(__file__).resolve().parents[1]
EGRESOS = ("implementacion", "operacion_fija", "operacion_variable")
BENEFICIOS = ("gasto_retirado", "ahorro_actividad", "margen_incremental")
CAMPOS = ("alternativa", "escenario", "moneda", "mes", *EGRESOS, *BENEFICIOS, "horas_liberadas")
CERO = Decimal(0)


@dataclass(frozen=True)
class Periodo:
    mes: int
    egresos: Decimal
    beneficios: Decimal
    horas: Decimal | None


def decimal_finito(texto: str, campo: str) -> Decimal:
    try:
        numero = Decimal(texto.strip())
    except InvalidOperation as error:
        raise ValueError(f"{campo}: se requiere un número decimal con punto.") from error
    if not numero.is_finite():
        raise ValueError(f"{campo}: el valor debe ser finito.")
    return numero


def preparar_plantilla(destino: Path) -> None:
    if destino.suffix.lower() != ".xlsx":
        raise ValueError("El archivo de salida debe tener extensión .xlsx.")
    plantilla = RAIZ / "assets" / "evaluacion-tecnologica.xlsx"
    with plantilla.open("rb") as origen, destino.open("xb") as salida:
        try:
            shutil.copyfileobj(origen, salida)
        except OSError:
            salida.close()
            destino.unlink(missing_ok=True)
            raise


def leer_periodo(fila: dict[str, str]) -> Periodo:
    mes = int(fila["mes"])
    if mes < 0:
        raise ValueError("El mes debe ser un entero desde cero.")
    valores = {campo: decimal_finito(fila[campo], campo) for campo in (*EGRESOS, *BENEFICIOS)}
    for campo in EGRESOS:
        if valores[campo] > 0:
            raise ValueError(f"{campo}: un egreso debe ser negativo o cero.")
    for campo in ("gasto_retirado", "ahorro_actividad"):
        if valores[campo] < 0:
            raise ValueError(f"{campo}: el ahorro debe ser positivo o cero.")
    horas = fila["horas_liberadas"].strip()
    return Periodo(
        mes,
        -sum((valores[c] for c in EGRESOS), CERO),
        sum((valores[c] for c in BENEFICIOS), CERO),
        decimal_finito(horas, "horas_liberadas") if horas else None,
    )


def resumir(periodos: list[Periodo], tasa: Decimal | None) -> dict:
    periodos = sorted(periodos, key=lambda p: p.mes)
    if len(periodos) < 2 or any(p.mes != indice for indice, p in enumerate(periodos)):
        raise ValueError("Incluir el mes 0 y todos los meses hasta el horizonte, una sola vez.")
    saldo = minimo = egresos = beneficios = horas = actual = CERO
    recuperacion = None
    recaida = False
    horas_completas = True
    for p in periodos:
        flujo = p.beneficios - p.egresos
        anterior = saldo
        saldo += flujo
        minimo = min(minimo, saldo)
        egresos += p.egresos
        beneficios += p.beneficios
        if recuperacion is None and anterior < 0 <= saldo:
            recuperacion = p.mes
        if recuperacion is not None and saldo < 0:
            recaida = True
        if tasa is not None:
            actual += flujo / ((1 + tasa) ** (Decimal(p.mes) / 12))
        if p.horas is None:
            horas_completas = False
        else:
            horas += p.horas
    estado = "recuperado" if recuperacion is not None else (
        "sin_deficit" if minimo == 0 else "fuera_del_horizonte"
    )
    return {
        "horizonte_meses": periodos[-1].mes,
        "desembolsos": egresos,
        "beneficios_de_caja": beneficios,
        "caja_neta": saldo,
        "deficit_maximo": abs(minimo),
        "payback_estado": estado,
        "payback_mes": recuperacion,
        "deficit_posterior_a_recuperacion": recaida,
        "van": actual if tasa is not None else None,
        "roi_simple": saldo / egresos if egresos else None,
        "horas_liberadas": horas if horas_completas else None,
    }


def auditar(archivo: Path, tasa: Decimal | None) -> list[dict]:
    if tasa is not None and tasa <= -1:
        raise ValueError("La tasa anual efectiva debe ser superior a −100 %.")
    grupos = defaultdict(list)
    monedas = {}
    with archivo.open(encoding="utf-8-sig", newline="") as entrada:
        lector = csv.DictReader(entrada, strict=True)
        if sorted(lector.fieldnames or []) != sorted(CAMPOS):
            raise ValueError("Los encabezados deben coincidir con templates/flujos.csv.")
        for fila in lector:
            try:
                if None in fila or any(valor is None for valor in fila.values()):
                    raise ValueError("La cantidad de columnas difiere del encabezado.")
                alternativa, escenario, moneda = (fila[c].strip() for c in CAMPOS[:3])
                if not all((alternativa, escenario, moneda)):
                    raise ValueError("Indicar alternativa, escenario y moneda.")
                clave = (alternativa, escenario)
                if monedas.setdefault(clave, moneda) != moneda:
                    raise ValueError("La moneda cambia dentro de la misma alternativa y escenario.")
                grupos[clave].append(leer_periodo(fila))
            except ValueError as error:
                raise ValueError(f"Fila {lector.line_num}: {error}") from error
    if not grupos:
        raise ValueError("El archivo contiene encabezados y necesita flujos para auditar.")
    resultados = []
    for clave, periodos in sorted(grupos.items()):
        try:
            totales = resumir(periodos, tasa)
        except ValueError as error:
            raise ValueError(f"{clave[0]} / {clave[1]}: {error}") from error
        resultados.append({
            "alternativa": clave[0], "escenario": clave[1],
            "moneda": monedas[clave], "tasa_anual_efectiva": tasa, **totales,
        })
    return resultados


def auditar_excel(archivo: Path) -> dict:
    hojas = leer_hojas(archivo, {"Supuestos", "Flujo mensual", "Resumen", "Sensibilidad"})
    supuestos, flujo = hojas["Supuestos"], hojas["Flujo mensual"]
    estado = supuestos.get("B29")
    if estado != "Calculable":
        raise ValueError(f"Modelo pendiente ({estado or 'sin resultados guardados'}). Completa los datos, recalcula y guarda el libro.")
    horizonte = supuestos.get("B7")
    if not isinstance(horizonte, Decimal) or horizonte % 1 or not 1 <= horizonte <= 60:
        raise ValueError("El horizonte guardado está fuera del alcance de la plantilla.")
    tasa = supuestos.get("B8")
    if tasa in (None, ""):
        tasa = None
    elif not isinstance(tasa, Decimal) or tasa <= -1:
        raise ValueError("Revisa la tasa guardada en Supuestos antes de auditar el libro.")
    diferencias = []

    def comparar(hoja: str, celda: str, esperado, margen=Decimal("0.005")) -> None:
        guardado = hojas[hoja].get(celda)
        if isinstance(esperado, Decimal) and isinstance(guardado, Decimal):
            coincide = abs(esperado - guardado) <= margen
        else:
            coincide = esperado == guardado
        if not coincide:
            diferencias.append({"celda": f"{hoja}!{celda}", "esperado": esperado, "guardado": guardado})

    periodos = []
    saldo = CERO
    for mes in range(int(horizonte) + 1):
        fila = mes + 12
        comparar("Flujo mensual", f"A{fila}", Decimal(mes), CERO)
        movimientos = {}
        for col, campo in zip("DEFGHI", (*EGRESOS, *BENEFICIOS)):
            valor = flujo.get(f"{col}{fila}")
            if not isinstance(valor, Decimal):
                raise ValueError(f"Falta un importe numérico guardado en Flujo mensual!{col}{fila}. Recalcula y guarda el libro.")
            movimientos[campo] = str(valor)
        horas = flujo.get(f"M{fila}")
        if horas not in (None, "") and not isinstance(horas, Decimal):
            raise ValueError(f"Revisa las horas guardadas en Flujo mensual!M{fila}.")
        periodo = leer_periodo({"mes": str(mes), "horas_liberadas": "" if horas in (None, "") else str(horas), **movimientos})
        periodos.append(periodo)
        neto = periodo.beneficios - periodo.egresos
        saldo += neto
        comparar("Flujo mensual", f"J{fila}", neto)
        comparar("Flujo mensual", f"K{fila}", saldo)
    totales = resumir(periodos, tasa)
    recuperacion = totales["payback_mes"]
    if recuperacion is None:
        recuperacion = "Sin déficit" if totales["payback_estado"] == "sin_deficit" else "Fuera del horizonte"
    posterior = "Sí" if totales["deficit_posterior_a_recuperacion"] else "No"
    if totales["payback_mes"] is None:
        posterior = "Sin recuperación previa"
    medidas = [totales["desembolsos"], totales["beneficios_de_caja"], saldo,
               totales["van"] if tasa is not None else "Sin tasa", recuperacion,
               totales["roi_simple"] if totales["desembolsos"] else "Sin desembolsos",
               totales["deficit_maximo"], totales["horas_liberadas"] if totales["horas_liberadas"] is not None else supuestos.get("B31"), posterior]
    for i, (col, medida) in enumerate(zip("BCDEFGHIJ", medidas)):
        margen = Decimal("0.00000005") if col == "G" else Decimal("0.005")
        comparar("Flujo mensual", f"{col}8", medida, margen)
        comparar("Resumen", f"B{18+i}", medida, margen)
    comparar("Sensibilidad", "D20", saldo)
    return {"archivo": str(archivo), "escenario": supuestos.get("B5"), "moneda": supuestos.get("B6"),
            "estado": "con diferencias" if diferencias else "conciliado", "diferencias": diferencias, **totales}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    acciones = parser.add_subparsers(dest="accion", required=True)
    plantilla = acciones.add_parser("plantilla", help="Crear una copia nueva del Excel en blanco.")
    plantilla.add_argument("salida", type=Path, help="Ruta nueva con extensión .xlsx.")
    auditoria = acciones.add_parser("auditar", help="Conciliar flujos mensuales y emitir JSON.")
    auditoria.add_argument("csv", type=Path, help="Archivo UTF-8 con los encabezados de templates/flujos.csv.")
    auditoria.add_argument("--tasa-anual", help="Tasa efectiva anual en fracción decimal con punto.")
    excel = acciones.add_parser("auditar-excel", help="Contrastar directamente el escenario guardado en un XLSX de la plantilla.")
    excel.add_argument("archivo", type=Path, help="Libro completado, recalculado y guardado.")
    args = parser.parse_args()
    try:
        if args.accion == "plantilla":
            preparar_plantilla(args.salida)
            print(f"Plantilla creada en {args.salida}")
        elif args.accion == "auditar-excel":
            informe = auditar_excel(args.archivo)
            print(json.dumps(informe, ensure_ascii=False, indent=2, default=str))
            return 1 if informe["diferencias"] else 0
        else:
            tasa = decimal_finito(args.tasa_anual, "tasa anual") if args.tasa_anual is not None else None
            print(json.dumps(auditar(args.csv, tasa), ensure_ascii=False, indent=2, default=str))
    except FileExistsError:
        parser.exit(2, "El archivo de salida ya existe. Elige una ruta nueva.\n")
    except (OSError, ValueError, DecimalException, csv.Error) as error:
        parser.exit(2, f"Error: {error}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
