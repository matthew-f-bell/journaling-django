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
from .forms import JournalEntryCreationForm, DailyGoalCreationForm, DailyGoalsChecklistForm, HydrationTrackerForm, DailyGoalsUpdateFormset




# Create your views here.

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
        get_datetime = timezone.now()
        get_date = get_datetime.date()
        print("get_date = " + str(get_date))
        print("my intake of water is " + str(int(intake_of_water[0])))
        exist_check = HydrationTracker.objects.filter(date_of_intake=get_date).exists()
        print("I do exist "+ str(exist_check))
        if '8' in intake_of_water:
            if exist_check == False:
                HydrationTracker.objects.create(user=self.object.user, date_of_intake=get_date)
                hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
                print(str(hydration_day.date_of_intake) + " has " + str(hydration_day.water_intake) + " to be filled with " + " has been selected for 8 oz")
                hydration_day.water_intake = hydration_day.water_intake + int(intake_of_water[0])
                hydration_day.save()
            else:
                hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
                old_water = hydration_day.water_intake
                print(str(hydration_day.date_of_intake) + " has " + str(old_water) + " to be filled with " + " has been selected for 8 oz")
                hydration_day.water_intake = old_water + int(intake_of_water[0])
                hydration_day.save()
        elif '16' in intake_of_water:
            hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
            hydration_day.water_intake = hydration_day.water_intake + intake_of_water
            print(hydration_day + " has been selected for 16 oz")
        elif '32' in intake_of_water:
            hydration_day = HydrationTracker.objects.get(date_of_intake=get_date)
            hydration_day.water_intake = hydration_day.water_intake + intake_of_water
            print(hydration_day + " has been selected for 32 oz")
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
        print(update_goals_id)
        get_datetime = timezone.now()
        get_date = get_datetime.date()
        print("get_date = " + str(get_date))
        if 'save_button' in self.request.POST:
            for goal in update_goals_id:
                goal_edit = DailyGoals.objects.get(id=goal)
                date_check = goal_edit.date_submitted
                next_day = date_check + timedelta(days=1)
                print(str(next_day))
                print("difference of dates = " + str(next_day-get_date))
                if (next_day-get_date == timedelta(days=0)):
                    print(str(date_check))
                    submission_increase = goal_edit.consecutive_submissions
                    goal_edit.consecutive_submissions = submission_increase + 1
                    goal_edit.submissions_total = goal_edit.submissions_total + 1
                    goal_edit.date_submitted = get_date
                    print("consecutive " + goal)
                    goal_edit.save()
                elif(next_day-get_date < timedelta(days=0)):
                    print(str(date_check))
                    goal_edit.consecutive_submissions = 1
                    goal_edit.submissions_total = goal_edit.submissions_total + 1
                    goal_edit.date_submitted = get_date
                    print("non-consecutive " + goal)
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
