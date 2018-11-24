from django.contrib import admin

from .models import Student, Question, Answer, Category, GoodNum, BadNum


admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Answer)
admin.site.register(GoodNum)
admin.site.register(BadNum)
admin.site.register(Student)