import bleach
from django.db import models
from django.conf import settings
from django.utils import timezone
from django_cryptography.fields import encrypt
from django.core.exceptions import ValidationError


class NoteBookDBConfig(models.Model):
    SUPPORTED_DATABASES = [
        (1, "Postgres"),
    ]

    db_type = models.PositiveSmallIntegerField(choices=SUPPORTED_DATABASES)

    db_name = models.CharField(max_length=100)
    db_user = models.CharField(max_length=100)
    db_password = encrypt(models.CharField(max_length=255))
    db_host = encrypt(models.CharField(max_length=255))
    db_port = models.CharField(max_length=6)


class NoteBook(models.Model):
    name = models.CharField(max_length=60)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    db_config = models.OneToOneField(NoteBookDBConfig, on_delete=models.CASCADE)


class NoteBookCell(models.Model):
    CELL_TYPES = [
        (1, "SQL Code"),
        (2, "Text"),
    ]

    notebook = models.ForeignKey(
        NoteBook, on_delete=models.CASCADE, related_name="cells"
    )
    type = models.PositiveSmallIntegerField(choices=CELL_TYPES)
    content = models.TextField(max_length=2000)

    def clean(self):
        if self.type == 1 and len(self.content) > 500:
            raise ValidationError("SQL code cannot exceed 500 characters")

    def save(self, *args, **kwargs):
        if self.type == 2:
            self.content = bleach.linkify(
                bleach.clean(self.content, tags=set())  # Disallow html tags
            )

        return super().save(*args, **kwargs)
