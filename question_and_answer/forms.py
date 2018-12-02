from django import forms
from django.contrib.auth.models import User
from .models import Question
import re

# 此文件是登录及注册的表单, 放在一起便于管理
# 以及还有对输入合法性检验的函数

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50,widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'input'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'input'}))
    identity = forms.ChoiceField(label='Identity', choices=[('student','Student'),('teacher', 'Teacher')], required=True, widget=forms.RadioSelect(attrs={'id':'identity', 'class':'select'}))

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 2:
            raise forms.ValidationError("Your username must be at least 2 characters long.")
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your email already exists.")
        else:
            raise forms.ValidationError("Please enter a valid email.")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")

        return password2


class LoginForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={"id":"username","class":"input"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"id":"password","class":"input"}))
    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("This email does not exist.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                        raise forms.ValidationError("This username does not exist. Please register first.")

        return username


class AskForm(forms.Form):
    category = forms.ChoiceField(label='请选择问题种类', choices=[(0,'物理'),(1,'数学'),(2,'语言'),(3,'金融')], required=True,
                                 widget=forms.RadioSelect)
    title = forms.CharField(label='请输入问题题目(60字以内):', max_length=60,required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    question = forms.CharField(label='请输入问题内容(2000字以内):', max_length=2000, required=True,widget=forms.Textarea(attrs={"class":"form-control"}))

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if int(category) < 0 or int(category) > 3:
            raise forms.ValidationError("你选择的模块不存在")
        return category

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 3:
            raise forms.ValidationError("Your title must be at least 3 characters long.")
        elif len(title) > 60:
            raise forms.ValidationError("Your title is too long.")
        else:
            filter_result = Question.objects.filter(question_title__exact=title)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your title already exists.")
        return title

    def clean_question(self):
        question = self.cleaned_data.get('question')

        if len(question) < 3:
            raise forms.ValidationError("Your text must be at least 3 characters long.")
        elif len(question) > 2000:
            raise forms.ValidationError("Your text is too long.")
        else:
            return question

class AnswerForm(forms.Form):
    answer = forms.CharField(label='answer', max_length=2000, widget=forms.Textarea(attrs={'name':"answer", 'class':"form-control",'rows':"10"}))

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')

        if len(answer) < 3:
            raise forms.ValidationError("Your answer must be at least 3 characters long.")
        elif len(answer) > 2000:
            raise forms.ValidationError("Your answer is too long.")
        else:
            return answer

class ProfileForm(forms.Form):
    name = forms.CharField(max_length = 100, label='名字：')
    picture = forms.ImageField(label='图片：')

