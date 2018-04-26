from flask import render_template, redirect, flash, url_for, abort, send_from_directory
from flask_login import login_required, current_user
from wtforms import ValidationError
import requests
import json

from . import home, photos
from .forms import BayOwnerForm
from ..models import BayOwner, Bay
from app import app


@home.route('/')
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/add_bay_owner', methods=['GET', 'POST'])
# @login_required
def add_bay_owner():
    form = BayOwnerForm()
    if form.validate_on_submit():
        file_name = photos.save(form.photo.data)
        file_url = photos.url(file_name)

        bay_owner = BayOwner(first_name=form.first_name.data, last_name=form.last_name.data,
                             national_id=form.national_id.data, uploaded_image_name=file_name)
        bay_owner.save()
        flash('Bay owner successfully created!')
        file_path = photos.path(file_name, app.config['UPLOADED_PHOTOS_DEST'])

        print('+++++++++++++++++++++++++++ Uploaded image path: ', file_path)

        return redirect(url_for('home.dashboard'))

    return render_template('home/bay_owner/add.html', form=form, title='Add Bay Owner')


def uploaded_image():
    file_name = ''
    file_path = photos.path(file_name, app.config['UPLOADED_PHOTOS_DEST'])
    return file_path


@home.route('/video_feed', methods=['GET', 'POST'])
# @login_required
def video_feed():
    print("+++++++++++++++++++++++++++++++ In here")
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/detected_faces', methods=['GET', 'POST'])
# @login_required
def detected_faces():
    return render_template('home/dashboard.html', title='Dashboard')