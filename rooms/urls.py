from django.urls import path

from rooms.views import RoomsListView

urlpatterns = [
    path("", RoomsListView.as_view())
]