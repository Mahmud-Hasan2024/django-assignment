from django import forms
from events.models import Event, Category
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'date': forms.SelectDateWidget(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'time': forms.TimeInput(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'location': forms.TextInput(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'category': forms.Select(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'participants': forms.SelectMultiple(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'image': forms.ClearableFileInput(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 rounded p-2 w-full'}),
        }

class ParticipantCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ParticipantUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email']


class EditUserForm(forms.ModelForm):
    group = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['group'].choices = [(group.name, group.name) for group in Group.objects.all()]


class GroupPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
