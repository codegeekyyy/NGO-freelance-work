from django import forms
from .models import Volunteer, ContactMessage, Donation, GalleryPhoto, Testimonial

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
        fields = ['donor_name', 'email', 'amount', 'transaction_id', 'image']
        widgets = {
            'donor_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Amount (INR)', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Transaction ID (Optional)', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-[#7C9070] file:text-white file:font-bold'}),
        }

class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project Title (e.g. Classroom Joy)', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'description': forms.Textarea(attrs={'placeholder': 'Tell the story behind this photo...', 'rows': 3, 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757] resize-none'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-[#7C9070] file:text-white file:font-bold'}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'role': forms.TextInput(attrs={'placeholder': 'e.g., Volunteer, Donor, Beneficiary', 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757]'}),
            'content': forms.Textarea(attrs={'placeholder': 'Share your experience with Leela Foundation...', 'rows': 4, 'class': 'w-full p-4 rounded-xl border border-[#F2E7D5] focus:outline-none focus:border-[#D97757] resize-none'}),
        }
