# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    '''
    学生类, 存储其用户名和密码
    与User类为一对一关系
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "<Student: %s>" % (self.user.username)

class Category(models.Model):
    '''
    板块名称
    '''
    name = models.CharField(max_length=40, unique=True, verbose_name='版块名称')

    def __str__(self):
        return "<Category: %s>" % (self.name)



class Question(models.Model):
    '''
    问题类, 由外键与student连接
    有问题内容, 发布日期, 赞数, 踩数属性
    '''
    student = models.ForeignKey('Student', verbose_name='提问者',on_delete=models.CASCADE)
    question_title = models.CharField('问题标题', max_length=255, unique=True,blank=False)
    question_category = models.ForeignKey('Category', verbose_name='板块名称', on_delete=models.CASCADE,default=1)
    question_text = models.TextField('详细描述')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='发布日期')
    priority = models.IntegerField(default=1000, verbose_name='排序优先级')

    def __str__(self):
        return "<%s,author:%s>" % (self.question_title[:20],self.student.user.username)
class Answer(models.Model):
    '''
    回答类, 与Student和Question相连
    有回答内容, 发布日期
    '''
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.TextField(verbose_name='回答内容')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    # parent_answer_text 是关于多级评论的内容, 暂时未实现, 由周纸墨完成
    parent_answer_text = models.ForeignKey("self", related_name='p_answer_text', blank=True, null=True,
                                           on_delete=models.CASCADE)
    def __str__(self):
        return "<user: %s>" % (self.student)


# 点赞功能及显示暂未完成
class GoodNum(models.Model):
    '''
    点赞
    '''
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

class BadNum(models.Model):
    '''
    踩
    '''
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

