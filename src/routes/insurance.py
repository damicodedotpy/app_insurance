# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify
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

    @blp.arguments(BasicInsuranceSchema)
    @blp.response(200, BasicInsuranceSchema)
    def post(self, insurance_data):
        '''This endpoint creates and saves
        a new instance of insurance into the
        database, then return the recent
        insurance object created as a JSON.'''
        insurance = InsuranceModel(**insurance_data)
        db.session.add(insurance)
        db.session.commit()
        return insurance

@blp.route("/insurance/<string:insurance_id>")
class InsuranceIDView(MethodView):
    @blp.response(200, CompleteInsuranceSchema)
    def get(self, insurance_id):
        '''This endpoint returns a specific
        insurance information from the database
        according to the ID provided.'''
        insurance = InsuranceModel.query.get_or_404(insurance_id)
        return insurance

    @blp.arguments(UpdateInsuranceSchema)
    @blp.response(200, CompleteInsuranceSchema)
    def put(self, insurance_data, insurance_id):
        '''This endpoint updates a specific
        insurance into the database with the
        information provided and then returns
        it.'''
        insurance = InsuranceModel.query.get_or_404(insurance_id)
        for key, value in insurance_data.items():
            setattr(insurance, key, value)
        db.session.commit()
        return insurance

    def delete(self, insurance_id):
        '''This endpoint deletes a
        specific business from the database
        according to the ID provided.'''
        insurance = InsuranceModel.query.get_or_404(insurance_id)
        db.session.delete(insurance)
        db.session.commit()
        return jsonify({"message": "Insurance deleted successfully."})
