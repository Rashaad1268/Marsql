from rest_framework.permissions import IsAuthenticated


class NoteBookViewSetPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.creator
