from django.db import models

# Create your models here.
class Question(models.Model):
    """
    ・max_lengthはCharFieldを使用する際必須
    ・第一引数で人間に分かりやすい名前を設定
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
class Choice(models.Model):
    """
    ForeignKeyによるリレーションの設定
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

