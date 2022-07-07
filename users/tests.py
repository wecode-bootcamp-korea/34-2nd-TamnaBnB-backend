import jwt

from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase, Client

from users.models import User, Host, Wishlist

class UserTest(TestCase):
    def setUp(self):

        User.objects.create(
            id            = 1,
            name          = "wecode",
            email         = "wecode@test.test",
            password      = "1q2w3e4r!@",
            birthday_date = "0101",
            profile_img   = "test.jpg",
            kakao_id      = 123456789
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_success_get_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id": 123456789,
                    "kakao_account" : {
                        "email"    : "wecode@test.test",
                        "birthday" : "0101",
                        "profile"  : {
                            "nickname"          : "wecode",
                            "profile_image_url" : "test.jpg"
                        }
                    }
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse()) 
        headers             = {"HTTP_Authoriazation": "가짜 access_token"}
        response            = client.get("/users/kakao-signin", **headers)
        access_token        = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)  
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            "message"     : "SUCCESS_LOGIN",
            "access_token": access_token
        })

    @patch("users.views.requests")
    def test_success_create_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                "id": 123451429,
                "kakao_account" : {
                    "email"    : "wecode@test.test",
                    "birthday" : "0101",
                    "profile"  : {
                        "nickname"          : "wecode",
                        "profile_image_url" : "test.jpg"
                        }
                    }   
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse()) 
        headers             = {"HTTP_Authoriazation": "가짜 access_token"}
        response            = client.get("/users/kakao-signin", **headers)
        access_token        = jwt.encode({"user_id": 2}, settings.SECRET_KEY, settings.ALGORITHM)  
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            "message"     : "CREATED_NEW_USER",
            "access_token": access_token
        })

    @patch("users.views.requests")
    def test_keyerror_siginview(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                "kakao_account" : {
                    "email"    : "wecode@test.test",
                    "profile"  : {
                        "nickname"          : "wecode",
                        "profile_image_url" : "test.jpg"
                        }
                    }   
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse()) 
        headers             = {"HTTP_Authoriazation": "가짜 access_token"}
        response            = client.get("/users/kakao-signin", **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message": "KEY_ERROR"})