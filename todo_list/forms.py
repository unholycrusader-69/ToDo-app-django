from django import forms
from .models import ToDo,UserNote
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime


HOUR_CHOICES = [(f"{h:02}", f"{h:02}") for h in range(1, 13)]
MINUTE_CHOICES = [(f"{m:02}", f"{m:02}") for m in range(0, 60)]
AM_PM_CHOICES = [("AM", "AM"), ("PM", "PM")]


class ToDoForm(forms.ModelForm):
    deadline_hour = forms.ChoiceField(choices=HOUR_CHOICES, required=False)
    deadline_minute = forms.ChoiceField(choices=MINUTE_CHOICES, required=False)
    deadline_ampm = forms.ChoiceField(choices=AM_PM_CHOICES, required=False)

    class Meta:
        model = ToDo
        fields = ['title','deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a new task'
            }),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        hour = cleaned_data.get('deadline_hour')
        minute = cleaned_data.get('deadline_minute')
        ampm = cleaned_data.get('deadline_ampm')

        if hour and minute and ampm:
            hour = int(hour)
            minute = int(minute)

            if ampm == 'PM' and hour != 12:
                hour += 12
            elif ampm == 'AM' and hour == 12:
                hour = 0

            cleaned_data['deadline_time'] = datetime.time(hour, minute)
        else:
            cleaned_data['deadline_time'] = None

        return cleaned_data
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReviewForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='Your Feedback')

class UserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        fields = ['page_one', 'page_two']
        widgets = {
            'page_one': forms.Textarea(attrs={'placeholder': 'Write your thoughts here...'}),
            'page_two': forms.Textarea(attrs={'placeholder': 'Ideas, reflections, reminders...'}),
        }