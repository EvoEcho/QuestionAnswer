from django.contrib import admin
from .models import *
#from .models import Student, Question, Answer, Category

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','student','pub_date','question_category_name')
    list_filter = ['id','student','pub_date','question_category__name']
    search_fields = ['student__user__username']
    list_per_page = 10

    def question_category_name(self, obj):
        return '%s' % obj.question_category.name

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id','student','question','pub_date')
    list_filter = ['id','student','question','pub_date']
    search_fields = ['student__user__username']
    list_per_page = 10

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','__str__')
    search_fields = ['user__username']
    list_per_page = 10


admin.site.register(Question,QuestionAdmin)
admin.site.register(Category)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Profile)