from django.test          import TestCase, Client

from users.models         import User, Host
from reviews.models       import Review
from rooms.models         import Region, Room, RoomImage, Facility, Type, Category
from reservations.models  import Reservation, ReservationStatus

class RoomListTest(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.bulk_create([
            User(
                id       = 1,
                kakao_id = 12345679
            ),
            User(
                id       = 2,
                kakao_id = 12345675
            ),
            User(
                id       = 3,
                kakao_id = 12345678
            )
        ])
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
        Review.objects.bulk_create([
            Review(
                id      = 1,
                content = "테스트 리뷰입니다.",
                ratings = 5.00,
                user_id = 1,
                room_id = 1
            ),
            Review(
                id      = 2,
                content = "테스트 리뷰입니다.",
                ratings = 5.00,
                user_id = 2,
                room_id = 2
            ),
            Review(
                id      = 3,
                content = "테스트 리뷰입니다.",
                ratings = 5.00,
                user_id = 3,
                room_id = 3
            ),
        ])
        RoomImage.objects.bulk_create([
            RoomImage(
                id        = 1,
                image_url = "test1.jpg",
                room_id   = 1
            ),
            RoomImage(
                id        = 2,
                image_url = "test2.jpg",
                room_id   = 2
            ),
            RoomImage(
                id        = 3,
                image_url = "test3.jpg",
                room_id   = 3
            )
        ])
        Facility.objects.bulk_create([
            Facility(
                id = 1,
                name = "수영장",
            ),
            Facility(
                id   = 2,
                name = "와이파이",
            ),
            Facility(
                id   = 3,
                name = "주방",
            )
        ])
        Type.objects.bulk_create([
            Type(
                id   = 1,
                name = "집 전체"
            ),
            Type(
                id   = 2,
                name = "개인실"
            ),
            Type(
                id   = 3,
                name = "다인실"
            )
        ])
        Category.objects.bulk_create([
            Category(
                id   = 1,
                name = "산장"
            ),
            Category(
                id   = 2,
                name = "디자인"
            ),
            Category(
                id   = 3,
                name = "초소형주택"
            )
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
                room_id            = 1,
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
                user_id            = 2,
                room_id            = 2,
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
                user_id            = 3,
                room_id            = 3,
                status_id          = 1
            ),
        ])

        for i in range(1, 3):
            Room.objects.get(id=i).types.add(Type.objects.get(id=i))
            Room.objects.get(id=i).facilities.add(Facility.objects.get(id=i))
            Room.objects.get(id=i).categories.add(Category.objects.get(id=i))

    def tearDown(self):
        User.objects.all().delete()
        Region.objects.all().delete()
        Review.objects.all().delete()
        Room.objects.all().delete()
        RoomImage.objects.all().delete()
        Facility.objects.all().delete()
        Type.objects.all().delete()
        Category.objects.all().delete()
        Reservation.objects.all().delete()

    def test_success_roomlist(self):
        response = self.client.get("/rooms")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
           "room_list": [
            {
                "id"            : 1,
                "name"          : "test1",
                "description"   : "test1",
                "thumbnail_img" : "test1.jpg",
                "price"         : "35000.00",
                "check_in_time" : "13:00",
                "check_out_time": "11:00",
                "room_info"     : "최대인원 5명 반려동물 동반 가능",
                "bedroom"       : "2",
                "bed_count"     : "2",
                "latitude"      : 37.123456,
                "longitude"     : 125.123456,
                "address"       : "경기도 오산시 오산로 77",
                "region"        : "제주시",
                "ratings_avg"   : "5.000000",
                "room_images"   : ["test1.jpg"]
            },
            {
                "id"            : 2,
                "name"          : "test2",
                "description"   : "test2",
                "thumbnail_img" : "test2.jpg",
                "price"         : "45000.00",
                "check_in_time" : "13:00",
                "check_out_time": "11:00",
                "room_info"     : "최대인원 5명 반려동물 동반 가능",
                "bedroom"       : "2",
                "bed_count"     : "2",
                "latitude"      : 37.123456,
                "longitude"     : 125.123456,
                "address"       : "경기도 오산시 오산로 77",
                "region"        : "제주시",
                "ratings_avg"   : "5.000000",
                "room_images"   : ["test2.jpg"]
            },
            {
                "id"            : 3,
                "name"          : "test3",
                "description"   : "test3",
                "thumbnail_img" : "test3.jpg",
                "price"         : "55000.00",
                "check_in_time" : "13:00",
                "check_out_time": "11:00",
                "room_info"     : "최대인원 5명 반려동물 동반 가능",
                "bedroom"       : "2",
                "bed_count"     : "2",
                "latitude"      : 37.123456,
                "longitude"     : 125.123456,
                "address"       : "경기도 오산시 오산로 77",
                "region"        : "제주시",
                "ratings_avg"   : "5.000000",
                "room_images"   : ["test3.jpg"]
            },
           ] 
        })

    def test_success_roomlist_filter_one(self):
        response = self.client.get("/rooms?region_id=1&bed_room=2&max_price=40000&check_in=2022-08-01&check_out=2022-08-02")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "room_list": [
                {
                    "id"            : 1,
                    "name"          : "test1",
                    "description"   : "test1",
                    "thumbnail_img" : "test1.jpg",
                    "price"         : "35000.00",
                    "check_in_time" : "13:00",
                    "check_out_time": "11:00",
                    "room_info"     : "최대인원 5명 반려동물 동반 가능",
                    "bedroom"       : "2",
                    "bed_count"     : "2",
                    "latitude"      : 37.123456,
                    "longitude"     : 125.123456,
                    "address"       : "경기도 오산시 오산로 77",
                    "region"        : "제주시",
                    "ratings_avg"   : "5.000000",
                    "room_images"   : ["test1.jpg"]
                },
            ]
        })

    def test_success_roomlist_filter_two(self):
        response = self.client.get("/rooms?region_id=1&bed_room=2&min_price=40000&max_price=60000&check_in=2022-07-29&check_out=2022-08-02")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "room_list": [
                {
                    "id"            : 3,
                    "name"          : "test3",
                    "description"   : "test3",
                    "thumbnail_img" : "test3.jpg",
                    "price"         : "55000.00",
                    "check_in_time" : "13:00",
                    "check_out_time": "11:00",
                    "room_info"     : "최대인원 5명 반려동물 동반 가능",
                    "bedroom"       : "2",
                    "bed_count"     : "2",
                    "latitude"      : 37.123456,
                    "longitude"     : 125.123456,
                    "address"       : "경기도 오산시 오산로 77",
                    "region"        : "제주시",
                    "ratings_avg"   : "5.000000",
                    "room_images"   : ["test3.jpg"]
                },
            ]
        })
    