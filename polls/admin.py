from django.contrib import admin

# Register your models here.
from .models import Question, Choice

"""admin.site.register(Question)
"""

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date information', {'fields':['pub_date'], 'classes':['collapse']})
    ]
    inlines = [ChoiceInline]

"""
モデルのadminオプションを変更したい場合は、モデル毎にadminクラスを作成し、
registerの第2引数として渡す
"""
admin.site.register(Question, QuestionAdmin)