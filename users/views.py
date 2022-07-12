import requests
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User


class KakaoAPI:
    def __init__(self, token):
        self.token = token
        
    def get_user_information(self):
        user_headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        
        return requests.get("https://kapi.kakao.com/v2/user/me", headers = user_headers).json()

    def get_loaction(self):
        pass


class KakaoSignInView(View):
    def get(self, request):
        try:
            code          = request.GET.get("code")
            token_headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
            TOKEN_URL     = "https://kauth.kakao.com/oauth/token"
            
            data = {
                "grant_type"   : "authorization_code",
                "client_id"    : settings.REST_API_KEY,
                "redirect_uri" : settings.REDIRECT_URI,
                "code"         : code
            }
            
            kakao_token = requests.post(TOKEN_URL, headers = token_headers, data = data).json()["access_token"]
            
            kakao = KakaoAPI(kakao_token)

            kakao.get_user_information()

            user, is_created = User.objects.custom_queryset()
            status_code  = 201 if is_created else 200
            message      = "CREATED_NEW_USER" if is_created else "SUCCESS_LOGIN"
            access_token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            
            messages = {
                "message"     : message,
                "access_token": access_token
            }

            return JsonResponse(messages, status=status_code)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
