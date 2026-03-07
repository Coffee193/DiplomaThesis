from django.urls import path
from . import views

urlpatterns = [
    path('getchats/', views.GetChats, name = 'GetChats'),
    path('createchat/', views.CreateChat, name = 'CreateChat'),
    path('deletechat/', views.DeleteChat, name = 'DeleteChat'),
    path('renamechat/', views.RenameChat, name = 'RenameChat'),
    path('getconversation/<int:conv_id>/', views.GetConversation, name = 'GetConversation'),
    path('askquestion/', views.AskQuestion, name='AskQuestion'),
    path('deleteallchats/', views.DeleteAllChats, name = 'DeleteAllChats'),
    path('resumestream/<int:conv_id>/', views.ResumeAnswerStream, name = 'ResumeAnswerStream'),

    path('slow/', views.Slow_Func_Test, name='Slow_Func_Test'),
]