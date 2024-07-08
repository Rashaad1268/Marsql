from rest_framework import serializers

from authentication.serializers import UserSerializer

from . import models


class NoteBookDBConfigCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NoteBookDBConfig
        fields = ("db_type", "db_name", "db_user", "db_password", "db_host", "db_port")
        extra_kwargs = {"db_password": {"write_only": True}}


class NoteBookDBConfigSerializer(serializers.ModelSerializer):
    db_type_display = serializers.SerializerMethodField()

    def get_db_type_display(self, db_conf):
        return db_conf.get_db_type_display()

    class Meta:
        model = models.NoteBookDBConfig
        fields = (
            "db_type",
            "db_type_display",
            "db_name",
            "db_user",
            "db_host",
            "db_port",
        )


class NoteBookCreateSerializer(serializers.ModelSerializer):
    db_config = NoteBookDBConfigCreateSerializer

    class Meta:
        model = models.NoteBook
        fields = ("name", "db_config")


class NoteBookSerializer(NoteBookCreateSerializer):
    creator = UserSerializer()
    db_config = NoteBookDBConfigSerializer()

    class Meta(NoteBookCreateSerializer.Meta):
        fields = ("id", "name", "creator", "created_at", "db_config")


class NoteBookCellCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NoteBookCell
        fields = ("type", "content")


class NoteBookCellSerializer(NoteBookCellCreateSerializer):
    class Meta(NoteBookCellCreateSerializer.Meta):
        fields = NoteBookCellCreateSerializer.Meta.fields + ("id", "notebook")
