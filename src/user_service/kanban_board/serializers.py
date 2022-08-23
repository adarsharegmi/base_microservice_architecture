from rest_framework import serializers
from kanban_board.models import KanbanBoard


class KanbanBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanBoard
        fields = ["name", "date_created", "description", "nickname"]
