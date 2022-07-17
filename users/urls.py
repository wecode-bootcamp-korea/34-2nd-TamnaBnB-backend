from django.urls import path

from users.views import KakaoSignInView, ProfileImageUploader

urlpatterns = [
    path("/kakao-signin", KakaoSignInView.as_view()),
    path("/profile-img-upload", ProfileImageUploader.as_view())
]