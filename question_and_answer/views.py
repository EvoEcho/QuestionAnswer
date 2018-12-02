# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, AskForm, AnswerForm, ProfileForm
from .models import *

def index(request):
    try:
        question_list1 = Question.objects.order_by('-pub_date')[:3]
        question_list2 = Question.objects.order_by('-grade')[:3]
        student_num = len(Student.objects.all())
        teacher_num = len(Teacher.objects.all())
        question_num = len(Question.objects.all())
        answer_num = len(Answer.objects.all())
    except:
        question_list1 = []
        question_list2 =[]
        student_num = 0
        teacher_num = 0
        question_num = 0
        answer_num = 0
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
        'teacher_num': teacher_num,
        'answer_num': answer_num,
        'is_logged_in': is_logged_in,
    }
    return render(request, 'question_and_answer/index.html', context)


def category(request):
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    try:
        question_list = []
        for i in range(4):
            question_list.append(Question.objects.filter(question_category__number=i).order_by('-grade')[:6])
        context = {
            'username': username,
            'question_list1': question_list[0],
            'question_list2': question_list[1],
            'question_list3': question_list[2],
            'question_list4': question_list[3],
            'is_logged_in': is_logged_in,
        }
    except:
        context = {
            'username': username,
            'question_list1': [],
            'question_list2': [],
            'question_list3': [],
            'question_list4': [],
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
    if request.method == 'POST':
        answer(request, id)
    form = AnswerForm()
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True


    else:
        username = '未登录'
        is_logged_in = False
    question = get_object_or_404(Question, pk=id)
    context['form'] = form
    context['username'] = username
    context['is_logged_in'] = is_logged_in
    context['question'] = question
    return render(request, 'question_and_answer/question_detail.html', context)

'''
@login_required() 是一个装饰器, 要求必须登录后才能查看, 跳转至登录界面
'''

@login_required(login_url='/qa/login/')
def like(request, id, type):
    if type == 'question':
        question = Question.objects.get(id=id)
        question.good_num += 1
        question.grade = question.grade + 10
        question.save()
        return HttpResponseRedirect(reverse('question_and_answer:detail', args=(id,)))
    else:
        answer = Answer.objects.get(id=id)
        answer.good_num += 1
        answer.save()
        return HttpResponseRedirect(reverse('question_and_answer:detail', args=(answer.question.id,)))

@login_required(login_url='/qa/login/')
def unlike(request, id, type):
    if type == 'question':
        question = Question.objects.get(id=id)
        question.bad_num += 1
        question.grade = question.grade - 7
        question.save()
        return HttpResponseRedirect(reverse('question_and_answer:detail', args=(id,)))
    else:
        answer = Answer.objects.get(id=id)
        answer.bad_num += 1
        answer.save()
        return HttpResponseRedirect(reverse('question_and_answer:detail', args=(answer.question.id,)))


@login_required(login_url='/qa/login/')
def answer(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user:
            pass
        else:
            return HttpResponseRedirect(reverse('question_and_answer:detail',  args={id, }))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['answer']
            answer = Answer(
                user = user,
                question = question,
                answer_text = answer_text,
            )
            answer.save()
            return HttpResponseRedirect(reverse('question_and_answer:detail', args={id, }))
    return HttpResponseRedirect(reverse('question_and_answer:detail', args={id, }) )


@login_required(login_url='/qa/login/')
def ask(request):
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
    if request.method == 'POST':
        id = request.user.id
        user = User.objects.get(id=id)
        if user:
            pass
        else:
            return HttpResponseRedirect(reverse('question_and_answer:index'))
        form = AskForm(request.POST)
        if form.is_valid():
            question_category_number = form.cleaned_data['category']
            question_title = form.cleaned_data['title']
            question_text = form.cleaned_data['question']
            question_category = Category.objects.get(number=question_category_number)
            question = Question(
                user=user,
                question_title=question_title,
                question_category=question_category,
                question_text=question_text,
            )
            question.save()
            return render(request, 'question_and_answer/ask2.html', {})
        else:
            context['askMessage'] = "您的输入含有非法字符, 请重试!"
            return
    else:
        form = AskForm()
        context['form'] = form
    return render(request, 'question_and_answer/ask.html', context)

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
            identity = form2.identity
            user = User.objects.create_user(username=username, email=email, password=password)
            if identity == 'student':
                student = Student(user=user)
                student.save()
            else:
                teacher = Teacher(user=user)
                teacher.save()
            context['loginMessage'] = "注册成功! 请登录"
            return render(request, 'question_and_answer/login_register.html', context)
        else:
            context['registerMessage'] = "表单无效, 请重新提交"
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
        if form1.is_valid():
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']

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
    request.session.flush()
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

