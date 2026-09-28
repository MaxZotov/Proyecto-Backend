from src.db import execute, fetch_all, fetch_one

def listar_socios(filtros, limit, offset):
    condiciones = []
    parametros = []
    if filtros.get("nombre") is not None:
        condiciones.append("LOWER(nombre) LIKE %s")
        parametros.append(f"%{filtros['nombre'].lower()}%")
    if filtros.get("activo") is not None:
        condiciones.append("activo = %s")
        parametros.append(filtros["activo"])
    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""
    filas = fetch_all(f"SELECT id, nombre, email, activo FROM socios {where} ORDER BY id LIMIT %s OFFSET %s", (*parametros, limit, offset))
    conteo = fetch_one(f"SELECT COUNT(*) AS total FROM socios {where}", parametros)
    return filas, conteo["total"]

def crear_socio(data):
    activo = data.get("activo", True)
    id_socio = execute(
        "INSERT INTO socios (nombre, email, activo) VALUES (%s, %s, %s)",
        (data["nombre"], data["email"], activo),
        return_id=True
    )
    return obtener_socio_id(id_socio)

def obtener_socio_id(id_socio):
    socio = fetch_one("SELECT id, nombre, email, activo FROM socios WHERE id = %s", (id_socio,))
    return socio

def actualizar_socio(id_socio, datos):
    campos_permitidos = ["nombre", "email", "activo"]
    
    campos_set = []
    valores = []
    
    for clave, valor in datos.items():
        if clave in campos_permitidos:
            campos_set.append(f"{clave} = %s")
            valores.append(valor)
            
    if not campos_set:
        return obtener_socio_id(id_socio)
        
    valores.append(id_socio)
    
    clausula_set = ", ".join(campos_set)
    query = f"UPDATE socios SET {clausula_set} WHERE id = %s"
    
    execute(query, tuple(valores))
    
    return obtener_socio_id(id_socio)