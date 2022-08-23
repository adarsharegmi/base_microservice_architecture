from django.contrib import admin
from django.urls import path
from kanban_board.views import KanbanBoardAPIView, KanbanBoardDetailView

urlpatterns = [
    path("api/board/", KanbanBoardAPIView.as_view()),
    path("api/board/<str:board_id>/", KanbanBoardDetailView.as_view()),
]
