from django import forms
from .models import User, Review, Favorite, Stamp

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['age', 'gender']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','content', 'image', 'video', 'sustainability_rating']

class FovoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['popup_store']

class StampForm(forms.ModelForm):
    class Meta:
        model= Stamp
        fields = ['code']

class SearchForm(forms.Form):
    query = forms.CharField(label='검색', max_length=100)