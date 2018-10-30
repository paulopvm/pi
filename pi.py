# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import datetime as dt


# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

file = open("controle.txt","a")
# Load a sample picture and learn how to recognize it.
print("Carregando rosto(s) conhecidos")
paulo_image = face_recognition.load_image_file("paulo.jpg")
paulo_face_encoding = face_recognition.face_encodings(paulo_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    print("Capturando imagem.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Encontrados {} rostos na imagem.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([paulo_face_encoding], face_encoding)
        name = "<Pessoa nao autorizada>"

        if match[0]:
            name = "Paulo Oliveira"

        print("Olá {}!".format(name))
        file.write(format(name) + " autorizado as " + str(dt.datetime.now()) + "\n")
