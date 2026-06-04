from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    dob = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(100), nullable=False)

    glucose = db.Column(db.Float, nullable=False)

    haemoglobin = db.Column(db.Float, nullable=False)

    cholesterol = db.Column(db.Float, nullable=False)

    remarks = db.Column(db.String(255))

    def __repr__(self):
        return f"<Patient {self.full_name}>"