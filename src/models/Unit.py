# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************
from extensions import db
# ***********************************CODE*************************************
class UnitModel(db.Model):
    __tablename__ = "units"

    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    make = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    id_business = db.Column(db.Integer(), db.ForeignKey("business.id"), nullable=True)
    id_insurance = db.Column(db.Integer(), db.ForeignKey("insurance.id"), nullable=True)

    business = db.relationship("BusinessModel", back_populates="units")
    insurance = db.relationship("InsuranceModel", back_populates="units")
