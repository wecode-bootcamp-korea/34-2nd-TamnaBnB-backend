import requests
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
            return JsonResponse({"message": "INVALID_USER"}, status=400)

    return wrapper

class KakaoSignin:
    def __init__(self, REST_API_KEY, REDIRECT_URI) :
        self.client_id       = REST_API_KEY
        self.redirect_uri    = REDIRECT_URI
        self.kakao_token_url = "https://kauth.kakao.com/oauth/token"
        self.kakao_user_url  = "https://kapi.kakao.com/v2/user/me"

    def get_kakao_token(self, code):
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
        
        body = {
            "grant_type"   : "authorization_code",
            "client_id"    : self.client_id,
            "redirect_uri" : self.redirect_uri,
            "code"         : code
        }

        response = requests.post(self.kakao_token_url, data=body, headers=headers, timeout=3)

        if not response.status_code == 200 :
            return JsonResponse({"message": "INVALID_REQUESTS"}, status = response.status_code)

        kakao_token = response.json()["access_token"]
        
        return kakao_token

    def get_user_information(self, kakao_token):
        headers = {
                "Authorization": f"Bearer {kakao_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }

        response = requests.get(self.kakao_user_url, headers=headers)

        if not response.status_code == 200 :
            return JsonResponse({"message": "INVALID_REQUESTS"}, status=response.status_code)

        return response.json()