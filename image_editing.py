import PIL
from flask import send_file

from io import BytesIO
from PIL import Image




def to_black_white(image):
    image = image.convert('L')
    return image

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')