# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jinja2 import Environment
# ******************************OWN LIBRARIES*********************************

# ***********************************CODE*************************************
db = SQLAlchemy()
migrate = Migrate()