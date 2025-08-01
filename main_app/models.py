from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



# Create your models here.
class CustomUser(AbstractUser):
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class JournalEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    journal_content = models.CharField(max_length=100000)
    date_created = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['journal-content', 'user', 'date_created']

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']