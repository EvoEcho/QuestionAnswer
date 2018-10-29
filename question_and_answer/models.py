# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class Student(models.Model):
    '''
    学生类, 存储其用户名和密码
    '''
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Question(models.Model):
    '''
    问题类, 由外键与student连接
    有问题内容, 发布日期, 赞数, 踩数属性
    '''
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    question_title = models.CharField(max_length=40)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published', default=timezone.now())
    good_num = models.IntegerField(default=0)
    bad_num = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text[:20]

class Answer(models.Model):
    '''
    回答类, 与Student和Question相连
    有回答内容, 发布日期, 赞数, 踩数
    '''
    student = models.ForeignKey('Student', default='user', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published', default=timezone.now())
    good_num = models.IntegerField(default=0)
    bad_num = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text[:20]


