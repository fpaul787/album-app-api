import tempfile
import os

from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Album

from album.serializers import AlbumSerializer

ALBUMS_URL = reverse('album:album-list')


def image_upload_url(album_id):
    """Return URL for album cover upload"""
    return reverse('album:album-upload-image', args=[album_id])


def detail_url(album_id):
    """Retrun album detail URL"""
    return reverse('album:album-detail', args=[album_id])


def sample_album():
    """Create a sample album"""
    defaults = {
        'name': 'Enter the WU',
        'release_date': '2020-05-11',
        'artist': 'Wu-tang Clan',
    }

    return Album.objects.create(**defaults)


class PublicAlbumApiTests(TestCase):
    """Test unauthenticated album API create"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for anything other than view"""
        res = self.client.post(ALBUMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAlbumApiTests(TestCase):
    """Test unauthenticated album API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'fptest@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_albums(self):
        """Test retrieving a list of albums"""
        sample_album()

        res = self.client.get(ALBUMS_URL)

        albums = Album.objects.all().order_by('id')
        serializer = AlbumSerializer(albums, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_album(self):
        """Test creating an album"""
        payload = {
            'name': 'Enter the WU',
            'release_date': '2020-05-11',
            'artist': 'Wu-tang Clan',
        }
        res = self.client.post(ALBUMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_full_update_album(self):
        """Test updating a album with patch"""
        album = sample_album()

        payload = {
            'name': 'does not matter',
            'realease_date': '2020-06-09',
            'artist': 'Push'
        }
        url = detail_url(album.id)
        self.client.put(url, payload)

        album.refresh_from_db()
        self.assertEqual(album.artist, payload['artist'])


class AlbumCoverUploadTests(TestCase):
    """Test for uploading album cover"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'fptest@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.album = sample_album()

    def tearDown(self):
        self.album.album_cover.delete()

    def test_upload_image_to_recipe(self):
        """Test uploading image to album"""
        url = image_upload_url(self.album.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'album_cover': ntf}, format='multipart')

        self.album.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('album_cover', res.data)
        self.assertTrue(os.path.exists(self.album.album_cover.path))
