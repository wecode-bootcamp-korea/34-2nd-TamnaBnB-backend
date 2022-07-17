from django.urls import path
from users.models import Wishlist

from users.views import KakaoSignInView, ProfileImageUploader, WishlistView

urlpatterns = [
    path("/kakao-signin", KakaoSignInView.as_view()),
    path("/profile-img-upload", ProfileImageUploader.as_view()),
    path("/wishlist", WishlistView.as_view())
]