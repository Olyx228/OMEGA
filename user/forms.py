from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import Request, Category, Profile

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
        }),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }),
        label='Пароль'
    )

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')
    full_name = forms.CharField(
        label='ФИО',
        max_length=255,
        required=True
    )
    username = forms.CharField(
        label='Логин',
        max_length=150,
        required=True
    )
    consent = forms.BooleanField(required=True, label='Согласие на обработку персональных данных')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'consent')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise ValidationError('Логин должен содержать только латиницу и дефисы.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[а-яА-ЯёЁА-Я\s-]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу, дефисы и пробелы.')
        return full_name

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'description': forms.Textarea(attrs={
                'class:' : 'form-control des'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            })
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError('Размер фото не должен превышать 2MB.')
            if not photo.name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise forms.ValidationError('Недопустимый формат файла. Используйте jpg, jpeg, png или bmp.')
        return photo

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'title': 'Выберите новый аватар',
                'style': 'display: block;',
            }),
        }

class UpdateStatusForm(forms.ModelForm):
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Request
        fields = ['status', 'comment', 'photo']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select',
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        photo = cleaned_data.get('photo')

        if status == 'accepted_in_work' and not cleaned_data.get('comment'):
            self.add_error('comment', 'Необходим комментарий для изменения статуса на "Принято в работу".')

        if status == 'completed' and not photo:
            self.add_error('photo', 'Необходимо прикрепить фото для изменения статуса на "Выполнено".')

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('Категория существует')
        return name
