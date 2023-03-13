# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Business import BusinessModel
from schemas import BasicBusinessSchema
# ***********************************CODE*************************************
blp = Blueprint("business", __name__, description="All busimess funcitonalities")

@blp.route("/business")
class BusinessView(MethodView):
    @blp.response(200, BasicBusinessSchema(many=True))
    def get(self):
        '''This endpoint return all
        the business stored into the
        database with their basic
        information in a JSON.'''
        business = BusinessModel.query.all()
        return business


    @blp.arguments(BasicBusinessSchema)
    @blp.response(200, BasicBusinessSchema)
    def post(self, business_data):
        '''This endpoint creates and saves
        a new instance of business into the
        database, then return the recent
        business created as a JSON object.'''
        business = BusinessModel(**business_data)
        try:
            db.session.add(business)
            db.session.commit()
        except:
            abort(500, message="Something has occured while adding the new business into de database.")
        return business