# I'm not able to verify what are licences for my test images
# If these are yours and you don't want them here, let me know and I'll use different

import os
import unittest
import hashlib

import requests
import pixhostuploader as pixhost

_cd = os.path.dirname(os.path.realpath(__file__))


class PixhostFirstTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PixhostFirstTestCase, self).__init__(*args, **kwargs)
        self.uploaded = None
        self.images = [
            os.path.join(_cd, 'IBM_PCjr_System_1.jpg'),
            os.path.join(_cd, 'ibm5150.jpg'),
        ]
        self.uploaded = pixhost.upload(self.images)

    def test_upload(self):
        self.assertEqual(len(self.uploaded), len(self.images))
        for upload in self.uploaded:
            self.assertIsInstance(upload['thumb_image'], str)
            self.assertTrue(len(upload['thumb_image']) > 0)
            self.assertIsInstance(upload['full_size_image'], str)
            self.assertTrue(len(upload['full_size_image']) > 0)
            self.assertIsInstance(upload['page_url'], str)
            self.assertTrue(len(upload['page_url']) > 0)

    def test_status_codes(self):
        test_img_response = requests.get(self.uploaded[0]['full_size_image'])
        self.assertEqual(test_img_response.status_code, 200)

        # check the thumb exists
        self.assertEqual(requests.get(self.uploaded[0]['thumb_image']).status_code, 200)

        # url with image page on pixhost.org exists
        self.assertEqual(requests.get(self.uploaded[0]['page_url']).status_code, 200)

    def test_md5(self):
        # download the uploaded file
        test_img_response = requests.get(self.uploaded[0]['full_size_image'])

        # check md5 of both files
        uploaded_md5 = hashlib.md5(test_img_response.content).hexdigest()
        with open(self.images[0], 'rb') as f:
            orig_md5 = hashlib.md5(f.read()).hexdigest()
        self.assertEqual(uploaded_md5, orig_md5)

class PixhostSecondTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PixhostSecondTestCase, self).__init__(*args, **kwargs)
        self.image = os.path.join(_cd, 'ibm5150.jpg')
        self.uploaded = pixhost.upload(self.image)

    def test_md5(self):
        test_img_response = requests.get(self.uploaded['full_size_image'])
        uploaded_md5 = hashlib.md5(test_img_response.content).hexdigest()
        with open(self.image, 'rb') as f:
            orig_md5 = hashlib.md5(f.read()).hexdigest()

        self.assertEqual(uploaded_md5, orig_md5)

if __name__ == '__main__':
    unittest.main()