from django.urls import path
from . import views

urlpatterns = [
    path('getchats/', views.getChats, name = 'getChats'),
    path('createchats/', views.createChats, name = 'createChats'),
    path('deletechats/', views.deleteChats, name = 'deleteChats'),
    path('renamechats/', views.renameChats, name = 'renameChats'),
    path('getchatconversation/<int:conv_id>/', views.getChatConv, name = 'getChatConv'),
    path('askquestion/', views.answearQuestion, name='answearQuestion'),
]