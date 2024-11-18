from django import forms
from .models import Jockey, Cheval, Course, Zone, Ecurie


class JockeyForm(forms.ModelForm):
    class Meta:
        model = Jockey
        fields = ['name', 'age', 'experience', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du jockey'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expérience en années'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ChevalForm(forms.ModelForm):
    class Meta:
        model = Cheval
        fields = ['name', 'age', 'race_type', 'jockey', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du cheval'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge'}),
            'race_type': forms.Select(attrs={'class': 'form-select'}),
            'jockey': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'date', 'location', 'chevaux']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la course'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu'}),
            'chevaux': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'type', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la zone'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EcurieForm(forms.ModelForm):
    class Meta:
        model = Ecurie
        fields = ['name', 'location', 'max_chevaux', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l’écurie'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu'}),
            'max_chevaux': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacité maximale'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }