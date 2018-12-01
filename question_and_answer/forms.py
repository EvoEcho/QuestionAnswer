from django import forms
from django.contrib.auth.models import User
import re

# 此文件是登录及注册的表单, 放在一起便于管理
# 以及还有对输入合法性检验的函数

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50,widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class':'input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'input'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'input'}))

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.ValidationError("Your username must be at least 6 characters long.")
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


class ProfileForm(forms.Form):
    name = forms.CharField(max_length = 100, label='名字：')
    picture = forms.ImageField(label='图片：')