from django import forms
from .models import User, Review, Favorite, Reservation

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['age', 'gender']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','content', 'image', 'date','sustainability_rating', 'positive_rating','rate']
        widgets = {
            'sustainability_rating': forms.RadioSelect(choices=Review.YES_NO_CHOICES),
            'positive_rating': forms.RadioSelect(choices =Review.YES_NO_CHOICES),
            'title' : forms.TextInput(attrs={'placeholder':'제목을 입력하세요.'}),
            'content': forms.Textarea(attrs={'placeholder': '|후기를 남겨주세요.'}),
            'rate': forms.NumberInput(attrs={'step': 0.5, 'min': 0, 'max': 5}),
            'date': forms.DateInput(attrs={ 'type': 'date'}),
        }

class FovoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['popup_store']


class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    category = forms.ChoiceField(required=False)
    location = forms.ChoiceField(required=False)
    date = forms.DateField(required=False)

    
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time','participant' ]

        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type':'time','step': 1800})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].input_formats = ['%H:%M'] 
    def clean_time(self):
        time_value = self.cleaned_data['time']
        # 필요에 따라 추가적인 시간 유효성 검사를 수행할 수 있음
        return time_value