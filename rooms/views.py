from datetime import datetime, timedelta

from django.views import View
from django.http  import JsonResponse
from django.db.models  import Avg, Count, Q
from reservations.models import Reservation

from rooms.models import Room
from reservations.models import Reservation

class RoomsListView(View):
    def get(self, request):
        check_in       = request.GET.get("check_in", None)
        check_out      = request.GET.get("check_out", None)
        offset         = int(request.GET.get("offset", 0))
        limit          = int(request.GET.get("limit", 25))
        reserved_rooms = []

        q = Q()

        if check_in and check_out :
            check_in_date  = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

            q |= Q(check_in_date__range  = [check_in_date, check_out_date-timedelta(days=1)])
            q |= Q(check_out_date__range = [check_in_date-timedelta(days= -1), check_out])
        
            reserved_rooms = Reservation.objects.filter(q)

        filter_set = {
            "region_id"   : "region_id",
            "bedroom"     : "bedroom",
            "bed_count"   : "bed_count",
            "min_price"   : "price__gte",
            "max_price"   : "price__lte",
            "max_guest"   : "max_guest__gte",
            "max_pet"     : "max_pet__gte",
            "type_id"     : "types__id",
            "category_id" : "categories__id"
        }

        filter = { filter_set.get(key) : value for key, value in request.GET.items() if filter_set.get(key) }
        
        rooms = Room.objects.filter(**filter)\
            .select_related("region")\
            .prefetch_related("images", "review_set")\
            .annotate(review_avg = Avg("review__ratings"))\
            .exclude(reservation__in=reserved_rooms)\
            .order_by("id")[offset:offset+limit]

        room_list = [
            {
                "id"             : room.id,
                "name"           : room.name,
                "description"    : room.description,
                "thumbnail_img"  : room.thumbnail_img,
                "price"          : room.price,
                "check_in_time"  : room.check_in,
                "check_out_time" : room.check_out,
                "room_info"      : f"최대인원 {room.max_guest}명 반려동물 동반 가능"\
                                    if room.max_pet > 0 else f"최대인원 {room.max_guest}명 반려동물 출입 불가",
                "bedroom"        : room.bedroom,
                "bed_count"      : room.bed_count,
                "latitude"       : float(room.latitude),
                "longitude"      : float(room.longitude),
                "address"        : room.address,
                "region"         : room.region.name,
                "ratings_avg"    : room.review_avg if True else "New",
                "room_images"    : [image.image_url for image in room.images.all()]
            } for room in rooms
        ]
        
        return JsonResponse({"room_list" : room_list}, status=200)

class RoomDetailView(View):
    def get(self, request, room_id):
        try:
            room = Room.objects\
                .select_related("host")\
                .prefetch_related("images", "review_set", "facilities", "types", "categories")\
                .annotate(review_count=Count('review__id'))\
                .annotate(review_avg=Avg("review__ratings"))\
                .get(id=room_id)

            room_info = {
                    "id"           : room.id,
                    "name"         : room.name,
                    "description"  : room.description,
                    "thumbnail_img": room.thumbnail_img,
                    "price"        : room.price,
                    "max_guest"    : room.max_guest,
                    "max_pet"      : room.max_pet,
                    "check_in"     : room.check_in,
                    "check_out"    : room.check_out,
                    "bedroom"      : room.bedroom,
                    "bed_count"    : room.bed_count,
                    "latitude"     : room.latitude,
                    "longitude"    : room.longitude,
                    "address"      : room.address,
                    "region"       : room.region.name,
                    "images"       : [image.image_url for image in room.images.all()],
                    "types"        : [type.name for type in room.types.all()],
                    "facilites"    : [facility.name for facility in room.facilities.all()],
                    "categories"   : [category.name for category in room.categories.all()],
                    "host"         : {
                        "id"           : room.host.id,
                        "name"         : room.host.name,
                        "nickname"     : room.host.nickname,
                        "profile_img"  : room.host.profile_img,
                        "is_super_host": room.host.is_super_host
                    },
                    "review"       : {
                        "ratings_count": room.review_count,
                        "ratings_avg"  : room.review_avg if True else "New",
                        "info"         : [
                            {
                                "id"               : review.id,
                                "user_name"        : review.user.name,
                                "user_profile_img" : review.user.profile_img,
                                "content"          : review.content,
                                "created_at"       : datetime.strftime(review.created_at, "%Y-%m-%d %H:%M"),
                            } for review in room.review_set.all().distinct().order_by("-created_at")
                        ]
                    }
                }

            return JsonResponse({"room_info": room_info}, status=200)

        except Room.DoesNotExist:
            return JsonResponse({"message": "INVALID_ROOM"}, status=400)
