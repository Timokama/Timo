from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Person, Group,Membership

class IndexView(generic.ListView):
    template_name = 'fetha/index.html'
    context_object_name = 'latest_person_list'

    def get_queryset(self):
        """Return the last five published players."""
        return Membership.objects.filter(
            date_joined__lte=timezone.now()
        ).order_by('id')[:5]

class DetailView(generic.DetailView):
    model = Person
    template_name = 'fetha/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Membership.objects.filter(date_joined__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Person
    template_name = 'fetha/results.html'

def vote(request, person_id):
    person = get_object_or_404(Group, pk=person_id)
    try:
        selected_group = person.choice_set.get(pk=request.POST['group'])
    except (KeyError, Group.DoesnotExist):
        #Redisplay the question voting form.
        return render(request, 'fetha/detail.html',{
            'person': person,
            'error_message':"you didn't select a person name",
        })
    else:
        selected_group.votes += 1
        selected_group.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('fetha:results', args=(person.id,)))