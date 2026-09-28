
from flask import Blueprint, jsonify, request
from mysql.connector import Error

from src.services.canchas_service import (
    create_court,
    delete_court,
    get_court,
    list_available,
    list_courts,
    update_court,
)
from src.utils import (
    clean_records,
    error,
    pagination_response,
    parse_bool,
    parse_date,
    parse_id,
    parse_pagination,
    reject_unknown_query,
)
from src.validators.common import validate_interval
from src.validators.entities import validate_court


canchas_bp = Blueprint("canchas", __name__)


def _query_filters():
    filters = {}
    if "id_deporte" in request.args:
        filters["id_deporte"] = parse_id(request.args["id_deporte"], "id_deporte")
    if "nombre" in request.args:
        filters["nombre"] = request.args["nombre"]
    for field in ("techada", "activa"):
        if field in request.args:
            filters[field] = parse_bool(request.args[field], field)
    return filters


@canchas_bp.route("/canchas", methods=["GET"])
def get_canchas():
    try:
        reject_unknown_query({"id_deporte", "nombre", "techada", "activa", "_limit", "_offset"})
        filters = _query_filters()
        limit, offset = parse_pagination()
        rows, total = list_courts(filters, limit, offset)
        if not rows:
            return "", 204
        return jsonify(pagination_response("canchas", clean_records(rows), total, limit, offset)), 200
    except ValueError as exc:
        return error("ERROR_VALIDACION", "Parámetros inválidos", str(exc), 400)
    except Error:
        return error("ERROR_BASE_DATOS", "No se pudieron consultar las canchas", "La base de datos no está disponible", 500)


@canchas_bp.route("/canchas", methods=["POST"])
def post_cancha():
    try:
        data = validate_court(request.get_json(silent=True))
        court = create_court(data)
        return jsonify(court), 201
    except ValueError as exc:
        return error("ERROR_VALIDACION", "El cuerpo es inválido", str(exc), 400)
    except Error as exc:
        if getattr(exc, "errno", None) == 1452:
            return error("DEPORTE_NO_ENCONTRADO", "Deporte inexistente", "El id_deporte no existe", 404)
        return error("ERROR_BASE_DATOS", "No se pudo crear la cancha", str(exc), 500)