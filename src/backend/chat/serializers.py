from rest_framework import serializers

from . import models
from notebooks.serializers import NoteBookCellSerializer


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatMessage
        fields = ("content", "attached_image", "attached_file")


class ChatMessageSerializer(ChatMessageCreateSerializer):
    cell = NoteBookCellSerializer()

    class Meta(ChatMessageCreateSerializer.Meta):
        model = models.ChatMessage
        fields = ChatMessageCreateSerializer.Meta.fields + (
            "id",
            "author_type",
            "created_at",
            "attached_image",
            "attached_file",
            "cell",
        )
