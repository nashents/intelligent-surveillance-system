from flask import Blueprint
from flask_uploads import UploadSet, configure_uploads, IMAGES
from app import app

home = Blueprint('home', __name__)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from . import views
