# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask_smorest import Blueprint, abort
from flask.views import MethodView
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Insurance import InsuranceModel
from schemas import BasicInsuranceSchema
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
