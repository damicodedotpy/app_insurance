# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask
# ******************************OWN LIBRARIES*********************************
from config import AppConfiguration
from extensions import db, migrate
from src.models import *
from src.routes.units import blp as UnitsBlueprint
from src.routes.bussiness import blp as BusinessBlueprint
from src.routes.insurance import blp as InsuranceBlueprint
# ***********************************CODE*************************************
def create_app():
    # Flask instance
    app = Flask(__name__)
    # App configuration
    app.config.from_object(AppConfiguration)
    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # Registered blueprints
    app.register_blueprint(UnitsBlueprint)
    app.register_blueprint(BusinessBlueprint)
    app.register_blueprint(InsuranceBlueprint)

    # Database creation
    with app.app_context():
        db.create_all()

    return app



