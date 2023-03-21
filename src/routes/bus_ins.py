# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify, request, render_template
from flask.views import MethodView
from flask_smorest import Blueprint
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Business import BusinessModel
from src.models.Insurance import InsuranceModel
from src.models.Bus_Ins import Business_InsuranceModel
from schemas import BusinessInsuranceSchema, CompleteInsuranceSchema
# ***********************************CODE*************************************
blp = Blueprint("business_insurance", __name__, description="All business/insurance functionalities")

@blp.route("/bus_ins/add/")
class BusinessInsuranceLinkView(MethodView):
    def get(self):
        '''This endpoint receives a business ID
        as well as an insurance ID and then
        creates a link between them in a
        many to many relationship.'''
        try:
            business_id = request.args.get("business_id")
            insurance_id = request.args.get("insurance_id")
        except:
            return jsonify(({"message": "Something has occurred while trying to get the ID's."}))
        
        try:
            for key, value in request.args.items():
                if value == "":
                    return jsonify({"message": f"The {key} ID was empty."})
        except:
            return jsonify({"message": "Something has occurred while validating the IDs."})
        
        try:
            business = BusinessModel.query.get_or_404(business_id)
            insurance = InsuranceModel.query.get_or_404(insurance_id)
        except:
            return jsonify({"message": "Something has occurred while searching the objects into the database."})
        
        try:
            business.insurance.append(insurance)
            db.session.add(business)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while linking the objects into the database."})
        return render_template("home.html", database_response="The business and the insurance has been linked successfully!")

@blp.route("/bus_ins/delete/")
class BusinessInsuranceUnlinkView(MethodView):
    def get(self):
        '''This endpoint unlink a business from
        an insurance according to de respective
        IDs provided.'''
        try:
            business_id = request.args.get("business_id")
            insurance_id = request.args.get("insurance_id")
        except:
            return jsonify(({"message": "Something has occurred while trying to get the ID's."}))
        
        try:
            for key, value in request.args.items():
                if value == "":
                    return jsonify({"message": f"The {key} ID was empty."})
        except:
            return jsonify({"message": "Something has occurred while validating the IDs."})
        
        try:
            business = BusinessModel.query.get_or_404(business_id)
            insurance = InsuranceModel.query.get_or_404(insurance_id)
        except:
            return jsonify({"message": "Something has occurred while searching the objects into the database."})
        
        try:
            business.insurance.remove(insurance)
            db.session.add(business)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while trying to unlink the objects from the database."})
        return render_template("home.html", database_response="Business and Insurance unlinked successfully!")



