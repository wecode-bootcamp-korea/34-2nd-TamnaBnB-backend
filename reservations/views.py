import json

from decimal  import Decimal
from datetime import datetime

from django.views import View
from django.http  import JsonResponse

from core.utils                 import token_decorator
from rooms.models               import Room
from users.models               import User
from reservations.models        import Reservation, ReservationStatus
from reservations.reserved_code import reservation_code

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
        
    @token_decorator
    def post(self, request):
        try:
            data               = json.loads(request.body)
            price              = Decimal(data["price"])
            check_in_date      = datetime.strptime(data["check_in"], "%Y-%m-%d")
            check_out_date     = datetime.strptime(data["check_out"], "%Y-%m-%d")
            num_of_guest       = int(data["num_of_guest"])
            num_of_pet         = int(data["num_of_pet"])
            user               = request.user
            room               = Room.objects.get(id=data["room_id"])

            if price > user.point :
                return JsonResponse({"message": "OVER_LIMIT_OF_POINT"}, status=400)

            if check_in_date < datetime.now() :
                return JsonResponse({"message": "INVALID_DATE"}, status=400)
            
            if check_in_date >= check_out_date :
                return JsonResponse({"message": "INVALID_DATE"}, status=400)

            if num_of_guest > room.max_guest :
                return JsonResponse({"message": "OVER_LIMIT_OF_GUEST"}, status=400)

            if num_of_pet > room.max_pet :
                return JsonResponse({"message": "OVER_LIMIT_OF_PET"}, status=400)

            reservation, is_created = Reservation.objects.update_or_create(
                user_id  = user.id,
                room_id  = room.id,
                defaults = {
                    "reservation_number" : reservation_code,
                    "accomodation_fee"   : price,
                    "check_in_date"      : check_in_date,
                    "check_out_date"     : check_out_date,
                    "num_of_guest"       : num_of_guest,
                    "num_of_pet"         : num_of_pet,
                    "status_id"          : 1
                }
            )

            if not is_created :
                reservation.accomodation_fee = price
                reservation.check_in_date    = check_in_date
                reservation.check_out_date   = check_out_date
                reservation.num_of_guest     = num_of_guest
                reservation.num_of_pet       = num_of_pet
                
            reservation.save()

            User.objects.filter(id=user.id).update(
                point = user.point - reservation.accomodation_fee
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
        except ReservationStatus.DoesNotExist:
            return JsonResponse({"message": "INVALID_RESERVATION_STATUS"}, status=400)

        except Room.DoesNotExist:
            return JsonResponse({"message": "INVALID_ROOM"}, status=400)
        
