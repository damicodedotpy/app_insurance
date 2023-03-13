# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask_smorest import Blueprint, abort
from flask.views import MethodView
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Unit import UnitModel
from schemas import BasicUnitSchema, CompleteUnitSchema
# ***********************************CODE*************************************
blp = Blueprint("units", __name__, description="All units functionalities")

@blp.route("/units")
class UnitsView(MethodView):
    @blp.response(200, CompleteUnitSchema(many=True))
    def get(self):
        '''This endpoint return all
        the units stored into the
        database with their basic
        information in a JSON.'''
        try:
            units = UnitModel.query.all()
        except:
            abort(500, message="There was a problem in the server side.")
        return units

    @blp.arguments(CompleteUnitSchema)
    @blp.response(200, CompleteUnitSchema)
    def post(self, unit_data):
        '''This endpoint creates and saves
       a new instance of unit into the
       database, then return the recent
       unit created as a JSON object.'''
        unit = UnitModel(**unit_data)
        db.session.add(unit)
        db.session.commit()
        return unit
