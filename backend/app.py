from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # Permettre les requêtes CORS

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
mail = Mail(app)

from routes import init_routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
