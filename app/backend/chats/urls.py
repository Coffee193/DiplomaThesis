from django.urls import path
from . import views

urlpatterns = [
    path('getchats/', views.GetChats, name = 'GetChats'),
    path('createchats/', views.createChats, name = 'createChats'),
    path('deletechat/', views.DeleteChat, name = 'DeleteChat'),
    path('renamechat/', views.RenameChat, name = 'RenameChat'),
    path('getchatconversation/<int:conv_id>/', views.getChatConv, name = 'getChatConv'),
    path('askquestion/', views.answearQuestion, name='answearQuestion'),
    path('deleteallchats/', views.DeleteAllChats, name = 'DeleteAllChats'),
]