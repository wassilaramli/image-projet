
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


def crop(image_path, where):
    change = 40
    image = Image.open(image_path)
    width, height = image.size
    left = 0
    top = 0
    right = width
    bottom = height
    if where == 'up':
        top = top + change
    elif where == 'bottom':
        bottom = bottom - change
    elif where == 'right':
        right = right - change
    elif where == 'left':
        left = left + change

    image = image.crop((left, top, right, bottom))
    image.save(image_path)



