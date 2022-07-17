import json
from tempfile import TemporaryFile
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from core.utils      import token_decorator, KakaoSignin
from core.s3uploader import FileUpload, s3_client
from users.models    import User, Wishlist
from rooms.models    import Room

class KakaoSignInView(View):
    def get(self, request):
        try:
            code = request.GET.get("code")
            
            kakao_api              = KakaoSignin(settings.REST_API_KEY ,settings.REDIRECT_URI)
            kakao_token            = kakao_api.get_kakao_token(code)
            kakao_user_information = kakao_api.get_user_information(kakao_token)

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
                "access_token": access_token,
                "user_image"  : user.profile_img
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

class WishlistView(View):
    @token_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            room = Room.objects.get(id=data["room_id"])

            if Wishlist.objects.filter(user=user, room=room).exists():
                Wishlist.objects.filter(user=user, room=room).delete()
                return JsonResponse({"message": "DELETE_SUCCESS"}, status=200)
            
            Wishlist.objects.create(
                user = user,
                room = room
            )
            
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except Room.DoesNotExist:
            return JsonResponse({"message": "INVALID_ROOM"}, status=400)

    @token_decorator
    def get(self, reqeust):
        user      = reqeust.user
        wishlists = Wishlist.objects.filter(user_id=user.id)\
                    .select_related("user", "room")\
                    .order_by("-created_at")\
        
        result = [
            {
                "id"         : wishlist.id,
                "room"       : {
                    "id"            : wishlist.room.id,
                    "name"          : wishlist.room.name,
                    "thumbnail_img" : wishlist.room.thumbnail_img,
                    "check_in"      : wishlist.room.check_in,
                    "check_out"     : wishlist.room.check_out
                }

            } for wishlist in wishlists
        ]
        
        return JsonResponse({"result": result}, status=200)
        