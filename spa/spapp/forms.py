from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    message = forms.CharField(label='Message', widget=forms.Textarea)
class SubscribeForm(forms.Form):
    user_email=forms.CharField(max_length=200)