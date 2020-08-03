from flask import Flask, request
import face_recognition
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

@app.route('/test')
def hello_world():
        return 'Hello, Get'



# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


## load images dictionary
loaded_imgs = {}


## read images from folder
def read_images():
    arr = listdir('./known/')
    
    for i in arr:
        loaded_imgs[i.split('.')] = face_recognition.load_image_file(i)
    

read_images()


## Create and save encodings of known faces
known_faces = []


def create_enc():
    try:
        for i in loaded_imgs:
            known_faces.append(face_recognition.face_encodings(loaded_imgs[i])[0])
    except IndexError:
        print('Index error occurred')
        quit()

## Loading enc in known_faces
create_enc()


def detect_faces_in_image(file):
    unknown_face = face_recognition.load_image_file(file)
    unknown_face = face_recognition.face_encodings(unknown_face)[0]
    result = face_recognition.compare_faces(known_faces, unknown_face)
    if not True in result:
        return false
    else:
        return true

@app.route('/predict', methods=['POST'])
def predict():
    
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            return "File not found"

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
