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
        return "Student: %s" % (self.user.username)

class Category(models.Model):
    '''
    板块名称
    '''
    name = models.CharField(max_length=40, unique=True, verbose_name='版块名称')
    number = models.IntegerField(default=0, verbose_name='板块序号')
    def __str__(self):
        return "Category: %s" % (self.name)

# 用来保存上传图片相关信息的模型
class Profile(models.Model):
    name = models.CharField(max_length = 50)
    # upload_to 表示图像保存路径
    picture = models.ImageField(upload_to = 'test_pictures')

    class Meta:
        db_table = "profile"

    def __str__(self):
        return self.name


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
    good_num = models.IntegerField(default=0)
    bad_num = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)
    def __str__(self):
        return "Title: %s, Asker:%s" % (self.question_title[:20],self.student.user.username)

class Answer(models.Model):
    '''
    回答类, 与Student和Question相连
    有回答内容, 发布日期
    '''
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.TextField(verbose_name='回答内容')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    head_img = models.ForeignKey('Profile', verbose_name='图片', on_delete=models.CASCADE)

    def __str__(self):
        return "Answerer: %s" % (self.student)
