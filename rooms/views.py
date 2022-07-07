from datetime import datetime, timedelta

from django.views import View
from django.http  import JsonResponse
from django.db.models  import Q, Avg
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