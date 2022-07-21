from django import forms

class TodoForm(forms.Form):
    todo = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control rounded-0 rounded-start', 'placeholder': 'Add task'}
        ),
        label='',
        required=False
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}
        ),
        label='',
        required=False
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}
        ),
        label='',
        required=False
    )
    repassword = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'password(again)'}
        ),
        label='',
        required=False
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}
        ),
        label='',
        required=False
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}
        ),
        label='',
        required=False
    )
