from django.urls import path
from GET_API import views

urlpatterns = [
    path('', views.handle_get, name = 'Tmax')
]
