# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from .models import *

def index(request):
    question_list1 = Question.objects.order_by('-pub_date')[:3]
    question_list2 = Question.objects.order_by('-grade')[:3]
    student_num = len(Student.objects.all())
    question_num = len(Question.objects.all())
    answer_num = len(Answer.objects.all())
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    context = {
        'username':username,
        'question_list1': question_list1,
        'question_list2': question_list2,
        'student_num': student_num,
        'question_num': question_num,
        'answer_num': answer_num,
        'is_logged_in': is_logged_in,
    }
    return render(request, 'question_and_answer/index.html', context)


def category(request):
    question_list = []
    for i in range(4):
        question_list.append(Question.objects.filter(question_category__number=i).order_by('-grade')[:6])
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    context = {
        'username': username,
        'question_list1': question_list[0],
        'question_list2': question_list[1],
        'question_list3': question_list[2],
        'question_list4': question_list[3],
        'is_logged_in': is_logged_in,
    }
    return render(request, 'question_and_answer/category.html', context)

def questions(request, category_id):
    return HttpResponseRedirect(reverse('question_and_answer:questionsOrder1', args={category_id,}))


def questionsOrder1(request, category_id):
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    question_list = Question.objects.filter(question_category__number=category_id).order_by('-pub_date')[:20]
    context = {
        'question_list':question_list,
        'category':Category.objects.get(number=category_id),
        'username': username,
        'is_logged_in': is_logged_in,
    }
    return render(request, 'question_and_answer/questionsOrder1.html', context)


def questionsOrder2(request, category_id):
    question_list = Question.objects.filter(question_category__number=category_id).order_by('-grade')[:20]
    context = {
        'question_list':question_list,
        'category':Category.objects.get(number=category_id),
    }
    return render(request, 'question_and_answer/questionsOrder2.html', context)

def detail(request, id):
    '''
    查看问题详细内容
    '''
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    question = get_object_or_404(Question, pk=id)
    context ={
        'username': username,
        'is_logged_in': is_logged_in,
        'question':question,

    }
    return render(request, 'question_and_answer/question_detail.html', context)

@login_required(login_url='/qa/login/')
def answer(request, question_id):
    '''
    回答问题
    '''
    question = get_object_or_404(Question, pk=question_id)
    try:
        answer_text = request.POST['answer']
    except KeyError:

        return render(request, 'question_and_answer/question_detail.html', {
            'question': question,
            'error_message': "Something wrong!",
        })
    else:
        user = User.objects.get(id=request.session.get('user_id'))
        answer = Answer(
            student=user.student,
            question=question,
            answer_text=answer_text,
            pub_date=timezone.now(),
        )
        answer.save()

        return HttpResponseRedirect(reverse('question_and_answer:detail', args=(question.id,)))

'''
@login_required() 是一个装饰器, 要求必须登录后才能查看, 跳转至登录界面
'''
@login_required(login_url='/qa/login/')
def ask(request):
    return render(request, 'question_and_answer/ask.html')
# '''
#     if request.method == 'POST':
#         user_id = request.session.get('user_id')
#         user = User.objects.get(id=user_id)
#         if user:
#             student = user.student
#         else:
#             return HttpResponseRedirect(reverse('question_and_answer:index'), args={1,})
#         try:
#             question_title = request.POST['title']
#             question_category_name = request.POST['category']
#             question_text = request.POST['question']
#             #new_img_path = handle_uploaded_file(request.FILES['head_img'])
#             #head_img = new_img_path
#             question_category = Category.objects.get(name=question_category_name)
#             # for e in Category.objects.all():
#             #     if e.name == question_category_name:
#             #         question_category = e
#             # 接收 post 方法传回后端的数据
#             MyProfileForm = ProfileForm(request.POST, request.FILES)
#             # 检验表单是否通过校验
#             if MyProfileForm.is_valid():
#                 # 构造一个 Profile 实例
#                 profile = Profile()
#                 # 获取name
#                 profile.name = MyProfileForm.cleaned_data["name"]
#                 # 获取图片
#                 profile.picture = MyProfileForm.cleaned_data["picture"]
#                 # 保存
#                 profile.save()
#                 head_img = profile
#             else:
#                 return render(request, 'question_and_answer/ask.html', {
#                     'error_message': "Something wrong!",
#                 })
#         except KeyError:
#             error_message = "Something wrong!"
#             return render(request, 'question_and_answer/ask.html', {
#                 'error_message': "Something wrong!",
#             })
#         else:
#             question = Question(
#                 student=student,
#                 question_title=question_title,
#                 question_category=question_category,
#                 question_text=question_text,
#                 head_img=profile
#             )
#             question.save()
#             return HttpResponseRedirect(reverse('question_and_answer:detail', args=(question.id,)))
#     return render(request, 'question_and_answer/ask.html', {})
#

def register(request):
    form1 = LoginForm()
    form2 = RegistrationForm()
    context = {
        'loginForm': form1,
        'registrationForm': form2,
    }
    if request.method == 'POST':
        form2 = RegistrationForm(request.POST)
        if form2.is_valid():
            username = form2.cleaned_data['username']
            email = form2.cleaned_data['email']
            password = form2.cleaned_data['password2']

            user = User.objects.create_user(username=username, email=email, password=password)
            student = Student(user=user)
            student.save()
            return HttpResponseRedirect(reverse('question_and_answer:login'))
        else:

            return render(request, 'question_and_answer/login_register.html', context)


    else:
        return render(request, 'question_and_answer/login_register.html',context)


def login(request):
    form1 = LoginForm()
    form2 = RegistrationForm()
    context = {
        'loginForm': form1,
        'registrationForm': form2,
    }
    if request.method == 'POST':
        form1 = LoginForm(request.POST)
        if form1.is_valid:
            username = LoginForm.cleaned_username['username']
            password = LoginForm.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('question_and_answer:index'))
            else:
                context['loginMessage'] = "密码或用户名错误, 请重试"
                return render(request, 'question_and_answer/login_register.html', context)
        else:
            context['loginMessage'] = "密码或用户名错误, 请重试"
            return render(request, 'question_and_answer/login_register.html', context)


    else:
        return render(request, 'question_and_answer/login_register.html', context)


@login_required(login_url='qa/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('question_and_answer:index'))

def about(request):
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    context = {
        'username': username,
        'is_logged_in': is_logged_in,
    }
    return render(request, 'question_and_answer/about.html', context)

@login_required(login_url='qa/login/')
def profile(request):
    return render(request, 'question_and_answer/profile.html')

@login_required(login_url='qa/login/')
def notice(request):
    return render(request, 'question_and_answer/notice.html')

@login_required(login_url='qa/login/')
def myquestions(request):
    return render(request, 'question_and_answer/myquestions.html')

@login_required(login_url='qa/login/')
def modification(request):
    return render(request, 'question_and_answer/modification.html')

