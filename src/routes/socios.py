from flask import Blueprint, jsonify, request
from mysql.connector import Error

from src.services.socios_service import crear_socio, listar_socios, obtener_socio_id, actualizar_socio
from src.utils import error, respuesta_paginacion, analisis_bool, analisis_paginacion, rechazar_query_desconocida
from src.validators.entities import validar_socio

socios_bp = Blueprint("socios", __name__)

@socios_bp.route("/socios", methods=["GET"])
def get_socios():
    try:
        rechazar_query_desconocida({"nombre", "activo", "_limit", "_offset"})
        filtros = {"nombre": request.args.get("nombre")}
        if "activo" in request.args:
            filtros["activo"] = analisis_bool(request.args.get("activo"), "activo")
        limit, offset = analisis_paginacion()
        filas, total = listar_socios(filtros, limit, offset)
        if not filas:
            return "", 204
        

        return jsonify(respuesta_paginacion("socios", filas, total, limit, offset)), 200
    except ValueError as exc:
        return error("ERROR_VALIDACION", "Parámetros inválidos", str(exc), 400)
    except Error:
        return error("ERROR_BASE_DE_DATOS", "No se pudo consultar socios", "base de datos no disponible", 500)

@socios_bp.route("/socios", methods=["POST"])
def post_socio():
    try:
        datos = request.get_json(silent=True)
        socio_validado = validar_socio(datos)
        socio = crear_socio(socio_validado)
        return jsonify(socio), 201
    except ValueError as exc:
        return error("ERROR_VALIDACION", "Datos inválidos", str(exc), 400)
    except Error as exc:
        if getattr(exc, "errno", None) == 1062:
            return error("ERROR_DUPLICADO", "El email ya existe", "El email proporcionado ya está registrado", 409)
        return error("ERROR_BASE_DE_DATOS", "No se pudo crear socio", str(exc), 500)

@socios_bp.route("/socios/<int:socio_id>", methods=["GET"])
def get_socio(socio_id):
    try:
        socio = obtener_socio_id(socio_id)
        
        if not socio:
            return error("NO_ENCONTRADO", "Socio no encontrado", f"No existe un socio con el ID {socio_id}", 404)
            
        return jsonify(socio), 200
        
    except Error:
        return error("ERROR_BASE_DE_DATOS", "No se pudo consultar el socio", "Base de datos no disponible", 500)

@socios_bp.route("/socios/<int:socio_id>", methods=["PATCH"])
def patch_socio(socio_id):
    try:
        datos = request.get_json(silent=True)
        datos_validados = validar_socio(datos, parcial=True)
        
        if not datos_validados:
            return error("ERROR_VALIDACION", "Datos inválidos", "No se proporcionaron campos para actualizar", 400)
            
        socio_existente = obtener_socio_id(socio_id)
        if not socio_existente:
            return error("NO_ENCONTRADO", "Socio no encontrado", f"No existe un socio con el ID {socio_id}", 404)
            
        socio_actualizado = actualizar_socio(socio_id, datos_validados)
        
        return jsonify(socio_actualizado), 200
        
    except ValueError as exc:
        return error("ERROR_VALIDACION", "Datos inválidos", str(exc), 400)
    except Error as exc:
        if getattr(exc, "errno", None) == 1062:
            return error("ERROR_DUPLICADO", "El email ya existe", "El email proporcionado ya está registrado por otro socio", 409)
        return error("ERROR_BASE_DE_DATOS", "No se pudo actualizar el socio", str(exc), 500)