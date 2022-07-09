from django.urls import path

from rooms.views import RoomsListView, RoomDetailView

urlpatterns = [
    path("", RoomsListView.as_view()),
    path("/<int:room_id>", RoomDetailView.as_view())
]