# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Unit import UnitModel
from schemas import BasicUnitSchema, CompleteUnitSchema, UpdateUnitSchema
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


@blp.route("/units/<string:unit_id>")
class UnitsIDView(MethodView):
    @blp.response(200, CompleteUnitSchema)
    def get(self, unit_id):
        '''This endpoint returns a
        specific unit's information from
        the database according to the
        ID provided.'''
        unit = UnitModel.query.get_or_404(unit_id)
        return unit

    @blp.arguments(UpdateUnitSchema)
    @blp.response(200, CompleteUnitSchema)
    def put(self, unit_data, unit_id):
        '''This endpoint extracts a
        specific unit from the database
        and updates its information
        according to the new data sent.'''
        unit = UnitModel.query.get_or_404(unit_id)
        for key, value in unit_data.items():
            setattr(unit, key, value)
        db.session.commit()
        return unit

    def delete(self, unit_id):
        '''This endpoint deletes a
        specific unit from the database
        according to the ID provided.'''
        unit = UnitModel.query.get_or_404(unit_id)
        db.session.delete(unit)
        db.session.commit()
        return jsonify({"message": "Unit deleted successfully."})

