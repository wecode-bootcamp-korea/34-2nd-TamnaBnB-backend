from email.mime import application
import jwt
import json 

from unittest.mock import MagicMock, patch

from django.test                    import TestCase, Client
from django.conf                    import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User

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

    @patch("users.views.KakaoSignin")
    def test_success_get_user(self, mocked_kakao_api):
        client = Client()

        class MockedResponse:
            def get_kakao_token(self, code):
                return "kakao_token"

            def get_user_information(self, kakao_token):
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

        mocked_kakao_api.return_value = MockedResponse()

        body         = {"code" : "kakao_authorization_code"}
        response     = client.get("/users/kakao-signin", data=body, content_type="application/json")
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            "message"     : "SUCCESS_LOGIN",
            "access_token": access_token,
            "user_image"  : "test.jpg"
        })

    @patch("users.views.KakaoSignin")
    def test_success_create_user(self, mocked_kakao_api):
        client = Client()

        class MockedResponse:
            def get_kakao_token(self, code):
                return "kakao_token"

            def get_user_information(self, kakao_token):
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

        mocked_kakao_api.return_value = MockedResponse() 

        body         = {"code" : "kakao_authorization_code"}
        response     = client.get("/users/kakao-signin", data=body, content_type="application/json")
        access_token = jwt.encode({"user_id": 2}, settings.SECRET_KEY, settings.ALGORITHM)  

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            "message"     : "CREATED_NEW_USER",
            "access_token": access_token,
            "user_image"  : "test.jpg"
        })

    @patch("core.utils.KakaoSignin")
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
        headers             = {"HTTP_Authorization": "가짜 access_token"}
        response            = client.get("/users/kakao-signin", **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message": "KEY_ERROR"})

class ProfileImageUploaderTest(TestCase):
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

        self.client = Client()
        self.access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()

    @patch("core.s3uploader.FileUpload")
    def test_success_update_profile_img(self, mocked_client):
        
        class MockedResponse:
            def upload(self, file):
                return "https://tamna.s3.ap-northeast-2.amazonaws.com/img/test"

        mocked_client.return_value = MockedResponse()
        
        file = SimpleUploadedFile(
            "test1.jpg",
            content      = b"file_content",
            content_type = "image/jpg"
        )

        headers = {
            "HTTP_Authorization": self.access_token,
            "content-type"      : "multipart/form-data"
        }

        body = {
            "file" : file
        }
        
        response = self.client.post("/users/profile-img-upload", body, **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS"})
    
    @patch("core.s3uploader.FileUpload")
    def test_fail_update_profile_img(self, mocked_client):
        
        class MockedResponse:
            def upload(self, file):
                return "https://tamna.s3.ap-northeast-2.amazonaws.com/img/test"

        mocked_client.return_value = MockedResponse()
        
        file = SimpleUploadedFile(
            None,
            content      = b"file_content",
            content_type = "image/jpg"
        )

        headers = {
            "HTTP_Authorization": self.access_token,
            "content-type"      : "multipart/form-data"
        }

        body = {
            "file" : ""
        }
        
        response = self.client.post("/users/profile-img-upload", body, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "NONE_IMAGE"})

    