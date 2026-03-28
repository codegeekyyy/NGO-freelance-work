from django import forms
from .models import Volunteer, ContactMessage, Donation

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'motivation_to_join', 'skills',]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'motivation_to_join': forms.Textarea(attrs={'placeholder': 'Why do you want to join us?', 'rows': 4, 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'skills': forms.Textarea(attrs={'placeholder': 'What skills can you share?', 'rows': 3, 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4, 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'email', 'amount', 'transaction_id']
        widgets = {
            'donor_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Amount (INR)', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Transaction ID (Optional)', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
        }
