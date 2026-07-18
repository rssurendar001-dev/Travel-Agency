from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from .models import CurrencyConverter, Enquiry, Blog, Memory, BudgetPlanner, TravelBuddy, TravelCost

class SignupForm(forms.Form):

    username = forms.CharField(max_length=100)

    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput())

    confirm_password = forms.CharField(widget=forms.PasswordInput())

from django import forms
from datetime import date
from .models import Enquiry

class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry
        fields = [
            'destination',
            'travel_date',
            'adults',
            'children',
            'phone',
            'email',
        ]

        widgets = {
            'travel_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': date.today().strftime('%Y-%m-%d')
                }
            )
        }

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']

        if travel_date < date.today():
            raise forms.ValidationError(
                "Travel date cannot be in the past. Please select today or a future date."
            )

        return travel_date
        
class BlogForm(forms.ModelForm):

    class Meta:

        model = Blog

        fields = [

            'title',

            'destination',

            'image',

            'content',
            
        ]   

class MemoryForm(forms.ModelForm):

    class Meta:
        model = Memory
        fields = [
            
            'album_name', 
                  
            'image', 
                  
            'caption'
                  
        ]

class BudgetPlannerForm(forms.ModelForm):

    class Meta:
        model = BudgetPlanner

        fields = [
            
            'total_budget',
            
            'transport',
            
            'hotel',
            
            'food',
            
            'shopping'
            
        ]
        
class TravelCostForm(forms.ModelForm):

    class Meta:

        model = TravelCost

        fields = [

            'destination',

            'people',

            'hotel_type',

            'days',

        ]

        widgets = {

            'destination': forms.Select(attrs={'class': 'form-control'}),

            'people': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Number of People'}),

            'hotel_type': forms.Select(attrs={'class': 'form-control'}),

            'days': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Number of Days'})
            
        }
             

from datetime import date
from django import forms

class TravelBuddyForm(forms.ModelForm):

    class Meta:
        model = TravelBuddy
        fields = [
            'destination',
            'travel_date',
            'budget',
            'interest',
            'about',
            'phone',
            'email',
        ]

        widgets = {
            'travel_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': date.today().strftime('%Y-%m-%d')
                }
            ),
            'about': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']

        if travel_date < date.today():
            raise forms.ValidationError(
                "Travel date cannot be in the past. Please select today or a future date."
            )

        return travel_date
        
class CurrencyConverterForm(forms.ModelForm):

    class Meta:

        model = CurrencyConverter

        fields = [

            'amount',

            'from_currency',

            'to_currency',

        ]

        widgets = {

            'amount': forms.NumberInput(
                
                attrs={
                    
                    'class': 'form-control',
                    
                    'placeholder': 'Enter Amount'
                    
                }
            ),

            'from_currency': forms.Select(attrs={'class': 'form-select'}),

            'to_currency': forms.Select(attrs={'class': 'form-select'})

        }

class EmailForm(forms.Form):

    email = forms.EmailField(
        
        widget=forms.EmailInput(
            
            attrs={
                
                "class": "form-control",
                
                "placeholder": "Enter Email"
                
            }
        )
    )


class OTPForm(forms.Form):

    otp = forms.CharField(
        
        max_length=6,
        
        widget=forms.TextInput(
            
            attrs={
                
                "class": "form-control",
                
                "placeholder": "Enter OTP"
                
            }
        )
    )