import shutil
import os
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from image_editing import increase_brightness, decrease_brightness, increase_contrast, decrease_contrast, crop, increase_blur
from PIL import Image, ImageEnhance

from flask import Flask, render_template, request, redirect, session, flash, send_file

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

temp_img_address = 'static/img_temp.png'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'


def get_file():
    if session.get('img_name'):
        return UPLOAD_FOLDER + "/" + session.get('img_name')
    else:
        flash("We could not identify your file. Download failed")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def reset_image():
    print('reset the file...')
    flash("Your image has been reset")
    print(UPLOAD_FOLDER + "/" + session.get('img_name'))
    image_original = Image.open(UPLOAD_FOLDER + "/original" + session.get('img_name'))
    image_original.save(get_file())


def get_ratio(image):
    width, height = image.size
    print(f"initial image ratio: {width / height}")
    return width, height


def connect_newspaper(newspaper):
    reset_image()
    image = Image.open(get_file())
    news = Image.open(join(dirname(realpath(__file__)), 'newspapers') + "/" + str(newspaper))
    news_width, news_height = news.size
    width, height = get_ratio(image)

    wpercent = news_width / width
    hpercent = news_height / height
    wsize = int((float(width) * float(hpercent)))
    hsize = int((float(height) * float(wpercent)))
    print(f'image: width {width}, height: {height}')
    print(f'newsp: width {news_width}, height: {news_height}')

    # si la largeur de l'image est plus petite que le journal
    if width < news_width:
        print(f"image n'est pas assez large, resize à {news_width}, {hsize}")
        image = image.resize((news_width, hsize), Image.ANTIALIAS)
        width, height = get_ratio(image)

    if height < news_height:
        print(f"image n'est pas assez haute, resize à {wsize}, {news_height}")
        image = image.resize((wsize, news_height), Image.ANTIALIAS)

        width, height = get_ratio(image)

    if height > news_height:
        print("image est trop haute, cropping!")
        image = image.crop(((width / 2 - news_width / 2), (height / 2 - news_height / 2), (width / 2 + news_width / 2),
                            (height / 2 + news_height / 2)))
        width, height = get_ratio(image)

    if width > news_width:
        print("image est trop large, cropping!")
        image = image.crop(((width / 2 - news_width / 2), (height / 2 - news_height / 2), (width / 2 + news_width / 2),
                            (height / 2 + news_height / 2)))
        width, height = get_ratio(image)

    image.save(get_file())

    image.paste(news, (0, 0), news)
    image.save(get_file())


def download():
    print(f"downloading...{get_file()}")

    return send_file(get_file(), as_attachment=True)


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
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + filename),
                        os.path.join(app.config['UPLOAD_FOLDER'] + "/" + "original" + filename))
            session['img_name'] = filename
            return redirect('/edit')


@app.route('/')
def show():
    return redirect('/upload')


@app.route('/edit', methods=['POST', 'GET'])
def edit_image():
    if request.method == 'POST':
        print(request.form)
        if request.form.get('black'):
            print('to black and white...')
            image = Image.open(get_file())
            image = image.convert('L')

            image.save(get_file())

        elif request.form.get('reset'):
            reset_image()

        elif request.form.get('brightnessplus'):
            increase_brightness(get_file())

        elif request.form.get('blur'):
            increase_blur(get_file())

        elif request.form.get('contrastplus'):
            increase_contrast(get_file())
        elif request.form.get('contrastminus'):
            decrease_contrast(get_file())

        elif request.form.get('brightnessminus'):
            decrease_brightness(get_file())

        elif request.form.get('continue'):
            image = Image.open(get_file())
            image.save(UPLOAD_FOLDER + "/original" + session.get('img_name'))
            return redirect('/resize')

        elif request.form.get('download'):
            return redirect('/download')

        else:
            print("couldn't find which request it was? ")

    return render_template('index.html')


@app.route('/newspaper', methods=['GET', 'POST'])
def add_newspaper():
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        print(request.form)
        if request.form.get('declic-junior'):
            connect_newspaper("declic-junior.png")

        if request.form.get('elle-maigrir'):
            connect_newspaper("elle-maigrir.png")

        if request.form.get('journal-mickey'):
            connect_newspaper("journal-mickey.png")

        if request.form.get('paris-match'):
            connect_newspaper("paris-match.png")

        if request.form.get('top-model'):
            connect_newspaper("top-model.png")
        if request.form.get('public'):
            connect_newspaper("public.png")
        if request.form.get('petit-prince'):
            connect_newspaper("petit-prince.png")


        elif request.form.get('reset'):
            reset_image()

        elif request.form.get('continue'):
            image = Image.open(get_file())
            image.save(UPLOAD_FOLDER + "/original" + session.get('img_name'))
            return redirect('/download')

    return render_template('newspaper.html')


@app.route('/resize', methods=['GET', 'POST'])
def resize_img():

    if request.method == 'POST':
        if request.form.get('up'):
            print('remove upper part')
            crop(get_file(), "up")
            return render_template('resize.html')

        elif request.form.get('right'):
            print('remove right part')
            crop(get_file(), "right")
            return render_template('resize.html')

        elif request.form.get('left'):
            print('remove left part')
            crop(get_file(), "left")
            return render_template('resize.html')
        elif request.form.get('down'):
            print('remove bottom part')
            crop(get_file(), "bottom")
            return render_template('resize.html')

        elif request.form.get('reset'):
            reset_image()
            return render_template('resize.html')

        elif request.form.get('continue'):
            image = Image.open(get_file())
            image.save(UPLOAD_FOLDER + "/original" + session.get('img_name'))
            return redirect('/newspaper')

    return render_template('resize.html')




@app.route('/download', methods=['POST', 'GET'])
def down():
    if request.method == 'POST':
        return download()

    return render_template('download.html')


if __name__ == "__main__":
    app.run()
