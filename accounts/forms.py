from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    last_name = forms.CharField(
        max_length=45,
        required=True,
        help_text='必須',
        label='姓'
    )
    first_name = forms.CharField(
        max_length=45,
        required=True,
        help_text='必須',
        label='名'
    )
    email = forms.EmailField(
        max_length=255,
        help_text='必須 有効なメールアドレスを入力してください。',
        label='Eメールアドレス'
    )
    phone_number = forms.CharField(
        max_length=45,
        help_text='必須 連絡が取れる電話番号を入力してください。',
        label='電話番号'
    )


    class Meta:
        model = User
        fields = ('last_name', 'first_name',  'email', 'phone_number', 'password1', 'password2', )