from django.test import TestCase
from django.contrib.auth.models import User

class RegistrationTestCase(TestCase):

    def setUp(self):
        # Create an initial user
        User.objects.create_user(username="johndoe", password="Test@123")

    def test_duplicate_username(self):
        # Attempt to register a user with the same username
        response = self.client.post('/register/', {
            'username': 'johndoe',  # Duplicate username
            'password': 'NewPassword@123',
            'confirm_password': 'NewPassword@123'
        })

        # Assert that the response contains the expected error message
        self.assertContains(response, "Username already exists", status_code=200)

        # Assert that no additional user was created
        self.assertEqual(User.objects.filter(username="johndoe").count(), 1)
