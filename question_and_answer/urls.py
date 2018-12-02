from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'question_and_answer'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.category, name='category'),
    path('questions/<int:category_id>', views.questions, name='questions'),
    path('questionsOrder1/<int:category_id>/',views.questionsOrder1, name='questionsOrder1'),
    path('questionsOrder2/<int:category_id>/',views.questionsOrder2, name='questionsOrder2'),
    path('questions/detail/<int:id>/', views.detail, name='detail'),
    path('questions/like/<int:id>/<str:type>/', views.like, name='like'),
    path('questions/unlike/<int:id>/<str:type>/', views.unlike, name='unlike'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('about/',views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('myquestions/', views.myquestions, name='myquestions'),
    path('modification/',views.modification, name='modification'),
    path('notice/', views.notice, name='notice'),
]