import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


# Create your tests here.


class QuestionMethodTests(TestCase):

    def test_was_publishend_recently_with_future_question(self):
        '''
        测试 was_published_recently()函数应该返回false
        当问题是将来推出的时候
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        futrue_question = Question(pub_date=time)
        self.assertIs(futrue_question.was_published_recently(), False)

    def test_was_publishend_recently_with_old_question(self):
        '''
        测试was_published_recently()函数是否返回一个False 当发pub_date
        超过一天的情况下
        '''
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_publishend_recently_with_recent_question(self):
        '''
        测试was_published_recently()函数是否返回一个True 当发pub_date
        不超过一天的情况下
        '''
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
