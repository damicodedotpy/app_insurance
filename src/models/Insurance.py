# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************
from extensions import db
# ***********************************CODE*************************************
class InsuranceModel(db.Model):
    __tablename__ = "insurance"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    rate = db.Column(db.String, nullable=False)

    units = db.relationship("UnitModel", back_populates="insurance")
    business = db.relationship("BusinessModel", back_populates="insurance", secondary="business_insurance")