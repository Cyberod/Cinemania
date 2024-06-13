from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.detail, name='detail'),
]