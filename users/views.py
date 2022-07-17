import requests
import jwt
import boto3
import uuid

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from core.utils      import token_decorator
from core.s3uploader import FileUpload, s3_client
from users.models    import User

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
            user_image   = user.profile_img if not is_created else None

            messages = {
                "message"     : message,
                "access_token": access_token,
                "user_image"  : user_image
            }

            return JsonResponse(messages, status=status_code)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class ProfileImageUploader(View):
    @token_decorator
    def post(self, request):
        try:    
            file           = request.FILES.get("file", None)
            s3__client     = FileUpload(s3_client)
            upload_img_url = s3__client.upload(file)
            user           = request.user
            
            if not file:
                return JsonResponse({"message": "NONE_IMAGE"}, status=400)

            User.objects.filter(id=user.id).update(
                profile_img = upload_img_url
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
