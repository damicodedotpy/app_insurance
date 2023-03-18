# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import jsonify, render_template, request, json
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import ValidationError
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Business import BusinessModel
from schemas import BasicBusinessSchema, CompleteBusinessSchema, UpdateBusinessSchema
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
        database_response = BusinessModel.query.all()
        return render_template("home.html", database_response=database_response)

    def post(self):
        '''This endpoint creates and saves
        a new instance of business into the
        database, then return the recent
        business created as a JSON object.'''
        try:
            form_data = request.form
        except:
            return jsonify({"message": "Something goes wrong trying to load the information in the form"})
        try:
            schema_arguments = BasicBusinessSchema()
            business_data = schema_arguments.load(form_data)
        except ValidationError:
            abort(400, message="The info provided is not as required.")
        business = BusinessModel(**business_data)
        try:
            db.session.add(business)
            db.session.commit()
        except:
            abort(500, message="Something has occured while adding the new business into de database.")
        schema = BasicBusinessSchema()
        database_response = schema.dump(business)
        return render_template("home.html", database_response=database_response)


@blp.route("/business/<string:business_id>")
class BusinessIDView(MethodView):
    def get(self, business_id):
        '''This endpoint returns a specific
        business information from the database
        according to the ID provided.'''
        try:
            business_id = request.args.get("business_id")
        except:
            return jsonify({"message": "Nos atoramos en la recepcion del id"})
        
        try: 
            business = BusinessModel.query.get_or_404(business_id)
        except:
            return jsonify({"message": "Nos atoramos en buscar el business correspondiente segun el id"})
        schema_business = CompleteBusinessSchema()
        database_response = schema_business.dump(business)
        return render_template("home.html", database_response=database_response)

    @blp.arguments(UpdateBusinessSchema)
    @blp.response(200, CompleteBusinessSchema)
    def put(self, business_data, business_id):
        '''This endpoint updates a specific
        business into the database with the
        information provided and then returns
        it.'''
        business = BusinessModel.query.get_or_404(business_id)
        for key, value in business_data.items():
            setattr(business, key, value)
        db.session.commit()
        return business

    def delete(self, business_id):
        '''This endpoint deletes a
        specific business from the database
        according to the ID provided.'''
        business = BusinessModel.query.get_or_404(business_id)
        db.session.delete(business)
        db.session.commit()
        return jsonify({"message": "Business deleted successfully."})