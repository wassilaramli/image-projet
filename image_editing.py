import PIL
from flask import send_file

from io import BytesIO
from PIL import Image, ImageEnhance

def decrease_brightness(image_path):
    print('decrease brightness...')
    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    im_output = enhancer.enhance(0.5)
    im_output.save(image_path)
    return True

def increase_brightness(image_path):
    print('increase brightness...')
    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    im_output = enhancer.enhance(1.5)
    im_output.save(image_path)
    return True

def decrease_contrast(image_path):
    print('decrease brightness...')
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    im_output = enhancer.enhance(0.5)
    im_output.save(image_path)
    return True

def increase_contrast(image_path):
    print('increase contract...')
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    im_output = enhancer.enhance(1.5)
    im_output.save(image_path)
    return True

