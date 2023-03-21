# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify, request, render_template
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

    def post(self):
        '''This endpoint creates and saves
        a new instance of unit into the
        database, then return the recent
        unit created as a JSON object.'''
        try:
            form_data = request.form
        except:
            return jsonify({"message": "Something has occurred while getting the form's data"})
        
        try:
            schema_unit = CompleteUnitSchema()
            unit_data = schema_unit.load(form_data)
        except:
            return jsonify({"message": "Something has occurred while validatin the data through the schema."})
        
        try:
            unit = UnitModel(**unit_data)
            db.session.add(unit)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while creating the unit object and storing it."})
        return render_template("home.html", database_response="Unit created successfully!")


@blp.route("/units/")
class UnitsIDView(MethodView):
    def get(self):
        '''This endpoint returns a
        specific unit's information from
        the database according to the
        ID provided.'''
        try:
            unit_id = request.args.get("unit_id")
        except:
            return jsonify({"message": "Something has occurred while catching the ID."})
        
        try:
            unit = UnitModel.query.get_or_404(unit_id)
        except:
            return jsonify({"message": "Something has ocurred while trying to find the unit or probably does not exist."})
        
        try:
            schema_unit = CompleteUnitSchema()
            database_response = schema_unit.dump(unit)
        except:
            return jsonify({"message": "Something has occurred while serializing the response."})
        return render_template("home.html", database_response=database_response)


@blp.route("/units/update/")
class UnitUpdateView(MethodView):
    def post(self):
        '''This endpoint extracts a
        specific unit from the database
        and updates its information
        according to the new data sent.'''
        try:
            unit_id = request.form["id"]
            unit = UnitModel.query.get_or_404(unit_id)
        except:
            return jsonify({"message": "Something has occurred while trying to find the unit."})
        
        try:
            form_data = {key: value for key, value in request.form.items() if value != ""}
        except:
            return jsonify({"message": "Something has occurred while trying to remove the empty keys from the form."})
        
        try:
            schema_unit = UpdateUnitSchema()
            unit_data = schema_unit.load(form_data)
        except:
            return jsonify({"message": "Something has occurred while deserializing the unit info."})
        
        try:
            for key, value in unit_data.items():
                setattr(unit, key, value)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while updating the unit's info into the database."})
        return render_template("home.html", database_response="The unit has been updated successfully.")


@blp.route("/units/delete/")
class UnitDeleteView(MethodView):
    def get(self):
        '''This endpoint deletes a
        specific unit from the database
        according to the ID provided.'''
        try:
            unit_id = request.args.get("unit_id")
        except:
            return jsonify({"message": "Something has occurred while trying to catch the ID."})
        
        try:
            unit = UnitModel.query.get_or_404(unit_id)
        except:
            return jsonify({"message": "Something has occurred while trying to find the unit."})
        
        try:
            db.session.delete(unit)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while trying to delete the unit."})
        return render_template("home.html", database_response="Unit deleted successfully.")

