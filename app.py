import os
from flask import Flask
from src.routes.socios import socios_bp, canchas_bp

app = Flask(__name__)

app.register_blueprint(socios_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint()
app.register_blueprint()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
