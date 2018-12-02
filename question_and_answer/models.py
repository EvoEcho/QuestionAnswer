# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 用来保存上传用户头像信息的模型
class Profile(models.Model):
    # upload_to 表示图像保存路径
    picture = models.ImageField(upload_to = 'profile_pictures')
    class Meta:
        db_table = "profile"
    def __str__(self):
        return self.student.user.username

class Student(models.Model):
    '''
    学生类, 存储其用户名和密码
    与User类为一对一关系
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=20, default='', verbose_name='联系方式', blank=True,null=True)
    univ = models.CharField(max_length=20, default='上海交通大学', verbose_name='学校')
    major = models.CharField(max_length=20, default='---', verbose_name='专业')
    def __str__(self):
        return (self.user.username)

class Teacher(models.Model):
    '''
    老师类, 存储用户名和密码
    与User类一对一关系
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    univ = models.CharField(max_length=20, default='上海交通大学', verbose_name='学校')
    major = models.CharField(max_length=20, default='---', verbose_name='研究方向')
    def __str__(self):
        return (self.user.username)


class Category(models.Model):
    '''
    板块名称
    '''
    name = models.CharField(max_length=40, unique=True, verbose_name='版块名称')
    number = models.IntegerField(unique=True, verbose_name='板块序号')
    def __str__(self):
        return  (self.name)

class Question(models.Model):
    '''
    问题类, 由外键与student连接
    有问题内容, 发布日期, 赞数, 踩数属性
    '''
    user = models.ForeignKey(User, verbose_name='提问者', related_name='questions',on_delete=models.CASCADE)
    question_title = models.CharField('问题标题', max_length=40, unique=True,blank=False)
    question_category = models.ForeignKey('Category', verbose_name='板块名称', on_delete=models.CASCADE)
    question_text = models.TextField('详细描述')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='发布日期')
    good_num = models.IntegerField(default=0, verbose_name='赞数')
    bad_num = models.IntegerField(default=0, verbose_name='踩数')
    grade = models.IntegerField(default=0, verbose_name='综合质量')

    def __str__(self):
        return self.question_title

class Answer(models.Model):
    '''
    回答类, 与Student和Question相连
    有回答内容, 发布日期
    '''
    user = models.ForeignKey(User, related_name='answers', verbose_name='回答者',on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name='answers',on_delete=models.CASCADE)
    answer_text = models.TextField(verbose_name='回答内容')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    good_num = models.IntegerField(default=0)
    bad_num = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text
