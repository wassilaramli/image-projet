import unittest
from os.path import join, dirname, realpath
from PIL import Image
import requests
from scripts import call_app

from image_editing import increase_brightness, decrease_brightness, increase_blur



class TestImageEditing(unittest.TestCase):

    test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"

    def test_inc_brightness(self):
        test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"

        success = increase_brightness(test_file_path)
        self.assertEqual(success, True)

    def test_dec_brightness(self):
        test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"
        success = decrease_brightness(test_file_path)
        self.assertEqual(success, True)

    def test_flouter(self):
        test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"
        success = increase_blur(test_file_path)
        self.assertEqual(success, True)

    def test_reset(self):
        print("reset...")
        test_file_path_original = join(dirname(realpath(__file__)), 'static') + "/" + "originaltestpic.png"
        test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"
        Image.open(test_file_path_original).save(test_file_path)

class TestIntegration(unittest.TestCase):
    def test_upload(self):
        test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"
        url = call_app('/upload', file=test_file_path)
        self.assertEqual(url, "http://127.0.0.1:5000/edit")

    def test_edit(self):
        form_data = {"black": True}
        code = call_app('/edit', form_data=form_data)
        self.assertEqual(code, 200)

        form_data = {"contrastplus": True}
        code = call_app('/edit', form_data=form_data)
        self.assertEqual(code, 200)

    def test_resize(self):
        form_data = {"up": True}
        code = call_app('/resize', form_data=form_data)
        self.assertEqual(code, 200)

    def test_couverture(self):
        form_data = {"elle-maigrir": True}
        code = call_app('/newspaper', form_data=form_data)
        self.assertEqual(code, 200)

    def test_download(self):
        form_data = {"test": True}
        code = call_app('/download', form_data=form_data)
        self.assertEqual(code, 200)


if __name__ == '__main__':
    unittest.main()
