from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control", "autocomlete": "off"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control", "autocomlete": "off"}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

'''
Описание класса с помощью несвязанной формы
class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Заголовок', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(required=False, label='Контент', widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5,
    }))
    is_published = forms.BooleanField(initial=True, required=False, label='Опубликовано или нет',
                                      widget=forms.CheckboxInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      empty_label='Выберите категорию', widget=forms.Select(attrs={"class": "form-control"}))
'''
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            'category': forms.Select(attrs={"class": "form-control"}),
        }
        empty_label = {'category': 'Выберите категорию'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифр')
        return title