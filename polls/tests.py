import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_publised_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
        seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    テスト用データを作成するショートカット関数
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        データが1件もない場合の表示を確認する
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_past_question(self):
        """
        indexページに過去日付のデータが表示されることを確認する
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
        
    def test_future_question(self):
        """
        indexページに未来日付のデータが表示されないことを確認する
        """
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_question_and_past_question(self):
        """
        過去日付と未来日付両方のデータが存在する場合に、過去日付のデータのみ
        表示されることを確認する
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    
    def test_two_past_questions(self):
        """
        複数データが表示されることを確認する
        """
        create_question(question_text="Past question_1.", days=-30)
        create_question(question_text="Past question_2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
        ['<Question: Past question_1.>','<Question: Past question_2.>']
        )


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        公開日が未来日のデータを表示しようとした場合に404エラーになる
        ことを確認する
        """
        future_question = create_question(question_text='Future question.',days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        公開日が到来しているデータが表示されることを確認する
        """
        past_question = create_question(question_text='Past question.',days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        









