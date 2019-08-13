from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #эта модель создана по умолчанию, её создавать не нужно
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #наши посты должны иметь автора, и если автор удаляется то и пост тоже

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

