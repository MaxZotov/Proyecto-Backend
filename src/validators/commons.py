from datetime import datetime

from src.constants import (
    HORA_CIERRE,
    HORA_APERTURA,
    HORA_RESERVACION_MAXIMA,
    HORA_RESERVACION_MINIMA,
)
from src.utils import gmt_menos_3_actual, analisis_iso_datetime

def requiere_objeto_json(data):
    if not isinstance(data, dict) or not data:
        raise ValueError ("El cuerpo debe ser un objeto JSON no vacio")

def rechazar_campos_desconocidos(data, permitido):
    desconocido = set(data) - set(permitido)
    if desconocido:
        raise ValueError(f"campos desconocidos : {','.join(sorted(desconocido))}")

def campos_requeridos(data,campos):
    faltante = [campo for campo in campos if campo not in data]
    if faltante:
        raise ValueError (f"Faltan campos obligatorios: {','.join(faltante)}")

def validar_texto(valor,campo):
    if not isinstance(valor,str) or not valor.strip():
        raise ValueError (f"el campo '{campo}' no puede estar vacio")
    return valor.strip()

def validar_booleano(valor,campo):
    if not isinstance(valor,bool):
        raise ValueError (f"el campo '{campo}' debe ser un booleano")
    return valor

