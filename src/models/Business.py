# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************
from extensions import db
# ***********************************CODE*************************************
class BusinessModel(db.Model):
    __tablename__ = "business"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=False)
    representative = db.Column(db.String, nullable=True)
    tel = db.Column(db.String, nullable=True)

    units = db.relationship("UnitModel", back_populates="business")
    insurance = db.relationship("InsuranceModel", back_populates="business", secondary="business_insurance")

