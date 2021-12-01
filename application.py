import shutil
import os
from image_editing import to_black_white, serve_pil_image
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

from PIL import Image, ImageEnhance

from flask import Flask, render_template, request, redirect, session, flash

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

temp_img_address = 'static/img_temp.png'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'

def get_file():
    return UPLOAD_FOLDER + "/" + session.get('img_name')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/upload')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/upload')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER']+ "/" + filename), os.path.join(app.config['UPLOAD_FOLDER']+ "/"+ "original"+filename))
            session['img_name'] = filename
            return redirect('/edit')




@app.route('/')
def show():
    return redirect('/upload')


@app.route('/edit', methods=['POST', 'GET'])
def edit_image():
    if request.method == 'POST':
        if request.form.get('black') == 'Black and White':
            print('to black and white...')
            image = Image.open(get_file())
            image = to_black_white(image)
            image.save(get_file())

        if request.form.get('reset') == 'Reset':
            print('reset the file...')
            print(UPLOAD_FOLDER + "/" + session.get('img_name'))
            image_original = Image.open(UPLOAD_FOLDER + "/original" + session.get('img_name'))
            image_original.save(get_file())

        if request.form.get('brightnessplus') == 'Increase brightness':
            print('increase brightness...')
            image = Image.open(get_file())
            enhancer = ImageEnhance.Brightness(image)
            im_output = enhancer.enhance(1.5)
            im_output.save(get_file())

        if request.form.get('brightnessminus') == 'Decrease brightness':
            print('decrease brightness...')
            image = Image.open(get_file())
            enhancer = ImageEnhance.Brightness(image)
            im_output = enhancer.enhance(0.5)
            im_output.save(get_file())

    return render_template('index.html')


@app.route('/newspaper')
def add_newspaper():
    image = Image.open(get_file())
    news = Image.open(UPLOAD_FOLDER + "/" + "news.png")
    image.paste(news, (0, 0), news)
    image.save(get_file())

    return render_template('newspaper.html')



#app.run()