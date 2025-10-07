from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.handleLogin, name = 'handleLogin'),
    path('finduser/', views.findUser, name = 'findUser'),
    path('register/', views.handleRegister, name = 'handleRegister'),
    path('create_referal/', views.CreateReferalCode, name = 'createReferalCode'),
    path('logout/', views.Logout, name = 'Logout'),
    path('getuserinfo/', views.GetUserInfo, name = 'GetUserInfo'),
    path('updatevalue/', views.UpdateValue, name = 'UpdateValue'),
    path('updateimage/', views.UpdateImg, name = 'UpdateImage'),
    path('getuserimg/', views.GetUserImg, name = 'GetUserImg'),
    path('testdelete/', views.TestDelete, name = 'TestDelete'),
    path('deleteaccount/', views.DeleteUser, name = 'DeleteUser'),
]