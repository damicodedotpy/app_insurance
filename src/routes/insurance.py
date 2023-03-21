# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify, request, render_template
from flask_smorest import Blueprint, abort
from flask.views import MethodView
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Insurance import InsuranceModel
from schemas import BasicInsuranceSchema, CompleteInsuranceSchema, UpdateInsuranceSchema
# ***********************************CODE*************************************
blp = Blueprint("insurance", __name__, description="All the insurance funtionalities")

@blp.route("/insurance")
class InsuranceView(MethodView):
    @blp.response(200, BasicInsuranceSchema(many=True))
    def get(self):
        '''This endpoint return all
        the insurances stored into the
        database with their basic
        information in a JSON.'''
        insurance = InsuranceModel.query.all()
        return insurance


    def post(self):
        '''This endpoint creates and saves
        a new instance of insurance into the
        database, then return the recent
        insurance object created as a JSON.'''
        try:
            form_data = request.form
        except:
            return jsonify({"message": "Something has occurred while getting de form's data."})
        
        try:
            schema_insurance = BasicInsuranceSchema()
            insurance_data = schema_insurance.load(form_data)
        except:
            return jsonify({"message": "Something has occurred while validating the data through the schema."})
        
        try:    
            insurance = InsuranceModel(**insurance_data)
            db.session.add(insurance)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while creating the new insurance instance and saving it"})
        return render_template("home.html", database_response="Insurance added successfully!")

@blp.route("/insurance/")
class InsuranceIDView(MethodView):
    def get(self):
        '''This endpoint returns a specific
        insurance information from the database
        according to the ID provided.'''
        try:
            insurance_id = request.args.get("insurance_id")
        except:
            return jsonify({"message": "The ID has been omitted or is an invalid type."})
        
        try:
            insurance = InsuranceModel.query.get_or_404(insurance_id)
        except:
            return jsonify({"message": "Something has occurred while searching the insurance by ID."})
        
        try:
            schema_insurance = CompleteInsuranceSchema()
            database_response = schema_insurance.dump(insurance)
        except:
            return jsonify({"message": "Something has occured while serializing the insurance information."})
        return render_template("home.html", database_response=database_response)

@blp.route("/insurance/update/")
class InsuranceUpdateView(MethodView):
    def post(self):
        '''This endpoint updates a specific
        insurance into the database with the
        information provided and then returns
        it.'''
        try:
            insurance_id = request.form["id"]
            insurance = InsuranceModel.query.get_or_404(insurance_id)
        except:
            return jsonify({"message": "Something has occurred while getting the insurance per ID."})
        
        try:
            form_data = {key: value for key, value in request.form.items() if value != ""}
        except:
            return jsonify({"message": "Something has occurred while getting the form's data and removing the empty keys."})
        
        try:
            schema_insurance = UpdateInsuranceSchema()
            insurance_data = schema_insurance.load(form_data)
        except:
            return jsonify({"message": "Something has occurred while deserializing the insurance's data."})
        
        try:
            for key, value in insurance_data.items():
                setattr(insurance, key, value)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while  updating and committing the updated insurance."})
        return render_template("home.html", database_response="Insurance updated successfully!")
        


@blp.route("/insurance/delete/")
class InsuranceDeleteView(MethodView):
    def get(self):
        '''This endpoint deletes a
        specific business from the database
        according to the ID provided.'''
        try:
            insurance_id = request.args.get("id")
        except:
            return jsonify({"message": "Something has occurred while gettin the insurance ID."})
        
        try:
            insurance = InsuranceModel.query.get_or_404(insurance_id)
        except:
            return jsonify({"message": "Something has ocurred while searching the insurance in the database."})
        
        try:
            db.session.delete(insurance)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while trying to delete the insurance from the database."})
        return render_template("home.html", database_response="Insurance deleted successfully!")
        
