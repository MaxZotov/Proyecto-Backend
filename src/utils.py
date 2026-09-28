from datetime import date, datetime, time, timedelta
from urllib.parse import urlencode
from flask import request
from src.constants import LIMIT_DEFAULT, GMT_MENOS_3, LIMIT_MAXIMO

def error(codigo, mensaje, descripcion, status):
    body = {
        "errores": [{
            "codigo": codigo,
            "mensaje": mensaje,
            "nivel": "error",
            "descripcion": descripcion,
        }]
    }
    return body, status

def analisis_id(valor, campo="id"):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"El campo '{campo}' debe ser un entero.")
    if numero <= 0:
        raise ValueError(f"El campo '{campo}' debe ser un entero positivo.")
    return numero

def analisis_bool(valor, campo):
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str) and valor.lower() in ("true", "false"):
        return valor.lower() == "true"
    raise ValueError(f"El campo '{campo}' debe ser 'true' o 'false'.")

def analisis_paginacion():
    try:
        limit = int(request.args.get("_limit", LIMIT_DEFAULT))
        offset = int(request.args.get("_offset", 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("_limit y _offset deben ser enteros.") from exc
    if not 1 <= limit <= LIMIT_MAXIMO:
        raise ValueError(f"_limit debe estar entre 1 y {LIMIT_MAXIMO}")
    if offset < 0:
        raise ValueError("_offset debe ser mayor o igual a 0")
    return limit, offset

def rechazar_query_desconocida(permitidas):
    desconocidas = set(request.args.keys()) - set(permitidas)
    if desconocidas:
        raise ValueError(f"Parámetros de query desconocidos: {', '.join(sorted(desconocidas))}")

def respuesta_paginacion(key, items, total, limit, offset):
    base = request.base_url
    query = request.args.to_dict()
    ultimo_offset = (max(total - 1, 0) // limit) * limit if limit > 0 else 0

    def link(offset_pagina):
        parametros = dict(query)
        parametros["_limit"] = limit
        parametros["_offset"] = offset_pagina
        return {"href": f"{base}?{urlencode(parametros)}"}

    links = {
        "_primero": link(0),
        "_previo": link(max(offset - limit, 0)),
        "_siguiente": link(offset + limit),
        "_ultimo": link(ultimo_offset),
    }
    if offset == 0:
        links["_previo"] = None
    if offset + limit >= total:
        links["_siguiente"] = None

    return {key: items, "_links": links}

def analisis_iso_datetime(valor):
    if not isinstance(valor, str):
        raise ValueError("la fecha debe ser un texto ISO 8601")
    try:
        return datetime.strptime(valor, "%Y-%m-%dT%H:%M:%S.%f-03:00")
    except ValueError as exc:
        raise ValueError("la fecha debe ser un texto ISO 8601 GMT-3 con 6 decimales") from exc

def analisis_fecha(valor, campo="fecha"):
    if not isinstance(valor, str):
        raise ValueError(f"El campo '{campo}' debe tener formato YYYY-MM-DD")
    try:
        return date.fromisoformat(valor)
    except ValueError as exc:
        raise ValueError(f"El campo '{campo}' debe tener formato YYYY-MM-DD") from exc

def gmt_menos_3_actual():
    return datetime.now(GMT_MENOS_3).replace(tzinfo=None)
