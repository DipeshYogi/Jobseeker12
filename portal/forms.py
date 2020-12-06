from django import forms
from .models import Jobs

class searchForm(forms.Form):
    Skills  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Skills'}),label='')
    Experience = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Experience'}),label='')

    Choices = (
                    ('Full time','Full time'),
                    ('Part time','Part time'),
                    ('Contract based','Contract based'),
        )
    Type = forms.ChoiceField(choices = Choices,label='')
