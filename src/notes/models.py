from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Прив'язка до користувача
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title