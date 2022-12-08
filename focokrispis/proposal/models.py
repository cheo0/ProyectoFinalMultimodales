from django.db import models
from django.conf import settings


# Create your models here.
class Proposal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')
    number_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title