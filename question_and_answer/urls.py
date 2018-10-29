from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'question_and_answer'
urlpatterns = [

    path('<int:page>/', views.index, name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/answer/', views.answer, name='answer'),
    path('newQuestion/', views.newQuestion, name='newQuestion'),
    path('newQuestion/submit/', views.newQuestionSubmit, name='newQuestionSubmit'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]