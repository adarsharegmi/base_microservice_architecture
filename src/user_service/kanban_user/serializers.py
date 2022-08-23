from rest_framework import serializers
from kanban_user.models import KanbanUser


class KanbanUserSerializer(serializers.ModelSerializer):
    kanban_group = serializers.StringRelatedField(many=True)

    class Meta:
        model = KanbanUser
        fields = ["group_name", "date_created", "board"]
        extra_kwargs = {"boards": {"required": False}}
