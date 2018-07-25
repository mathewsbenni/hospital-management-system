from django import forms

class CreateUserForm(form.Form):
    username = forms.StringField(required=True)
    password = forms.StringField(widget=forms.PasswordInput, required=True)
    user_type = forms.StringField(required=True)
    