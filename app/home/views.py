from flask import render_template, redirect, flash, url_for, abort
from flask_login import login_required, current_user
from wtforms import ValidationError
import requests
import json

from . import home, photos
from .forms import BayOwnerForm
from ..models import BayOwner
from app import db


@home.route('/')
def dashboard():
    render_template('home/dashboard.html', title='Dashboard')


@home.route('/add_bay_owner', methods=['GET', 'POST'])
@login_required
def add_bay_owner():
    form = BayOwnerForm
    if form.validate_on_submit():
        file_name = photos.save(form.photo.data)
        file_url = photos.url(file_name)

        bay_owner = BayOwner(first_name=form.first_name.data, last_name=form.last_name.data,
                             national_id=form.national_id.data, upload_image_name=file_name)
        bay_owner.save()
        flash('Bay owner successfully created!')
        return redirect(url_for('home.dashboard'))

    return render_template('home/dashboard.html', form=form, title='Dashboard')
