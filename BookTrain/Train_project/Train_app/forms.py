from django import forms
from Train_app.models import PassengerModel

class PassengerForm(forms.ModelForm):
    gender_choice = (('M', 'Male'),('F', 'Female') ,('Trans', 'Transgender'))
    berth_choice = (('U', 'Upper'),('SU', 'Side Upper'),('L', 'Lower'),('M', 'Middle'),('SL', 'Side Lower'), ('WS', 'Window Side'), ('MB', 'Middle Seat'), ('A', 'Aisle'))

    Gender = forms.ChoiceField(widget=forms.Select, choices=gender_choice)
    Berth = forms.ChoiceField(widget=forms.Select, choices=berth_choice)

    class Meta():
        model = PassengerModel
        fields = ('Passenger_name', 'Age', 'Gender', 'Berth')
