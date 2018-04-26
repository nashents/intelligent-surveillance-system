from flask import render_template, redirect, flash, url_for, abort
from flask_login import login_required, current_user
from wtforms import ValidationError
import requests
import json

from . import home
from .forms import RegistrationForm
from ..models import Patient
from app import db


@home.route('/')
def index():
    return redirect('/login')


@home.route('/patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = RegistrationForm()
    if form.validate_on_submit():

        patient = Patient(first_name=form.first_name.data, last_name=form.last_name.data,
                          national_id=form.national_id.data)
        patient.save()
        return redirect('/patients')

    else:
        return render_template('home/patient/patient.html', form=form, title='Add Customer')


@home.route('/patients', methods=['GET', 'POST'])
@login_required
def list_patients():
    patients = Patient.get_all()
    return render_template('home/patient/patients.html', patients=patients, title='Patients')


@home.route('/patient/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    """
    Edit a patient
    """

    add_patient = False

    patient = Patient.query.get_or_404(id)
    form = RegistrationForm(obj=patient)
    if form.validate_on_submit():
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.national_id = form.national_id.data
        db.session.commit()
        flash('You have successfully edited the patient.')

        # redirect to the customers page
        return redirect(url_for('home.list_patients'))

    form.first_name.data = patient.first_name
    form.last_name.data = patient.last_name
    form.national_id.data = patient.national_id
    return render_template('home/patient/patient.html', action="Edit",
                           add_patient=add_patient, form=form,
                           patient=patient, title="Edit Patient")


@home.route('/customers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
    """
    Delete a patient from the database
    """

    patient = Patient.query.get_or_404(id)
    patient.delete()
    flash('You have successfully deleted the patient.')

    # redirect to the patient page
    return redirect(url_for('home.list_patient'))


@home.route('/patient/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view_patient(id):
    """
    View a patient profile
    """
    patient = Patient.query.get(int(id))
    # customer_accounts = Account.query.filter_by(customer_id=id).all()

    # account = Account.query.filter_by(customer_id=id).first()
    # account_transactions = Transaction.query.filter_by(account_number=account.mobile_number).all()
    # print("######################### Customer Accounts", customer_accounts)

    return render_template('home/patient/patient_profile.html', patient=patient, title='Patient Profile',
                            )


# @home.route('/patient/edit_account/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_account(id):
#     """
#     Edit a patient account
#     """
#     if current_user.role_id == 1:
#         account = Account.query.get_or_404(id)
#         form = CustomerAccountForm(obj=account)
#
#         if form.validate_on_submit():
#             account.max_value_for_transaction = form.max_value_for_transaction.data
#             db.session.commit()
#             flash('You have successfully edited the account.')
#             return redirect(url_for('home.list_customers'))
#
#         form.max_value_for_transaction.data = account.max_value_for_transaction
#         form.mobile_number.data = account.mobile_number
#         # form.balance.data = account.balance
#
#         return render_template('home/account/edit_account.html', action="Edit",
#                                form=form, account=account, title="Edit Account")
#     else:
#         abort(403)


@home.route('/patient/add_prescription', methods=['GET', 'POST'])
@login_required
def create_prescription():
    form = RegistrationForm()
    if form.validate_on_submit():

        patient = Patient(first_name=form.first_name.data, last_name=form.last_name.data,
                          national_id=form.national_id.data)
        patient.save()
        return redirect('/patients')

    else:
        return render_template('home/prescription/add.html', form=form, title='Create Prescription')
