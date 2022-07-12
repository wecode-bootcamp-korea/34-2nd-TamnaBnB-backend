import jwt

from django.test import TestCase, Client
from django.conf import settings

from reviews.models import Review
from users.models   import User, Host
from rooms.models   import Room, Region

class ReviewTest(TestCase) :
    def setUp(self):
        self.client = Client()

        User.objects.create(
            id            = 1,
            name          = "wecode",
            email         = "wecode@test.test",
            password      = "1q2w3e4r!@",
            birthday_date = "0101",
            profile_img   = "test.jpg",
            kakao_id      = 123456789
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

        Review.objects.create(
            content   = "테스트용 리뷰입니다.",
            ratings   = "4",
            image_url = "test1.jpg",
            user_id   = 1,
            room_id   = 1
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Region.objects.all().delete()
        Room.objects.all().delete()
        Review.objects.all().delete()

    def test_success_post_review(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        body = {
            "content"   : "테스트용 리뷰입니다.",
            "ratings"   : "3",
            "image_url" : "test.jpg",
            "user_id"   : 1,
            "room_id"   : 1
        }

        response = self.client.post("/reviews", body, **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "SUCCESS"})
        self.assertEqual(response.status_code, 200)

    def test_fail_key_error(self): 
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        body = {
            "content"   : "테스트용 리뷰입니다.",
            "ratings"   : "3",
            "image_url" : "tets.jpg",
            "user_id"   : 1,
        }

        response = self.client.post("/reviews", body, **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_invalid_signature_token_error(self):
        access_token = jwt.encode({"user_id": 1}, "abscef", settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        body = {
            "content"   : "테스트용 리뷰입니다.",
            "ratings"   : "3",
            "image_url" : "test.jpg",
            "user_id"   : 1,
            "room_id"   : 1
        }

        response = self.client.post("/reviews", body, **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "INVALID_SIGNATURE_OF_TOKEN"})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_token_decode_error(self):
        headers      = {"HTTP_Authorization": "DECODED_TOKEN"}

        body = {
            "content"   : "테스트용 리뷰입니다.",
            "ratings"   : "3",
            "image_url" : "test.jpg",
            "user_id"   : 1,
            "room_id"   : 1
        }

        response = self.client.post("/reviews", body, **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "DECODE_ERROR"})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_invailid_user_error(self):
        access_token = jwt.encode({"user_id": 2}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        body = {
            "content"   : "테스트용 리뷰입니다.",
            "ratings"   : "3",
            "image_url" : "test.jpg",
            "user_id"   : 2,
            "room_id"   : 1
        }

        response = self.client.post("/reviews", body, **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "INVALID_USER"})
        self.assertEqual(response.status_code, 400)

    def test_success_delete_review(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        response = self.client.delete("/reviews?room_id=1", **headers, content_type="application/json")

        self.assertEqual(response.json(), {"message": "SUCCESS"})
        self.assertEqual(response.status_code, 200)

    def test_fail_room_does_not_exist_error(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        response = self.client.delete("/reviews?room_id=123", **headers, content_type="application/json")

        self.assertEqual(response.json(), {"message": "INVALID_ROOM"})
        self.assertEqual(response.status_code, 400) 