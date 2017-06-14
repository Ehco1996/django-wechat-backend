from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        '''
        返回最新的五个发布的投票问题的列表
        但是并不返回哪些被设置文以后将要发表的投票
        '''
        return Question.objects.filter(
            pub_date_lte=timezone.now()
        ).order_by('-pub_date')[:5]


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, pk):

    # 从数据库里获取符合id的question
    question = get_object_or_404(Question, pk=pk)

    try:
        # 尝试从表单的POST数据里选取符合的vote选项。
        selected_choice = question.choice_set.get(
            pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 返回一个detail列表，再次渲染一下detail的表单
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did't select a choice "
        })
    else:
        selected_choice.votes += 1
        # 当多个人同时提交的时候，可能会导致数据库里的值不同步 这个叫 race condition
        # DJango内置了一个数据库过滤函数可以方便的解决这个问题：
        # https://docs.djangoproject.com/en/1.10/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.save()
        # 不管成不成功，都发起一个重定向的请求 用来保存数据到数据库
        # 这样当用户不小心点了回退按键，也不会出现数据提交了两次。
        # 该请求指向了results函数
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
