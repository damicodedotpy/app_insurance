# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Business import BusinessModel
from src.models.Insurance import InsuranceModel
from src.models.Bus_Ins import Business_InsuranceModel
from src.models.Bus_Ins import Business_InsuranceModel
from schemas import BusinessInsuranceSchema, CompleteInsuranceSchema
# ***********************************CODE*************************************
blp = Blueprint("business_insurance", __name__, description="All business/insurance functionalities")

@blp.route("/bus_ins/<string:business_id>/<string:insurance_id>")
class BusinessInsuranceView(MethodView):

    @blp.response(200, CompleteInsuranceSchema)
    def post(self, business_id, insurance_id):
        '''This endpoint receives a business ID
        as well as an insurance ID and then
        creates a link between them in a
        many to many relationship.'''
        business = BusinessModel.query.get_or_404(business_id)
        insurance = InsuranceModel.query.get_or_404(insurance_id)
        business.insurance.append(insurance)
        db.session.add(business)
        db.session.commit()
        return insurance

    def delete(self, business_id, insurance_id):
        '''This endpoint unlink a business from
        an insurance according to de respective
        IDs provided.'''
        business = BusinessModel.query.get_or_404(business_id)
        insurance = InsuranceModel.query.get_or_404(insurance_id)
        business.insurance.remove(insurance)
        db.session.add(business)
        db.session.commit()
        return jsonify({"message": "Business and Insurance unlinked successfully."})



