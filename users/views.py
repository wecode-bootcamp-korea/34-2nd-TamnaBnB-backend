import requests
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User

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
            
            user_headers = {
                "Authorization": f"Bearer {kakao_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            }
            
            kakao_user_information = requests.get("https://kapi.kakao.com/v2/user/me", headers = user_headers).json()

            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_user_information["id"],
                defaults = {
                    "email"         : kakao_user_information["kakao_account"]["email"],
                    "name"          : kakao_user_information["kakao_account"]["profile"]["nickname"],
                    "profile_img"   : kakao_user_information["kakao_account"]["profile"]["profile_image_url"],
                    "birthday_date" : kakao_user_information["kakao_account"]["birthday"]
                }
            )

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