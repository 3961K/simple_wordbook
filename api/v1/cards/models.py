from django.contrib.auth import get_user_model
from django.db import models
import uuid

from ..wordbooks.models import Wordbook

User = get_user_model()


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=100)
    answer = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True, editable=False)
    is_hidden = models.BooleanField(default=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='cards')
    wordbooks = models.ManyToManyField(Wordbook,
                                       related_name='cards')

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return '{}:{}'.format(self.word, self.answer)
