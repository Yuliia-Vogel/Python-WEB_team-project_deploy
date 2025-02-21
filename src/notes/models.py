from django.db import models
<<<<<<< Updated upstream
=======
from django.contrib.auth import get_user_model

User = get_user_model()
>>>>>>> Stashed changes

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Note(models.Model):
<<<<<<< Updated upstream
    title = models.CharField(max_length=255)
=======
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
>>>>>>> Stashed changes
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
