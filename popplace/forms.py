from django import forms
from .models import User, Review, Favorite, Stamp, Reservation

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['age', 'gender']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','content', 'image', 'video', 'sustainability_rating','rate']
        widgets = {
            'rate': forms.NumberInput(attrs={'step': 0.5, 'min': 0, 'max': 5}),
        }

class FovoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['popup_store']

class StampForm(forms.ModelForm):
    class Meta:
        model= Stamp
        fields = ['code']

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='검색', max_length=100)

    
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