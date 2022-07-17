import jwt
import json

from unittest.mock import MagicMock, patch

from django.test                    import TestCase, Client
from django.conf                    import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User, Host, Wishlist
from rooms.models import Room, Region

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

class WishlistTest(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(
            id       = 1,
            kakao_id = 12345678
        )

        User.objects.create(
            id       = 2,
            kakao_id = 12345678
        )

        Host.objects.create(
            id            = 1,
            nickname      = "test",
            profile_img   = "test_profile.jpg",
            is_super_host = True,
            user_id       = 1
        )

        Region.objects.create(
            id   = 1,
            name = "제주시"
        )

        Room.objects.create(
            id            = 1,
            name          = "test1",
            description   = "test1",
            thumbnail_img = "test1.jpg",
            price         = 35000.00,
            max_guest     = 5,
            max_pet       = 5,
            check_in      = "13:00",
            check_out     = "11:00",
            bedroom       = "2",
            bed_count     = "2",
            latitude      = 37.123456,
            longitude     = 125.123456,
            address       = "경기도 오산시 오산로 77",
            region_id     = 1,
            host_id       = 1
        )

        Wishlist.objects.create(
            id      = 1,
            user_id = 2,
            room_id = 1
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Region.objects.all().delete()
        Room.objects.all().delete()
        Wishlist.objects.all().delete()

    def test_success_wishlist_add(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": access_token}
        body    = {
            "room_id" : 1
        }

        response = self.client.post("/users/wishlist", json.dumps(body), **headers, content_type="application/json")
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_success_wishlist_delete(self):
        access_token = jwt.encode({"user_id": 2}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}
        body         = {
            "room_id" : 1
        }

        response = self.client.post("/users/wishlist", json.dumps(body), **headers, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "DELETE_SUCCESS"})

    def test_success_wishlist_load(self):
        access_token = jwt.encode({"user_id": 2}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        response = self.client.get("/users/wishlist", **headers, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result" : [
                {
                    "id"         : 1,
                    "room"       : {
                        "id"            : 1,
                        "name"          : "test1",
                        "thumbnail_img" : "test1.jpg",
                        "check_in"      : "13:00",
                        "check_out"     : "11:00"
                    }

                }
            ]
        })
    def test_fail_keyerror(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}
        response     = self.client.post("/users/wishlist", **headers, content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_fail_invalid_room(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": access_token}
        body    = {
            "room_id" : 1234
        }

        response = self.client.post("/users/wishlist", json.dumps(body), **headers, content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_ROOM"})