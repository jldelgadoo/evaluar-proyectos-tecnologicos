"""Leer los valores guardados en hojas XLSX, incluidas cadenas y fórmulas calculadas."""

from decimal import Decimal
from pathlib import Path
from posixpath import dirname, join, normpath
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

HOJA = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
DOC = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PAQUETE = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def texto(elemento: ET.Element) -> str:
    partes = elemento.findall(HOJA + "t") + elemento.findall(HOJA + "r/" + HOJA + "t")
    return "".join(p.text or "" for p in partes)


def parte(archivo: ZipFile, ruta: str) -> ET.Element:
    informacion = archivo.getinfo(ruta)
    if informacion.file_size > 40 * 1024 * 1024:
        raise ValueError(f"La parte {ruta} supera el tamaño admitido para revisar esta plantilla.")
    return ET.fromstring(archivo.read(informacion))


def valores(hoja: ET.Element, cadenas: list[str]) -> dict:
    celdas = {}
    for celda in hoja.iter(HOJA + "c"):
        dato = celda.findtext(HOJA + "v")
        tipo = celda.get("t", "n")
        if tipo == "inlineStr":
            entrada = celda.find(HOJA + "is")
            dato = texto(entrada) if entrada is not None else ""
        elif tipo == "s" and dato:
            indice = int(dato)
            if not 0 <= indice < len(cadenas):
                raise ValueError("El índice de texto guardado en el libro no es válido.")
            dato = cadenas[indice]
        elif tipo == "n" and dato:
            dato = Decimal(dato)
            if not dato.is_finite():
                raise ValueError(f"Valor no finito en la celda {celda.get('r')}.")
        celdas[celda.attrib["r"]] = dato
    return celdas


def leer_hojas(ruta: Path, nombres: set[str]) -> dict:
    libro = "xl/workbook.xml"
    try:
        with ZipFile(ruta) as archivo:
            raiz = parte(archivo, libro)
            relaciones = parte(archivo, "xl/_rels/workbook.xml.rels")
            destinos = {}
            cadenas = []
            for rel in relaciones.findall(PAQUETE + "Relationship"):
                if rel.get("TargetMode") == "External":
                    continue
                destino = rel.attrib["Target"]
                ruta_interna = destino.lstrip("/") if destino.startswith("/") else normpath(join(dirname(libro), destino))
                tipo = rel.get("Type", "").rsplit("/", 1)[-1]
                if tipo == "worksheet":
                    destinos[rel.attrib["Id"]] = ruta_interna
                elif tipo == "sharedStrings":
                    cadenas = [texto(si) for si in parte(archivo, ruta_interna).findall(HOJA + "si")]
            resultado = {}
            for hoja in raiz.iter(HOJA + "sheet"):
                nombre = hoja.attrib["name"]
                if nombre in nombres:
                    destino = destinos[hoja.attrib[DOC + "id"]]
                    resultado[nombre] = valores(parte(archivo, destino), cadenas)
            if nombres - resultado.keys():
                raise ValueError("Faltan hojas de la plantilla: " + ", ".join(sorted(nombres - resultado.keys())) + ".")
            return resultado
    except (BadZipFile, KeyError, ET.ParseError) as error:
        raise ValueError("El archivo no contiene un libro XLSX legible con la estructura esperada.") from error
