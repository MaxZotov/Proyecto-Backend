import re
from src.validators.commons import (
    rechazar_campos_desconocidos,
    campos_requeridos,
    requiere_objeto_json,
    validar_booleano,
    validar_texto,
)

PATRON_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def validar_cancha(data, parcial=False):
    requiere_objeto_json(data)
    permitidos = {"nombre", "id_deporte", "precio_hora", "techada", "activa"}
    rechazar_campos_desconocidos(data, permitidos)
    if not parcial:
        campos_requeridos(data, {"nombre", "id_deporte", "precio_hora"})
    resultado = {}
    if "nombre" in data:
        resultado["nombre"] = validar_texto(data["nombre"], "nombre")
    if "id_deporte" in data:
        resultado["id_deporte"] = validar_int_positivo(data["id_deporte"], "id_deporte")
    if "precio_hora" in data:
        resultado["precio_hora"] = validar_int_positivo(data["precio_hora"], "precio_hora")
    if "techada" in data:
        resultado["techada"] = validar_booleano(data["techada"], "techada")
    if "activa" in data:
        resultado["activa"] = validar_booleano(data["activa"], "activa")
    return resultado

def validar_socio(data, parcial=False):
    requiere_objeto_json(data)
    permitidos = {"nombre", "email", "activo"}
    rechazar_campos_desconocidos(data,permitidos)
    if not parcial:
        campos_requeridos(data,{"nombre", "email"})
    resultado = {}
    if "nombre" in data:
        resultado["nombre"] = validar_texto(data["nombre"],"nombre")
    if "email" in data:
        email = validar_texto(data["email"],"email").lower()
        if not PATRON_EMAIL.fullmatch(email):
            raise ValueError ("El campo email no tiene un formato valido")
        resultado ["email"] = email
    if "activo" in data:
        resultado["activo"] = validar_booleano(data["activo"],"activo") 
    return resultado