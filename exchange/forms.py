from django import forms
from .models import Book, ExchangeOffer, ExchangeRequest
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'image', 'category']


class ExchangeOfferForm(forms.ModelForm):
    class Meta:
        model = ExchangeOffer
        fields = ['to_user', 'requested_book']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'image']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        return password_confirm


class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['requested_book']

    def save(self, commit=True):
        instance = super().save(commit=False)

        print(
            f"Saving ExchangeRequest with offered_book={instance.offered_book} and requested_book={instance.requested_book}")

        if commit:
            instance.save()
        return instance

