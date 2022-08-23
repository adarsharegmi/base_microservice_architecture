from rest_framework import serializers
from kanban_board.models import KanbanBoard
from user_service.kanban_user.serializers import KanbanUserSerializer


class KanbanBoardSerializer(serializers.ModelSerializer):
    kanban_group = KanbanUserSerializer(many=True, read_only=True)

    class Meta:
        model = KanbanBoard
        fields = ["name", "date_created", "description", "nickname", "kanban_group"]
