import jwt

from django.test import TestCase, Client

from django.conf import settings

from users.models        import User, Host
from rooms.models        import Room, Region
from reservations.models import Reservation, ReservationStatus

class ReservationTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        User.objects.create(
            id       = 1,
            kakao_id = 12345679
        )
        Host.objects.bulk_create([
            Host(
                id            = 1,
                name          = "sangwoong",
                profile_img   = "test.jpg",
                is_super_host = True,
            ),
            Host(
                id            = 2,
                name          = "woong",
                profile_img   = "test.jpg",
                is_super_host = True,
            ),
            Host(
                id            = 3,
                name          = "sang",
                profile_img   = "test.jpg",
                is_super_host = True,
            )
        ])
        Region.objects.bulk_create([
            Region(
                id   = 1,
                name = "제주시"
            ),
            Region(
                id   = 2,
                name = "서귀포시"
            )
        ])
        Room.objects.bulk_create([
            Room(
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
                host_id       = 1,
                region_id     = 1
            ),
            Room(
                id            = 2,
                name          = "test2",
                description   = "test2",
                thumbnail_img = "test2.jpg",
                price         = 45000.00,
                max_guest     = 5,
                max_pet       = 5,
                check_in      = "13:00",
                check_out     = "11:00",
                bedroom       = "2",
                bed_count     = "2",
                latitude      = 37.123456,
                longitude     = 125.123456,
                address       = "경기도 오산시 오산로 77",
                host_id       = 1,
                region_id     = 1
            ),
            Room(
                id            = 3,
                name          = "test3",
                description   = "test3",
                thumbnail_img = "test3.jpg",
                price         = 55000.00,
                max_guest     = 5,
                max_pet       = 5,
                check_in      = "13:00",
                check_out     = "11:00",
                bedroom       = "2",
                bed_count     = "2",
                latitude      = 37.123456,
                longitude     = 125.123456,
                address       = "경기도 오산시 오산로 77",
                host_id       = 1,
                region_id     = 1
            ),
        ])
        ReservationStatus.objects.bulk_create([
            ReservationStatus(
                id   = 1,
                name = "예약 완료"
            )
        ])
        Reservation.objects.bulk_create([
            Reservation(
                id = 1, 
                reservation_number = "0000-0000-0001",
                accomodation_fee   = 50000.00,
                check_in_date      = "2022-08-03",
                check_out_date     = "2022-08-04",
                num_of_guest       = 5,
                num_of_pet         = 5,
                user_id            = 1,
                room_id            = 3,
                status_id          = 1
            ),
            Reservation(
                id = 2, 
                reservation_number = "0000-0000-0002",
                accomodation_fee   = 50000.00,
                check_in_date      = "2022-08-01",
                check_out_date     = "2022-08-02",
                num_of_guest       = 5,
                num_of_pet         = 5,
                user_id            = 1,
                room_id            = 1,
                status_id          = 1
            ),
            Reservation(
                id = 3, 
                reservation_number = "0000-0000-0003",
                accomodation_fee   = 50000.00,
                check_in_date      = "2022-08-07",
                check_out_date     = "2022-08-09",
                num_of_guest       = 5,
                num_of_pet         = 5,
                user_id            = 1,
                room_id            = 2,
                status_id          = 1
            ),
        ])

    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Room.objects.all().delete()
        Reservation.objects.all().delete()
        ReservationStatus.objects.all().delete()

    def test_success_get_reservation(self):
        access_token = jwt.encode({"user_id": 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        response     = self.client.get("/reservations", **headers, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results" : {
                "reservation" : [
                    {
                        "id"                 : 3,
                        "reservation_number" : "0000-0000-0003",
                        "accomodation_fee"   : "50000.00",
                        "check_in_date"      : "2022-08-07",
                        "check_out_date"     : "2022-08-09",
                        "num_of_guest"       : 5,
                        "num_of_pet"         : 5,
                        "status"             : "예약 완료",
                        "room"  : {
                            "id"            : 2,
                            "name"          : "test2",
                            "thumbnail_img" : "test2.jpg",
                            "check_in"      : "13:00",
                            "check_out"     : "11:00",
                        }
                    },
                    {
                        "id"                 : 1,
                        "reservation_number" : "0000-0000-0001",
                        "accomodation_fee"   : "50000.00",
                        "check_in_date"      : "2022-08-03",
                        "check_out_date"     : "2022-08-04",
                        "num_of_guest"       : 5,
                        "num_of_pet"         : 5,
                        "status"             : "예약 완료",
                        "room"  : {
                            "id"            : 3,
                            "name"          : "test3",
                            "thumbnail_img" : "test3.jpg",
                            "check_in"      : "13:00",
                            "check_out"     : "11:00",
                        }
                    },
                    {
                        "id"                 : 2,
                        "reservation_number" : "0000-0000-0002",
                        "accomodation_fee"   : "50000.00",
                        "check_in_date"      : "2022-08-01",
                        "check_out_date"     : "2022-08-02",
                        "num_of_guest"       : 5,
                        "num_of_pet"         : 5,
                        "status"             : "예약 완료",
                        "room"  : {
                            "id"            : 1,
                            "name"          : "test1",
                            "thumbnail_img" : "test1.jpg",
                            "check_in"      : "13:00",
                            "check_out"     : "11:00",
                        }
                    }
                ]
            }
        })

    def test_fail_invalid_signature_token_error(self):
        access_token = jwt.encode({"user_id": 1}, "abscef", settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        response = self.client.get("/reservations", **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "INVALID_SIGNATURE_OF_TOKEN"})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_token_decode_error(self):
        headers      = {"HTTP_Authorization": "DECODED_TOKEN"}

        response = self.client.get("/reservations", **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "DECODE_ERROR"})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_invalid_user_error(self):
        access_token = jwt.encode({"user_id": 3}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization": access_token}

        response = self.client.get("/reservations", **headers, content_type="application/json")
        
        self.assertEqual(response.json(), {"message": "INVALID_USER"})
        self.assertEqual(response.status_code, 400)