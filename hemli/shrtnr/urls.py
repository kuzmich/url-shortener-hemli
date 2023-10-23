from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<path:short_path>', views.redirect_to_full, name='redirect'),
]
