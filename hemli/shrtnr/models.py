from django.contrib.sessions.models import Session
from django.db import models


class ShortLink(models.Model):
    url = models.URLField(verbose_name="Длинный URL")
    path = models.CharField(max_length=10, unique=True, blank=True, verbose_name="Желаемое сокращение")
    created_at = models.DateTimeField(auto_now_add=True)
    num_views = models.IntegerField(default=0)

    sessions = models.ManyToManyField(Session, related_name='short_links')

    def __str__(self):
        return self.path


# class UserLink(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='short_links')
#     link = models.ForeignKey(ShortLink, on_delete=models.CASCADE)
    
