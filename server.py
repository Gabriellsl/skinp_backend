import os
from flask import Flask, flash, request, url_for, jsonify, send_file
from PIL import Image
from pathlib import Path
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from threading import Thread
import time

basepath = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(basepath, ".", "upload_folder"))

# used to avoid sending unwanted files
ALLOWED_EXTENSIONS = {'jpg', 'png'}

app = Flask(__name__)

def clean_folder(path):
    time.sleep(5)
    os.remove(path)
    print('the image ',path,' as deleted!')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['POST'])
def uploadFile():
    dateTime = str(datetime.now())
    filename = "submited_img", dateTime, '.jpg'
    filename = str(filename).replace(" ", "")
    if 'file' not in request.files:
        content = {
            'Not file found': 'Please send file data with key=file'}
        return jsonify(content), 400

    file = request.files['file']

    if allowed_file(file.filename) == False:
        content = {
            'Extension not allowed': 'You must send file in jpg or png format'}
        return jsonify(content), 400

    # img = Image.open(file)
    # img = np.asarray(img)
    # plt.imshow(img)
    # plt.show()
    file_path = os.path.join(
        path, secure_filename(filename))
    file.save(file_path)

    thread = Thread(target=clean_folder, kwargs={'path': file_path})
    thread.start()

    return send_file(file_path, mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True)
