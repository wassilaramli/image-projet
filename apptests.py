import unittest
from os.path import join, dirname, realpath
from PIL import Image

from image_editing import increase_brightness, decrease_brightness


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

    def test_reset(self):
        print("reset...")
        test_file_path_original = join(dirname(realpath(__file__)), 'static') + "/" + "originaltestpic.png"
        test_file_path = join(dirname(realpath(__file__)), 'static') + "/" + "testpic.png"
        Image.open(test_file_path_original).save(test_file_path)


if __name__ == '__main__':
    unittest.main()
