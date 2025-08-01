from django import forms
from .models import JournalEntry

class JournalEntryCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    journal_content = forms.CharField(max_length=100000)

    class Meta:
        model = JournalEntry
        fields = ['title', 'journal_content']