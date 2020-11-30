# flask app

import os
#from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
#
from PIL import Image, ImageFilter
#Import all the enhancement filter from pillow
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

uploadFolder = "/home/henrryagc/Escritorio/pyImgProc/app/static/uploads/"
app.config['IMAGE_UPLOADS'] = uploadFolder

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


filtros = [BLUR, EDGE_ENHANCE, SMOOTH]

@app.route('/')
@app.route('/index')
def index():
    """Hola Mundo
    mundo
    """
    name = 'Henrry'
    return render_template('index.html', title='Henrry\'s App')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
        img = Image.open('/home/henrryagc/Escritorio/pyImgProc/app/static/uploads/' + filename)
        img_names = []
        for filtro in filtros:
            imgFilt = img.filter(filtro)
            print(filtro.name + filename)
            imgFilt.save(os.path.join(app.config['IMAGE_UPLOADS'], filtro.name + filename))
            img_names.append(filtro.name + filename)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        return render_template('index.html', filename=filename, img_names=img_names)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)
