from django.contrib import admin

from .models import Student, Question, Answer

admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Answer)
