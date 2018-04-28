from sendalerts import send_an_email, send_an_sms
import face_recognition
import P3picam
import picamera
from datetime import datetime
from subprocess import call
from time import sleep, time



motionState = False
picPath = "/home/pi/Desktop/iss/images/unknown_people/"
last_epoch = 0
email_update_interval = 600

def captureImage(currentTime, picPath):
    # Generate the picture's name
    picName = currentTime.strftime("%Y.%m.%d-%H.%M.%S") + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picPath + picName)
     
    print("We have taken a picture.")
    return picName

def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime

def timeStamp(currentTime, picPath, picName):
    # Variable for file path
    filepath = picPath + picName
    # Create message to stamp on picture
    message = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    # Create command to execute
    timestampCommand = "/usr/bin/convert " + filepath + " -pointsize 36 \
    -fill red -annotate +700+650 '" + message + "' " + filepath
    # Execute the command
    call([timestampCommand], shell=True)
    print("We have timestamped our picture.")
    
def main():
    known_image = face_recognition.load_image_file("/home/pi/Desktop/iss/images/known_people/2018.04.20-112118.jpg")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    face_locations = []
    unknown_face_encodings = []
    while True:
        motionState = P3picam.motion()
        print(motionState)
        if motionState:
            currentTime = getTime()
            picName = captureImage(currentTime, picPath)
            timeStamp(currentTime, picPath, picName)
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
                    
                    try:
                        if(time.time() - last_epoch) > email_update_interval:
                            last_epoch = time.time()
                            print ("Sending email and Sms...")
                            send_an_email(unknown_image)
                            send_an_sms()
                            print ("done!")
                    
                    except:
                        print ("Error sending email: ")
                        
                    
		                  
                   
           
       
        
while True:
    main()
   
  
        

 
        
