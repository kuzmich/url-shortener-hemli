from django.contrib.sessions.models import Session
from django.db import models


class ShortLink(models.Model):
    url = models.URLField(verbose_name="Длинная ссылка")
    path = models.CharField(max_length=10, unique=True, blank=True, verbose_name="Желаемое сокращение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    num_views = models.IntegerField(default=0, verbose_name="Переходы")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='short_links')

    def __str__(self):
        return self.path
    
