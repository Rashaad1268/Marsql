from typing import Optional
from django.db import models
from rest_framework import status, viewsets, serializers
from rest_framework.response import Response


class CustomViewSet(viewsets.ModelViewSet):
    partial_serializer: Optional[serializers.Serializer] = None
    full_serializer: Optional[serializers.Serializer] = None

    def should_return_data(self):
        return True

    def get_serializer_class(self):
        if self.partial_serializer is None or self.full_serializer is None:
            raise NotImplementedError(
                "Specify partial_serializer and full_serializer or "
                "override the get_serializer_class() method"
            )

        if self.action.lower() in ("create", "partial_update", "update", "delete"):
            return self.partial_serializer
        else:
            return self.full_serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)

        if not self.should_return_data():
            return Response(status=status.HTTP_204_NO_CONTENT)

        headers = self.get_success_headers(serializer.data)
        return Response(
            self.full_serializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if not self.should_return_data():
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            self.full_serializer(instance, context=self.get_serializer_context()).data
        )

    def perform_create(self, serializer) -> models.Model:
        return serializer.save()

    def perform_update(self, serializer) -> models.Model:
        return serializer.save()
