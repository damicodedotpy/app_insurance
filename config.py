# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************

# ***********************************CODE*************************************
class AppConfiguration(object):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:3132@localhost/app_insurance"
    SQLALCHEMY_TRACK_MODIFICATIONS = False