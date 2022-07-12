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
            room      = data["room_id"]
            user      = request.user

            Review.objects.create(
                content   = content,
                ratings   = ratings,
                image_url = image_url,
                user      = user,
                room      = room
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
           return  JsonResponse({"Message": "KEY_ERROR"}, status=400)

"""
s3 upload

boto3 library

bucket -> client 역할을 하는 객체를 만든다.

client.uplaod_fileobj(file)
put_object

이름이 중복되면 안됨
uuid로 해결
"""
