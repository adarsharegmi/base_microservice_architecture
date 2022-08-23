from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from kanban_board.models import KanbanBoard
from kanban_board.serializers import KanbanBoardSerializer
from user_login.decorator import authorize


class KanbanBoardAPIView(APIView):
    # list all the boards
    def get(self, request, *args, **kwargs):
        """
        list boards
        """
        boards = KanbanBoard.objects.all()
        serializer = KanbanBoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        register the kanban KanbanBoard
        """
        data = {
            "name": request.data.get("name"),
            "date_created": request.data.get("date_created"),
            "description": request.data.get("description"),
            "nickname": request.data.get("nickname"),
        }
        serializer = KanbanBoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KanbanBoardDetailView(APIView):
    @authorize
    def get(self, request, board_id, *args, **kwargs):
        """
        list the specific board
        """
        try:
            board = KanbanBoard.objects.get(id=board_id)
            serializer = KanbanBoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KanbanBoard.DoesNotExist:
            return Response(
                {"res": "no board found"}, status=status.HTTP_400_BAD_REQUEST
            )

    @authorize
    def put(self, request, board_id, *args, **kwargs):
        """
        update the kanban board details
        """
        board_instance = KanbanBoard.objects.get(id=board_id)
        if not board_instance:
            return Response(
                {"res": "no board found for the board id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "name": request.data.get("name"),
            "date_created": request.data.get("date_created"),
            "description": request.data.get("description"),
            "nickname": request.data.get("nickname"),
        }
        serializer = KanbanBoardSerializer(instance=board_instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authorize
    def delete(self, request, board_id, *args, **kwargs):
        """
        delete the board
        """
        board_instance = KanbanBoard.objects.get(id=board_id)
        if not board_instance:
            return Response(
                {"res": "object with board id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        board_instance.delete()
        return Response({"res": "board is deleted"}, status=status.HTTP_200_OK)
