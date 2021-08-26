from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()


class Wordbook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wordbook_name = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now=True, editable=False)
    is_hidden = models.BooleanField(default=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='wordbooks')

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.wordbook_name
