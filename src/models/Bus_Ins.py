# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************
from extensions import db
# ***********************************CODE*************************************
class Business_InsuranceModel(db.Model):
    __tablename__ = "business_insurance"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    id_business = db.Column(db.Integer, db.ForeignKey("business.id"))
    id_insurance = db.Column(db.Integer, db.ForeignKey("insurance.id"))