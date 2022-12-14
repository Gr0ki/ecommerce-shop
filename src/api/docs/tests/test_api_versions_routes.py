from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..views import versions_data


class APIVersionsRoutesListTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        """
        Specifying url, user password, and creating the user with staff permissions.
        Applying instructions from the rewritten 'setUpClass' classmethod.
        """
        cls.url = reverse("api-versions-routes")
        cls.password = "teststaffpassword"
        cls.username = "teststaff"
        cls.user = get_user_model().objects.all().filter(username=cls.username).first()
        if cls.user is None:
            cls.user = get_user_model().objects.create_user(
                cls.username, email="teststaff@test.com", password=cls.password
            )
            cls.user.is_staff = True
            cls.user.save()
        super().setUpClass()

    def test_response_data_for_guest(self):
        """
        Tests if appropriate data and response code are returned for an unauthorized user.
        """
        response = self.client.get(APIVersionsRoutesListTestCase.url)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_response_data_for_staff(self):
        """
        Tests if appropriate data and response code are returned for authorized staff user.
        """
        # Make all requests in the context of a logged in session
        self.client.login(
            username=APIVersionsRoutesListTestCase.username,
            password=APIVersionsRoutesListTestCase.password,
        )
        # Get the response and test its data
        response = self.client.get(APIVersionsRoutesListTestCase.url)
        self.assertEqual(len(response.data.keys()), len(versions_data.keys()))
        for key, value in versions_data.items():
            self.assertEqual(response.data[key], value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Log out
        self.client.logout()
