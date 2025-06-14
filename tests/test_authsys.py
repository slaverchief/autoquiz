from rest_framework.test import APITestCase
from authsys.models import CustomUser
from django.urls import reverse

class AuthSysTest(APITestCase):
    @classmethod
    def setUp(cls):
        CustomUser.objects.create_user(username="user1", password='1')
        CustomUser.objects.create_user(username="user2", password='2')
        CustomUser.objects.create_user(username="user3", password='3')

    def test_signup(self):
        URL = reverse("user_api")
        resp1 = self.client.post(URL, {"username": "user2", "password": "1"}, format="json")
        resp2 = self.client.post(URL, {"username": "user"}, format="json")
        resp3 = self.client.post(URL, {"username": "user5", "password": "1"}, format="json")
        resp4 = self.client.post(URL, {"username": "user6", "password": ""}, format="json")
        resp5 = self.client.post(URL, {"username": "", "password": ""}, format="json")
        resp6 = self.client.post(URL, {"username": "", "password": "asd"}, format="json")
        self.assertEqual(resp1.status_code, 400)
        self.assertEqual(resp2.status_code, 400)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 400)
        self.assertEqual(resp5.status_code, 400)
        self.assertEqual(resp6.status_code, 400)

    def test_signin_success(self):
        URL = reverse('token_obtain_pair')
        resp1 = self.client.post(URL, {"username": "user1", "password": '1'})
        self.assertEqual(resp1.status_code, 200)
        token = resp1.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        auth_resp1 = self.client.get(reverse("user_api"))
        self.assertEqual(auth_resp1.status_code, 200)

    def test_signin_failure(self):
        URL = reverse('token_obtain_pair')
        resp1 = self.client.post(URL, {"username": "user212", "password": '1'})
        self.assertEqual(resp1.status_code, 401)
        resp2 = self.client.post(URL, {"username": "user212", "password": ''})
        self.assertEqual(resp2.status_code, 400)
