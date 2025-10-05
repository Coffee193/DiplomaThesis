from django.urls import path
from . import views

urlpatterns = [
    path('createreferal/', views.CreateReferal, name = 'CreateReferal'),
    path('getallreferals/', views.GetAllReferals, name = 'GetAllReferals'),
]