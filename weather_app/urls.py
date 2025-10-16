from django.urls import path
from . import views

app_name = 'weather_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('stats/', views.stats_view, name='stats'),
    path('weekly/', views.weekly_weather, name='weekly_weather'),
    path('monthly/', views.monthly_weather, name='monthly_weather'),
    path('api/weather/', views.weather_api, name='weather_api'),
    
]
