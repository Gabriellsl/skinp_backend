import os
from flask import Flask, flash, request, url_for, jsonify, send_file, make_response
from PIL import Image
from pathlib import Path
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from threading import Thread
import time
import base64
from io import BytesIO

basepath = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(basepath, ".", "upload_folder"))

# used to avoid sending unwanted files
ALLOWED_EXTENSIONS = {'jpg', 'png'}

app = Flask(__name__)

def clean_folder(path):
    time.sleep(5)
    os.remove(path)
    print('the image ',path,' has been deleted!')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def decodeImage(base64string):
    dateTime = str(datetime.now())
    filename = "submited_img", dateTime, '.jpg'
    filename = str(filename).replace(" ", "")
    
    byte_data = base64.b64decode(base64string)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)

    file_path = os.path.join(
        path, secure_filename(filename))
    img.save(file_path)

    thread = Thread(target=clean_folder, kwargs={'path': file_path})
    thread.start()

    numpyImage = np.asarray(img)
    return numpyImage

def encodeImage(string):
    pil_img = Image.fromarray((string * 255).astype('uint8'))
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return new_image_string

def predictImage(imageBase64):
    numpyImage = decodeImage(imageBase64)
    numpyPredicted = (numpyImage.astype('float32') / 255)*0.5
    encodedImage = encodeImage(numpyPredicted)
    return encodedImage

@app.route('/postImage/', methods=['post'])
def uploadImage():
    req = request.get_json()
    if 'image' not in req:
        content = {
            'Not file found': 'Please send file data with key=file'}
        return jsonify(content), 400


    image = predictImage(req['image'])
    return jsonify(res=image,accuracy=0.99)


# @app.route('/upload/', methods=['POST'])
# def uploadFile():
#     dateTime = str(datetime.now())
#     filename = "submited_img", dateTime, '.jpg'
#     filename = str(filename).replace(" ", "")
#     if 'file' not in request.files:
#         content = {
#             'Not file found': 'Please send file data with key=file'}
#         return jsonify(content), 400

#     file = request.files['file']

#     if allowed_file(file.filename) == False:
#         content = {
#             'Extension not allowed': 'You must send file in jpg or png format'}
#         return jsonify(content), 400

#     file_path = os.path.join(
#         path, secure_filename(filename))
#     file.save(file_path)

#     thread = Thread(target=clean_folder, kwargs={'path': file_path})
#     thread.start()

#     response = make_response(send_file(file_path, mimetype='image/gif'))
    
#     #response.headers['acc'] = '98,3'
#     #response.headers['loss'] = '0,039'
#     return response

if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0')



