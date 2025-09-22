from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.views.generic.edit import UpdateView, DeleteView, FormMixin
from .models import CustomUser, JournalEntry, DailyGoals, HydrationTracker
from django.http import HttpResponseRedirect
from .forms import CustomUserForm, JournalEntryCreationForm, DailyGoalCreationForm, DailyGoalsChecklistForm, HydrationTrackerForm, DailyGoalsUpdateFormset



# User Profile CRUD
@method_decorator(login_required, name='dispatch')
class Profile_Update_View(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'user_update.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user = self.object.user.id
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user}))
    
class Profile_Delete_View(DeleteView):
    model = CustomUser
    template_name = 'user_delete.html'
    success_url = ''


# Home Page View
class Home(TemplateView):
    template_name = 'home.html'

@method_decorator(login_required, name='dispatch')
class Profile_View(TemplateView, FormMixin):
    model = CustomUser
    form_class = HydrationTrackerForm
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        get_datetime = timezone.localtime()
        get_date = get_datetime.date()

        if HydrationTracker.objects.filter(user=user).exists() == False:
            one_year_of_hydration_null = get_date - timedelta(days=365)
            while one_year_of_hydration_null <= get_date:
                HydrationTracker.objects.create(user=self.request.user, date_of_intake=one_year_of_hydration_null, water_intake=0)
                one_year_of_hydration_null = one_year_of_hydration_null + timedelta(days=1)
        elif HydrationTracker.objects.filter(user=user).latest('date_of_intake').date_of_intake + timedelta(days=1) < get_date:
            hydration_catch_up = HydrationTracker.objects.filter(user=user).latest('date_of_intake').date_of_intake
            while hydration_catch_up < get_date:
                HydrationTracker.objects.create(user=self.request.user, date_of_intake=hydration_catch_up, water_intake=0)
                hydration_catch_up = hydration_catch_up + timedelta(days=1)
        elif HydrationTracker.objects.filter(user=user).filter(date_of_intake=get_date).exists() == False:
                HydrationTracker.objects.create(user=self.request.user, date_of_intake=get_date, water_intake=0)
        else:
            print("Did nothing")

        context['journal_entries'] = JournalEntry.objects.filter(user=user)
        context['daily_goals'] = DailyGoals.objects.filter(user=user)
        context['hydration_trackers'] = HydrationTracker.objects.filter(user=user)
        context['hydration_form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        form = HydrationTrackerForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user_id = self.object.user.id
        intake_of_water = self.request.POST.getlist("water_intake")
        get_datetime = timezone.localtime()
        get_date = get_datetime.date()
        if '8' in intake_of_water:
            hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
            hydration_day.water_intake = hydration_day.water_intake + int(intake_of_water[0])
            hydration_day.save()
        elif '16' in intake_of_water:
            hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
            hydration_day.water_intake = hydration_day.water_intake + int(intake_of_water[0])
            hydration_day.save()
        elif '32' in intake_of_water:
            hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
            hydration_day.water_intake = hydration_day.water_intake + int(intake_of_water[0])
            hydration_day.save()
        else:
            hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
            print("*_*_*_*_*_*_*_* Not a valid submission!!!!!! *_*_*_*_*_*_*_*")
            print(hydration_day)
        return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user_id}))
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user-profile', kwargs={'user_id':user_id})


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
class Daily_Goals_Checklist_View(FormView):
    model = DailyGoals
    template_name = 'daily_goals_checklist.html'
    form_class = DailyGoalsChecklistForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user_id = self.object.user.id
        update_goals_id = self.request.POST.getlist("completed_daily_goals")
        get_datetime = timezone.localtime()
        get_date = get_datetime.date()
        if 'save_button' in self.request.POST:
            for goal in update_goals_id:
                goal_edit = DailyGoals.objects.get(id=goal)
                date_check = goal_edit.date_submitted
                next_day = date_check + timedelta(days=1)
                if (next_day-get_date == timedelta(days=0)):
                    submission_increase = goal_edit.consecutive_submissions
                    goal_edit.consecutive_submissions = submission_increase + 1
                    goal_edit.submissions_total = goal_edit.submissions_total + 1
                    goal_edit.date_submitted = get_date
                    goal_edit.save()
                elif(next_day-get_date < timedelta(days=0)):
                    goal_edit.consecutive_submissions = 1
                    goal_edit.submissions_total = goal_edit.submissions_total + 1
                    goal_edit.date_submitted = get_date
                    goal_edit.save()
                else:
                    print("Did nothing for " + goal)
            return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user_id}))
        elif 'delete_button' in self.request.POST:
            DailyGoals.objects.filter(pk__in=update_goals_id).delete()
            return HttpResponseRedirect(reverse_lazy('user-profile', kwargs={'user_id':user_id}))
        
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user-profile', kwargs={'user_id':user_id})

@method_decorator(login_required, name='dispatch')
class Daily_Goals_Delete_View(DeleteView):
    model = DailyGoals
    template_name = 'daily_goals_delete.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('daily-goals-checklist', kwargs={'user_id':user_id})

@method_decorator(login_required, name='dispatch')
class Daily_Goals_Update_View(FormView):
    model = DailyGoals
    fields = ['title']
    form_class = DailyGoalsUpdateFormset
    template_name = 'daily_goals_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = DailyGoals.objects.filter(user=user)
        context['daily_goal_formset'] = DailyGoalsUpdateFormset(queryset=queryset)
        return context

    def post(self, request, *args,**kwargs):
        user = self.request.user
        queryset = DailyGoals.objects.filter(user=user)
        formset = DailyGoalsUpdateFormset(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)
    
    def form_valid(self, formset):
        return super().form_valid(formset)
    
    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('daily-goals-checklist', kwargs={'user_id':user_id})
