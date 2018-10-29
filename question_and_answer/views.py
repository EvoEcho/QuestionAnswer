# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Student, Question, Answer

def index(request, page):
    #return HttpResponse(str(page))
    question_list = Question.objects.order_by('-pub_date')[(page-1):(page+20)]
    user = 'hello'
    context = {
        'user':user,
        'question_list': question_list,
    }
    return render(request, 'question_and_answer/index.html', context)

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_and_answer/detail.html', {'question': question})

def answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        answer_text = request.POST['answer']
    except KeyError:

        return render(request, 'question_and_answer/detail.html', {
            'question': question,
            'error_message': "Something wrong!",
        })
    else:
        answer = Answer(
            student=Student.objects.get(id=1),
            question=question,
            answer_text=answer_text,
            pub_date=timezone.now(),
        )
        answer.save()

        return HttpResponseRedirect(reverse('question_and_answer:detail', args=(question.id,)))

def newQuestion(request):
    return render(request, 'question_and_answer/newQuestion.html', {})

def newQuestionSubmit(request):
    student = Student.objects.get(id=1)
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
    


def login(request):
    return HttpResponse("登录成功!")

def register(request):
    return HttpResponse("注册成功!")
