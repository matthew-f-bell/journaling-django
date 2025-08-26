from django import forms
from django.forms import modelformset_factory
from .models import JournalEntry, DailyGoals
from django.utils import timezone


class JournalEntryCreationForm(forms.ModelForm):
    get_datetime = timezone.now()
    current_date = get_datetime.date()

    title = forms.CharField(max_length=100, initial=current_date)
    journal_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = JournalEntry
        fields = ['title', 'journal_content']

class DailyGoalCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100)

    class Meta:
        model = DailyGoals
        fields = ['title']

class DailyGoalsChecklistForm(forms.ModelForm):
    completed_daily_goals = forms.ModelMultipleChoiceField(
        queryset=DailyGoals.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = DailyGoals
        fields = []

class DailyGoalsUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    
    class Meta:
        model = DailyGoals
        fields = ['title']

DailyGoalsUpdateFormset = modelformset_factory(DailyGoals, form=DailyGoalsUpdateForm, extra=0)
