from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.views.generic.edit import UpdateView, DeleteView
from .models import CustomUser, JournalEntry
from django.http import HttpResponseRedirect
from .forms import JournalEntryCreationForm



# Create your views here.

# Home Page View
class Home(TemplateView):
    template_name = 'home.html'

@login_required
def profile_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    journal_entries = JournalEntry.objects.filter(user=user)

    return render(request, 'profile.html', {'user': user, 'journal_entries':journal_entries})

@method_decorator(login_required, name='dispatch')
class Journal_Entry_View(FormView):
    model = JournalEntry
    form_class = JournalEntryCreationForm
    template_name = 'journal_entry_creation.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')
    
@method_decorator(login_required, name='dispatch')
class Journal_Update_View(UpdateView):
    model = JournalEntry
    form_class = JournalEntryCreationForm
    template_name = 'journal_entry_creation.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    success_url = '/'

@method_decorator(login_required, name='dispatch')
class Journal_Delete_View(DeleteView):
    model = JournalEntry
    template_name = 'journal_entry_delete.html'
    success_url = '/'