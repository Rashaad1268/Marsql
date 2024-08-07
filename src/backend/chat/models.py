from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from notebooks.models import NoteBook, NoteBookCell


class ChatMessage(models.Model):
    AUTHOR_TYPE_CHOICES = [
        (1, "User"),
        (2, "AI"),
    ]

    notebook = models.ForeignKey(NoteBook, on_delete=models.CASCADE)
    author_type = models.PositiveSmallIntegerField(choices=AUTHOR_TYPE_CHOICES)
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)

    cell = models.ForeignKey(
        NoteBookCell, blank=True, null=True, on_delete=models.SET_NULL
    )

    attached_image = models.ImageField(
        upload_to="messages/images/", null=True, blank=True
    )
    attached_file = models.FileField(upload_to="messages/files/", null=True, blank=True)

    def clean(self):
        if self.author_type != 2 and self.cell:
            raise ValidationError("Only messages generated by AI can have a cell attached to it")
