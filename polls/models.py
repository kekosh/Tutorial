from django.db import models

#カスタムメソッド用
import datetime
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    """
    ・max_lengthはCharFieldを使用する際必須
    ・第一引数で人間に分かりやすい名前を設定
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    #オブジェクトを参照した時の表記を指定
    def __str__(self):
        return self.question_text
        
    #カスタムメソッド
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Choice(models.Model):
    """
    ForeignKeyによるリレーションの設定
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    #オブジェクトを参照した時の表記を指定
    def __str__(self):
        return self.choice_text


    

