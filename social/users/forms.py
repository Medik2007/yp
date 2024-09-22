from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

BANNED_CHARACTERS = [' ', '/', '?', '&', '%', '<', '>', "'", '"', ':', ';', ',', '|', '\\']


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    img = forms.CharField(label='Image')
    repeat_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password = forms.CharField(label='Repeat Password', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            self.add_error('username', 'Username should be uniqe')
            return
        for character in BANNED_CHARACTERS:
            if character in username:
                self.add_error('username', f"Username contains unallowed characters ('{character}')")
                return
        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email) or email == 'meeedik2007@gmail.com':
            return email 
        self.add_error('email', 'Email should be uniqe')
        return

    
    def clean_password(self):
        password = self.cleaned_data['password'] 
        if password != self.cleaned_data['repeat_password']:
            self.add_error('password', "Passwords don't match")
            return
        return password



class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
