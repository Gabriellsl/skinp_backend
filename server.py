from flask import Flask, request
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt

# used to avoid sending unwanted files
ALLOWED_EXTENSIONS = {'jpg','png'}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return('test')

@app.route('/upload/')
def uploadFile():
    file = request.files['file']
    print(type(file));
    img = Image.open(file)
    img = np.asarray(img)
    plt.imshow(img)
    plt.show()
    return 'Successful'

if __name__ == '__main__':
    app.run(debug=True)
