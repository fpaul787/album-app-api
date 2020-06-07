from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='adminFP@fp.com',
            password='password123'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@fp.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that usrs are listed on user page"""
        url = reverse('admin:core_user_changelist')  # generate url for list user page
        res = self.client.get(url)  # perfrom http get

        self.assertContains(res, self.user.name)  # check if http req returns status 200
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertTrue(res.status_code, 200)
