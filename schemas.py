# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from marshmallow import Schema, fields
# ******************************OWN LIBRARIES*********************************

# ***********************************CODE*************************************
class BasicUnitSchema(Schema):
    id = fields.Integer(dump_only=True)
    vin = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Integer()

class BasicBusinessSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    state = fields.String(required=True)
    representative = fields.String()
    tel = fields.String()

class BasicInsuranceSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    rate = fields.String(required=True)

class UpdateUnitSchema(Schema):
    id = fields.Integer(load_only=True)
    vin = fields.String()
    make = fields.String()
    year = fields.Integer()
    id_business = fields.Integer()
    id_insurance = fields.Integer()

class UpdateBusinessSchema(Schema):
    id = fields.Integer(load_only=True)
    name = fields.String()
    state = fields.String()
    representative = fields.String()
    tel = fields.String()

class UpdateInsuranceSchema(Schema):
    id = fields.Integer(load_only=True)
    name = fields.String()
    rate = fields.String()

class CompleteUnitSchema(BasicUnitSchema):
    id_business = fields.Integer(required=True, load_only=True)
    id_insurance = fields.Integer(required=True, load_only=True)
    business = fields.Nested(BasicBusinessSchema(), dump_only=True)
    insurance = fields.Nested(BasicInsuranceSchema(), dump_only=True)

class CompleteBusinessSchema(BasicBusinessSchema):
    units = fields.List(fields.Nested(BasicUnitSchema()), dump_only=True)
    insurance = fields.List(fields.Nested(BasicInsuranceSchema()), dump_only=True)

class CompleteInsuranceSchema(BasicInsuranceSchema):
    units = fields.List(fields.Nested(BasicUnitSchema()), dump_only=True)
    business = fields.List(fields.Nested(BasicBusinessSchema()), dump_only=True)

class BusinessInsuranceSchema(Schema):
    business = fields.Nested(BasicBusinessSchema())
    insurance = fields.Nested(BasicInsuranceSchema())





