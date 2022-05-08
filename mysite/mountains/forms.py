from django import forms
from django.core.exceptions import ValidationError

from .models import AdvUser, Comment, Equipment, Wishes


class ChangeUserInfoForm (forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')




class RegisterUserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            errors = {'password': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)


    class Meta:
        model = AdvUser
        fields = ('username', 'password', 'password2', 'first_name', 'last_name', 'email', 'phone', 'photo')




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)



class WishesForm(forms.Form):
    pass



class SendForm(forms.Form):
    phone = forms.CharField(max_length=20)
    name = forms.CharField(max_length=50)




