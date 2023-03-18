# ******************************PYTHON LIBRARIES******************************
from flask import jsonify, request, render_template, render_template_string, json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# ******************************EXTERNAL LIBRARIES****************************
from extensions import db
from src.models.Business import BusinessModel
from src.models.Unit import UnitModel
from src.models.Insurance import InsuranceModel
from schemas import BasicBusinessSchema, BasicUnitSchema, BasicInsuranceSchema
# ******************************OWN LIBRARIES*********************************
blp = Blueprint("forms", __name__, description="All forms funcitionalities")

@blp.route("/home")
class FormsView(MethodView):
    def get(self):
        return render_template("home.html")
    
    def post(self):
        selected_database = request.form["database_type"]
        selected_action = request.form["action_type"]
        
        # In the next code blocks we return all the data stored into an specific database
        # BUSINESS DABATASE - All data
        if selected_database == "business" and selected_action == "all":
            try:
                business = BusinessModel.query.all()
            except:
                abort(500, message="There was a problem in the server side.")
            schema = BasicBusinessSchema(many=True)
            database_response = schema.dump(business)
            return render_template("home.html", database_response=database_response)
        
        # UNIT DABATASE - All data
        elif selected_database == "unit" and selected_action == "all":
            try:
                units = UnitModel.query.all()
            except:
                abort(500, message="There was a problem in the server side.")
            schema = BasicUnitSchema(many=True)
            database_response = schema.dump(units)
            return render_template("home.html", database_response=database_response)
        
        # INSURANCE DABATASE - All data
        elif selected_database == "insurance" and selected_action == "all":
            try:
                insurance = InsuranceModel.query.all()
            except:
                abort(500, message="There was a problem in the server side.")
            schema = BasicInsuranceSchema(many=True)
            database_response = schema.dump(insurance)
            return render_template("home.html", database_response=database_response)
        


        return render_template("home.html", selected_database=selected_database, selected_action=selected_action)
