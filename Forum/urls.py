from django.urls import path

from .views import *

app_name = 'Forum'

urlpatterns = [
    path('', BlogHomeView.as_view(), name='forum'),
    path('blog/<slug>', BlogDetailView.as_view(), name='blog'),
    path('category/<name>', CategoryView.as_view(), name='category'),
    path('userqa', UserQAView.as_view(), name='userqa'),
    path('userqadetail', UserQaDetailView.as_view(), name='userqadetail'),
    path('askquestion', AskQuestionView, name='askquestion'),
    path('chat', index, name='chat'),
    path('<str:room_name>/', room, name='room'),
]
