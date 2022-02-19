from flask_cors import CORS
from flask_jwt_extended import JWTManager

def register_extensions(app):
    # Registers flask extensions
    jwt.init_app(app)
    cors.init_app(app)

cors = CORS()
jwt = JWTManager()
