# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from .models import Student, Question, Answer

def index(request, page=1):
    # 暂时只有按时间倒序排列, 将有分页器及排序功能
    question_list = Question.objects.order_by('-pub_date')[(page-1):(page+20)]
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        username = user.username
    else:
        username = '未登录'
    context = {
        'username':username,
        'question_list': question_list,
    }
    return render(request, 'question_and_answer/index.html', context)

def detail(request, pk):
    '''
    查看问题详细内容
    '''
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_and_answer/detail.html', {'question': question})

def answer(request, pk):
    '''
    回答问题
    '''
    question = get_object_or_404(Question, pk=pk)
    try:
        answer_text = request.POST['answer']
    except KeyError:

        return render(request, 'question_and_answer/detail.html', {
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
def newQuestion(request):
    '''
    用户提问
    '''
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if user:
            student = user.student
        else:
            return HttpResponseRedirect(reverse('question_and_answer:index'), args={1,})
        try:
            question_title = request.POST['title']
            question_text = request.POST['question']
        except KeyError:
            error_message = "Something wrong!"
            return render(request, 'question_and_answer/newQuestion.html', {
                'error_message': "Something wrong!",
            })
        else:
            question = Question(
                student=student,
                question_title=question_title,
                question_text=question_text,
            )
            question.save()
            return HttpResponseRedirect(reverse('question_and_answer:detail', args=(question.id,)))
    return render(request, 'question_and_answer/newQuestion.html', {})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create_user(username=username, email=email, password=password)
            student = Student(user=user)
            student.save()
            return HttpResponseRedirect(reverse('question_and_answer:login'))
    else:
        form = RegistrationForm()
    return render(request, 'question_and_answer/register.html',{'form':form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                request.session['user_id'] = user.id
                request.session['is_login'] = True
                return HttpResponseRedirect(reverse('question_and_answer:index', args={1,}))
            else:
                return render(request, 'question_and_answer/login.html', {'form':form, 'message': "密码或用户名错误, 请重试"})

    else:
        form = LoginForm()

    return render(request, 'question_and_answer/login.html', {'form': form})

def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
    return HttpResponseRedirect(reverse('question_and_answer:login'))

