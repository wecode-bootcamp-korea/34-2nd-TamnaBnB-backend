import json

from core.utils   import token_decorator
from django.http  import JsonResponse
from django.views import View

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