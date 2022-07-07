import jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def token_decorator(func):
    def wrapper(self, request, *args, **kwargs) :
        try:
            access_token = request.headers.get("Authorization", None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id = payload["user_id"])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({"message": "INVALID_SIGNATURE_OF_TOKEN"}, status=400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "DECODE_ERROR"}, status=400)

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        except User.DoesNotExist :
            return JsonResponse({"message": "INNALID_USER"}, status=400)

    return wrapper