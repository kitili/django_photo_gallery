from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import RequestFactory, TestCase
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from pathlib import Path

from .admin import PhotoAdmin


def create_uploaded_file_object(image_path):
    """Create a `SimpleUploadedFile` object using a specified image path."""
    return SimpleUploadedFile(name='test_image.jpg',
                              content=open(image_path, 'rb').read(),
                              content_type='image/jpeg')


class MockPhoto(models.Model):
    large_img_path = Path(__file__).resolve().parent / 'test_images/2500x1500.jpg'
    mock_large_upload = create_uploaded_file_object(large_img_path)
    downsized_image = ImageSpecField(source='mock_large_upload',
                                     processors=[ResizeToFit(width=500)],
                                     format='JPEG')

    small_img_path = Path(__file__).resolve().parent / 'test_images/200x100.jpg'
    mock_small_upload = create_uploaded_file_object(large_img_path)
    upsized_image = ImageSpecField(source='mock_small_upload',
                                   processors=[ResizeToFit(width=500)],
                                   format='JPEG')


class PhotoModelTests(TestCase):

    def test_image_downsizing(self):
        """Test that ImageSpecField downsizes a mock upload image to a width of 500px."""
        photo = MockPhoto()
        self.assertEqual(photo.downsized_image.width, 500)

    def test_image_upsizing(self):
        """Test that ImageSpecField upsizes a mock upload image to a width of 500px."""
        photo = MockPhoto()
        self.assertEqual(photo.upsized_image.width, 500)


class MockPhotoAdmin(PhotoAdmin):
    def __init__(self):
        pass


class PhotoAdminTests(TestCase):

    request = RequestFactory()

    def test_get_fields_add(self):
        """Test that `thumbnail_img_tag` is excluded from add view `fields`"""
        photo_admin = MockPhotoAdmin()
        fields = photo_admin.get_fields(self.request)
        self.assertEqual(fields, ['large_image'])

    def test_get_fields_change(self):
        """Test that `thumbnail_img_tag` is included in change view `fields`"""
        photo_admin = MockPhotoAdmin()
        fields = photo_admin.get_fields(self.request, obj=MockPhoto())
        self.assertEqual(fields, ['large_image', 'thumbnail_img_tag'])