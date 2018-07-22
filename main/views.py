from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from main.models import Question, Choice


def detail(request, question_id):
    q = Question.objects.get(id=question_id)
    context = {'question': q}
    return render(request, 'main/detail.html', context)

def results(request, question_id):

    field = request.GET.get('field', '')
    xxx = request.GET.get('xxx', '')

    response = "You're looking at the results of question %s. %s - %s"
    return HttpResponse(response % (question_id, field, xxx))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'main/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list , 'some_var': 343}
    return render(request, 'main/index.html', context)