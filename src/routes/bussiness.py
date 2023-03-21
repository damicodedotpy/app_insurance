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
    # @blp.response(200, BasicBusinessSchema(many=True))
    # def get(self):
    #     '''This endpoint return all
    #     the business stored into the
    #     database with their basic
    #     information in a JSON.'''
    #     database_response = BusinessModel.query.all()
    #     return render_template("home.html", database_response=database_response)

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
    
@blp.route("/business/update/")
class BusinessUpdateView(MethodView):
    def post(self):
        '''This endpoint updates a specific
        business into the database with the
        information provided and then returns
        it.
        
        Note: I had to separate this function
        from the /business endpoint because
        I can not have two POST functions into
        the same endpoint. I discovered that 
        HTML forms only accepts GET and POST
        HTTP methods in its forms, and as I had
        a PUT function I didn't worked well, so
        I had to turn it into a POST function,
        which made me to take it out from the 
        /business endpoint due to I already had 
        a POST function on it.
        '''
        try:
            business_id = request.form["id"]
            business = BusinessModel.query.get_or_404(business_id)
        except:
            return jsonify({"message": "The ID has not been specified or is of an invalid type."})
        
        try:
            form_data = {key:value for key, value in request.form.items() if value != "" }
            print(request.form)
            print(type(request.form))
        except:
            return jsonify({"message": "Any information has not been sent."})
        
        schema_arguments = UpdateBusinessSchema()
        business_data = schema_arguments.load(form_data)
        
        try:
            for key, value in business_data.items():
                setattr(business, key, value)
            db.session.commit()
        except:
            return jsonify({"message": "An error has occurred while updating"})
        
        try:
            business_updated = BusinessModel.query.get_or_404(business_id)
            schema_response = CompleteBusinessSchema()
            database_response = schema_response.dump(business_updated)
        except:
            return jsonify({"message": "An error has occurred while serializing the object updated"})
        return render_template("home.html", database_response=database_response)


@blp.route("/business/")
class BusinessIDView(MethodView):
    def get(self):
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
            return jsonify({"message": "El ID enviado no existe o es de tipo incorrecto"})
        schema_business = CompleteBusinessSchema()
        database_response = schema_business.dump(business)
        return render_template("home.html", database_response=database_response)


@blp.route("/business/delete/")
class BusinessDeleteView(MethodView):
    def get(self):
        '''This endpoint deletes a
        specific business from the database
        according to the ID provided.
        
        
        Note: Here happened the same than
        the update function, I had to separate 
        it from the original /business/ endpoint
        for the same reasons.
        '''
        try:
            business_id = request.args.get("business_id")
        except:
            return jsonify({"message": "The ID provided does not exist or is invalid."})
        
        try:
            business = BusinessModel.query.get_or_404(business_id)
        except:
            return jsonify({"message": "Something unexpected has occured while fetching the object."})
        
        try:
            db.session.delete(business)
            db.session.commit()
        except:
            return jsonify({"message": "Something has occurred while trying to delete the object."})
        return render_template("home.html", database_response="Business deleted successfully.")