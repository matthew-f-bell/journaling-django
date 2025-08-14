from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import FormView, ListView
from django.views.generic.edit import UpdateView, DeleteView, FormMixin
from .models import CustomUser, JournalEntry, DailyGoals
from django.http import HttpResponseRedirect
from .forms import JournalEntryCreationForm, DailyGoalCreationForm, DailyGoalsChecklistForm



# Create your views here.

# Home Page View
class Home(TemplateView):
    template_name = 'home.html'

@login_required
def profile_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    journal_entries = JournalEntry.objects.filter(user=user)
    daily_goals = DailyGoals.objects.filter(user=user)

    return render(request, 'profile.html', {'user': user, 'journal_entries':journal_entries, 'daily_goals':daily_goals})

# Journal CRUD Views
@method_decorator(login_required, name='dispatch')
class Journal_Entry_View(FormView):
    model = JournalEntry
    form_class = JournalEntryCreationForm
    template_name = 'journal_entry_creation.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user = self.object.user.id
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user}))
    
@method_decorator(login_required, name='dispatch')
class Journal_Update_View(UpdateView):
    model = JournalEntry
    form_class = JournalEntryCreationForm
    template_name = 'journal_entry_creation.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user = self.object.user.id
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user}))


@method_decorator(login_required, name='dispatch')
class Journal_Delete_View(DeleteView):
    model = JournalEntry
    template_name = 'journal_entry_delete.html'
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user-profile', kwargs={'user_id':user_id})


# Daily Goals Crud    
@method_decorator(login_required, name='dispatch')
class Daily_Goals_Create_View(FormView):
    model = DailyGoals
    form_class = DailyGoalCreationForm
    template_name = 'daily_goals_creation.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user = self.object.user.id
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('daily-goals-checklist', kwargs={'user_id':user}))
    
@method_decorator(login_required, name='dispatch')
class Daily_Goals_Completed_View(FormView):
    model = DailyGoals
    form_class = DailyGoalsChecklistForm


    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        last_daily_goals = self.objects.filter(pk=pk-1)
        if (self.object.date_submitted - last_daily_goals.date_submitted) <= 1:
            self.object.consecutive_submissions =+ 1
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            user_id = self.object.user.id
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user_id}))


@method_decorator(login_required, name='dispatch')
class Daily_Goals_Checklist_View(FormView):
    model = DailyGoals
    template_name = 'daily_goals_checklist.html'
    form_class = DailyGoalsChecklistForm

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        daily_goals = DailyGoals.objects.filter(user=user_id)
        return {'daily_goals':daily_goals}

    def form_valid(self, form):
            
#        pk = self.objects.pk
#        last_daily_goals = self.objects.filter(pk=pk-1)
#        if (self.object.date_submitted - last_daily_goals.date_submitted) <= 1:
#            self.object.consecutive_submissions =+ 1
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            user_id = self.object.user.id
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user_id}))
#        else:
#            return HttpResponseRedirect(reverse_lazy('home'))
        

    
@method_decorator(login_required, name='dispatch')
class Daily_Goals_Delete_View(DeleteView):
    model = DailyGoals
    template_name = 'daily_goals_delete.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('daily-goals-checklist', kwargs={'user_id':user_id})
    
