from django.core.exceptions import PermissionDenied

from backend.viewsets import CustomViewSet
from .serializers import NoteBookCreateSerializer, NoteBookSerializer

from . import permissions
from .models import NoteBook


class NoteBookViewSet(CustomViewSet):
    partial_serializer = NoteBookCreateSerializer
    full_serializer = NoteBookSerializer
    permission_classes = (permissions.NoteBookViewSetPermissions,)
    queryset = NoteBook.objects.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_staff:
            notebook_count = NoteBook.objects.filter(creator=user).count()

            if notebook_count >= 3:
                raise PermissionDenied("Free users can't create more than 3 notebooks")

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
