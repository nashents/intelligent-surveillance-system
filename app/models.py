import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


#
# class BaseId(db.Model, ABC):
#     id = db.Column(db.Integer, primary_key=True)
#
#
# class BaseName(BaseId):
#     name = db.Column(db.String(60), unique=True)

class Drug(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(255))
    drug_properties = db.relationship('DrugProperty', backref='drug')
    # prescription_items = db.relationship('PrescriptionItem', backref='drug')

    def __repr__(self):
        return '<Drug: {}>'.format(self.name)


class DrugDosage(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(60), unique=False)
    value = db.Column(db.Integer)
    unit_of_count = db.Column(db.String(65))
    unit_of_count_value = db.Column(db.Integer)
    drug_properties = db.relationship('DrugProperty', backref='drug_dosage')


class DrugFormulation(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    volume = db.Column(db.Boolean, default=False)
    drug_properties = db.relationship('DrugProperty', backref='drug_formulation')

#
# class DrugRoute(db.Model):
#     id = db.Column(db.BigInteger, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     drug_properties = db.relationship('DrugProperty', backref='drug_route')


class DrugProperty(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    drug_dosage_id = db.Column(db.BigInteger, db.ForeignKey('drug_dosage.id'))
    route_id = db.Column(db.BigInteger, db.ForeignKey('drug_route.id'))
    formulation_id = db.Column(db.BigInteger, db.ForeignKey('drug_formulation.id'))
    drug_name_id = db.Column(db.BigInteger, db.ForeignKey('drug.id'))


class DrugRoute(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    drug_properties = db.relationship('DrugProperty', backref='drug_route')


# class PrescriptionItem(db.Model):
#     id = db.Column(db.BigInteger, primary_key=True)
#     duration = db.Column(db.Integer, index=True, unique=False)
#     frequency = db.Column(db.Integer, index=True, unique=False)
#     instruction = db.Column(db.String(60))
#     drug__id = db.Column(db.BigInteger, db.ForeignKey('drug.id'))
#     prescription_id = db.Column(db.BigInteger, db.ForeignKey('prescription.id'))
#
#     #   date_generated = db.Column
#
#     def __repr__(self):
#         return '<PrescriptionItem: {} {} >'.format(self.duration, self.frequency, self.instruction)


class Prescription(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'))
    # prescription_items = db.relationship('PrescriptionItem', backref='prescription', lazy='dynamic')
    doctor = db.Column(db.String(60), unique=False)

    @staticmethod
    def get_all():
        return Prescription.query.all()

    def __repr__(self):
        return "<Prescription: {}>".format(self.mobile_number)


class Patient(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(60), index=True, unique=False)
    last_name = db.Column(db.String(60), index=True, unique=False)
    national_id = db.Column(db.String(60), index=True, unique=True)
    prescriptions = db.relationship('Prescription', backref='patient', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(self, patient_id):
        return Patient.query.get(int(patient_id))

    @staticmethod
    def get_all():
        return Patient.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Patient: {}>".format(self.national_id)


class ServerResponse(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    # Set up user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Role(db.Model):
    """
    Create a Role table
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
