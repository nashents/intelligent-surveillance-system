from flask import render_template, redirect, flash, url_for, Response, stream_with_context
import io
from datetime import datetime
from subprocess import call
from time import sleep, time
from .sendalerts import send_an_email, send_an_sms
import face_recognition
from .P3picam import motion
import picamera

from . import home, photos
from .forms import BayOwnerForm
from ..models import BayOwner, Bay
from app import app

from .camera_pi import Camera

motionState = False
picPath = "/home/pi/Desktop/iss/images/unknown_people/"
last_epoch = 0
email_update_interval = 600


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

        bay_owner = bay_owner.get(id=id)

        file_path = photos.path(file_name, app.config['UPLOADED_PHOTOS_DEST'])

        print('+++++++++++++++++++++++++++ Uploaded image path: ', file_path)

        return redirect(url_for('home.dashboard'))

    return render_template('home/bay_owner/add.html', form=form, title='Add Bay Owner')


# -------------------------- face recognition methods -------------------------------- #


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""

    bay_owner = BayOwner.query.get(int(2))
    file_name = bay_owner.uploaded_image_name
    file_path = photos.path(file_name, app.config['UPLOADED_PHOTOS_DEST'])

    @stream_with_context
    def gen(camera):
        """Video streaming generator function."""

        while True:
            frame = camera.get_frame()

            print("++++++++++++++++++++++++++ Bay Owner file path", file_path)
            known_image = face_recognition.load_image_file(file_path)

            known_face_encoding = face_recognition.face_encodings(known_image)[0]
            face_locations = []
            unknown_face_encodings = []
            currentTime = datetime.now()
            # picName = capture_image(currentTime, picPath)

            # Generate the picture's name
            picName = currentTime.strftime("%Y.%m.%d-%H.%M.%S") + '.jpg'
            with picamera.PiCamera() as camera:
                camera.resolution = (1280, 720)
                camera.capture(picPath + picName)

            print("We have taken a picture.")

            # Time stamp
            filepath = picPath + picName
            # Create message to stamp on picture
            message = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
            # Create command to execute
            timestampCommand = "/usr/bin/convert " + filepath + " -pointsize 36 \
                       -fill red -annotate +700+650 '" + message + "' " + filepath
            # Execute the command
            call([timestampCommand], shell=True)
            print("We have timestamped our picture.")

            filepath = picPath + picName

            unknown_image = face_recognition.load_image_file(filepath)
            face_locations = face_recognition.face_locations(unknown_image)
            print("Found {} faces in image.".format(len(face_locations)))
            unknown_face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            for unknown_face_encoding in unknown_face_encodings:
                results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
                name = "<Unknown Person>"

                if results[0] == True:
                    name = "Panashe Ngorima"
                    print("I see someone named {}!".format(name))
                else:
                    print("Alert!! THERE IS AN UNRECOGNIZED FACE IN THE PARKING BAY")
                    # save unknown face
                    try:
                        if (time.time() - last_epoch) > email_update_interval:
                            last_epoch = time.time()
                            print("Sending email and Sms...")
                            send_an_email(unknown_image)
                            send_an_sms()
                            print("done!")

                    except:
                        print("Error sending email: ")

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def uploaded_image():
    file_name = ''
    file_path = photos.path(file_name, app.config['UPLOADED_PHOTOS_DEST'])
    return file_path


@home.route('/video_feed', methods=['GET', 'POST'])
# @login_required
def video_feed():
    print("+++++++++++++++++++++++++++++++ In here")
    return render_template('home/video_feed.html', title='Video Feed')


@home.route('/detected_faces', methods=['GET', 'POST'])
# @login_required
def detected_faces():
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/exit_feed', methods=['GET', 'POST'])
# @login_required
def exit_feed():
    return redirect(url_for('home.dashboard'))

#
# def main():
#     bay_owner = BayOwner.get_all()
#     file_name = bay_owner.uploaded_image_name
#     file_path = photos.path(file_name, app.config['UPLOADED_PHOTOS_DEST'])
#     known_image = face_recognition.load_image_file(file_path)
#
#     known_face_encoding = face_recognition.face_encodings(known_image)[0]
#     face_locations = []
#     unknown_face_encodings = []
#
#     motionState = motion()
#     print(motionState)
#     if motionState:
#         currentTime = get_time()
#         picName = capture_image(currentTime, picPath)
#         time_stamp(currentTime, picPath, picName)
#         filepath = picPath + picName
#
#         unknown_image = face_recognition.load_image_file(filepath)
#         face_locations = face_recognition.face_locations(unknown_image)
#         print("Found {} faces in image.".format(len(face_locations)))
#         unknown_face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
#
#         for unknown_face_encoding in unknown_face_encodings:
#             results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
#             name = "<Unknown Person>"
#
#             if results[0] == True:
#                 name = "Panashe Ngorima"
#                 print("I see someone named {}!".format(name))
#             else:
#                 print("Alert!! THERE IS AN UNRECOGNIZED FACE IN THE PARKING BAY")
#                 # save unknown face
#                 try:
#                     if (time.time() - last_epoch) > email_update_interval:
#                         last_epoch = time.time()
#                         print("Sending email and Sms...")
#                         send_an_email(unknown_image)
#                         send_an_sms()
#                         print("done!")
#
#                 except:
#                     print("Error sending email: ")
#
#
# while True:
#     main()
