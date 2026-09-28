import os
from flask import Flask
from dotenv import load_dotenv

from src.routes.canchas import canchas_bp
from src.routes.deportes import deportes_bp
from src.routes.bloqueos import bloqueos_bp
from src.routes.reservas import reservas_bp
from src.routes.socios import socios_bp

load_dotenv()

def crear_app():
	app = Flask(__name__)
	app.json.sort_keys = False

	app.register_blueprint(deportes_bp)
	app.register_blueprint(canchas_bp)
	app.register_blueprint(bloqueos_bp)
	app.register_blueprint(socios_bp)
	app.register_blueprint(reservas_bp)

	@app.errorhandler(404)
	def not_found(_error):
		return jsonify({"errors": [{
			"code": "RECURSO_NO_ENCONTRADO",
			"message": "El recurso no existe",
			"level": "error",
			"description": "La ruta o el identificador solicitado no existe"
		}]}), 404

	@app.errorhandler(405)
	def method_not_allowed(_error):
		return jsonify({"errors": [{
			"code": "METODO_NO_PERMITIDO",
			"message": "Método HTTP no permitido",
			"level": "error",
			"description": "La ruta no admite el método HTTP recibido"
		}]}), 405

	@app.errorhandler(400)
	def bad_request(exc):
		return jsonify({"errors": [{
			"code": "ERROR_VALIDACION",
			"message": "Solicitud inválida",
			"level": "error",
			"description": exc.description
		}]}), 400

	@app.errorhandler(Exception)
	def internal_error(_error):
		return jsonify({"errors": [{
			"code": "ERROR_INTERNO",
			"message": "Ocurrió un error interno",
			"level": "error",
			"description": "El servidor no pudo completar la solicitud"
		}]}), 500

	return app


app = crear_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
