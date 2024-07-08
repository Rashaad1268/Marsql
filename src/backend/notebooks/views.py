from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    NoteBookCreateSerializer,
    NoteBookSerializer,
    NoteBookCellCreateSerializer,
    NoteBookCellSerializer,
)
from . import permissions, utils
from backend.viewsets import CustomViewSet
from .models import NoteBook, NoteBookCell
from .databases import postgres


class NoteBookViewSet(CustomViewSet):
    partial_serializer = NoteBookCreateSerializer
    full_serializer = NoteBookSerializer
    permission_classes = (permissions.NoteBookViewSetPermissions,)
    queryset = NoteBook.objects.select_related("db_config").all()

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_staff:
            notebook_count = NoteBook.objects.filter(creator=user).count()

            if notebook_count >= 3:
                raise PermissionDenied("Free users can't create more than 3 notebooks")

        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        notebook = self.get_object()
        serializer = self.get_serializer(notebook)

        if notebook.db_config.db_type == 1:
            db_schema = postgres.get_postgres_db_metadata(notebook.db_config)

        else:
            raise Response({"detail": "Notebook has unsupported database type"})

        return Response({"notebook": serializer.data, "db_schema": db_schema})

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class NoteBookCellViewSet(CustomViewSet):
    partial_serializer = NoteBookCellCreateSerializer
    full_serializer = NoteBookCellSerializer

    def get_queryset(self):
        if self.action == "list":
            return NoteBookCell.objects.filter(
                notebook__id=int(self.kwargs["notebook_pk"]),
                chatmessage__isnull=True,  # Don't select the cells that are used in a message
            ).order_by("id")
        return NoteBookCell.objects.filter(
            notebook__id=int(self.kwargs["notebook_pk"]),
        ).order_by("id")

    def perform_create(self, serializer):
        return serializer.save(notebook_id=int(self.kwargs["notebook_pk"]))

    def should_return_data(self):
        return self.action not in ("update", "partial_update")

    @action(methods=("POST",), detail=True, url_path="run")
    def run_cell(self, request, pk, notebook_pk):
        cell = self.get_object()

        if cell.type != 1:
            return Response(
                {"detail": "Only SQL code cells can be run"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        do_commit = request.data.get("commit", False) is True

        query = cell.content.strip()

        if not query:
            return Response(
                {"detail": "No code in cell to run"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            postgres.run_postgres_query(
                query=utils.modify_query(query),
                db_conf=cell.notebook.db_config,
                do_commit=do_commit,
            )
        )
