from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# SECURITY FLAW: Broken Access Control
# - page that is designed to be visible for logged in users
#   can be accessed with direct URL
#
# FIX: add access control with the decorator below (remember to import it first):
# - use the login_required decorator below
# - use Django's built in authentication models in usermgmt/views.py
# @login_required(login_url='/login/')
def vip(request):
  return render(request, 'polls/vip.html')

# SECURITY FLAW I: Cross Site Request Forgery
# - the exempt decorator makes the website ignore CSRF token checks,
#   thus making it vulnerable to CSRF attacks
#
# FIX: remove the @csrf_exempt decorator
@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
