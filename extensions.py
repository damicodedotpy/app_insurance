# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# ******************************OWN LIBRARIES*********************************

# ***********************************CODE*************************************
db = SQLAlchemy()
migrate = Migrate()