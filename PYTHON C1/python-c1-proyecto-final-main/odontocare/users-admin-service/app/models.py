from datetime import datetime
from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="admin")

    def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role}

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    dni = db.Column(db.String(20), unique=True, nullable=False)  # o documento
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dni": self.dni,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat() + "Z",
        }

class Clinic(db.Model):
    __tablename__ = "clinics"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(30), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() + "Z",
        }


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    license_number = db.Column(db.String(50), unique=True, nullable=False)  # matrícula
    specialty = db.Column(db.String(80), nullable=True)

    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.id"), nullable=False)
    clinic = db.relationship("Clinic", backref=db.backref("doctors", lazy=True))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "license_number": self.license_number,
            "specialty": self.specialty,
            "clinic_id": self.clinic_id,
            "created_at": self.created_at.isoformat() + "Z",
        }