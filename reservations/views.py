from django.views import View
from django.http import JsonResponse

from core.utils import token_decorator
from reservations.models import Reservation
from rooms.models import Room

class ReservationView(View):
    @token_decorator
    def get(self, request):
        user         = request.user
        reservations = Reservation.objects.filter(user = user)\
                        .order_by("-check_out_date")
        
        results = {
            "reservation" : [{
                "id"                 : reservation.id,
                "reservation_number" : reservation.reservation_number,
                "accomodation_fee"   : reservation.accomodation_fee,
                "check_in_date"      : reservation.check_in_date,
                "check_out_date"     : reservation.check_out_date,
                "num_of_guest"       : reservation.num_of_guest,
                "num_of_pet"         : reservation.num_of_pet,
                "status"             : reservation.status.name,
                "room"  : {
                    "id"            : reservation.room.id,
                    "name"          : reservation.room.name,
                    "thumbnail_img" : reservation.room.thumbnail_img,
                    "check_in"      : reservation.room.check_in,
                    "check_out"     : reservation.room.check_out
                }
            } for reservation in reservations ]
        }

        return JsonResponse({"results" : results}, status = 200) 
        