from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_text_html

from to_do.models import TodoItem


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True,
        help_text=password_validators_help_text_html()
    )

    password_confirmation = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput,
        required=True,
        help_text="Please confirm your password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match. Please confirm your password.")

        return cleaned_data

    def save(self, commit=True):  # face parolele hash-ed pt user confidentiality
        password = self.cleaned_data['password']
        self.instance.set_password(password)

        return super().save(commit)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = TodoItem  # Your TodoItem model
        fields = ['task', 'description', 'status', 'priority', 'due_date']  # Fields of your TodoItem model

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop the 'user' argument passed to the form
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        task = super().save(commit=False, *args, **kwargs)
        task.user = self.user  # Assign the logged-in user to the task
        if commit:
            task.save()
        return task

# incercare
class CustomPasswordResetForm(PasswordResetForm):   # sa reseteze parola daca o uita
    email = forms.EmailField(label="Email", max_length=254)