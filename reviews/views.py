import json

from django.http  import JsonResponse
from django.views import View

from core.utils     import token_decorator
from rooms.models   import Room
from reviews.models import Review

class ReviewView(View):
    @token_decorator
    def post(self, request):
        try:
            data      = json.loads(request.body)
            content   = data["content"]
            ratings   = data["ratings"]
            image_url = data["image_url"]
            room_id   = data["room_id"]
            user      = request.user

            Review.objects.create(
                content   = content,
                ratings   = ratings,
                image_url = image_url,
                user_id   = user.id,
                room_id   = room_id
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
           return  JsonResponse({"message": "KEY_ERROR"}, status=400)

    @token_decorator
    def delete(self, request):
        try:
            room_id = request.GET.get("room_id")
            room    = Room.objects.get(id=room_id)
            review  = Review.objects.get(user_id = request.user.id, room_id = room.id)
            
            review.delete()
            
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Room.DoesNotExist:
            return JsonResponse({"message": "INVALID_ROOM"}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"message": "INVALID_REVIEW"}, status=400)
