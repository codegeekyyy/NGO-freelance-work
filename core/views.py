from django.shortcuts import render, redirect
from .models import Event, Testimonial, Donation, Volunteer, ImpactStatistic
from django.db.models import Sum
from django.contrib import messages
from .forms import VolunteerForm, DonationForm, ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def home(request):
    volunteer_form = VolunteerForm()
    contact_form = ContactForm()
    if request.method == 'POST':
        if 'volunteer_submit' in request.POST:
            volunteer_form = VolunteerForm(request.POST)
            if volunteer_form.is_valid():
                volunteer = volunteer_form.save(commit=False)
                if request.user.is_authenticated:
                    volunteer.user = request.user
                volunteer.save()
                
                send_mail(
                    'New Volunteer Application',
                    f'Name: {volunteer.name}\nEmail: {volunteer.email}',
                    settings.DEFAULT_FROM_EMAIL,
                    ['leelafoundation323@gmail.com'],
                    fail_silently=True,
                )
                messages.success(request, 'Thank you for your interest in volunteering!')
                return redirect('home')
        
        elif 'contact_submit' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                send_mail(
                    f'New Contact: {contact_form.cleaned_data["subject"]}',
                    f'From: {contact_form.cleaned_data["name"]}\nMessage: {contact_form.cleaned_data["message"]}',
                    settings.DEFAULT_FROM_EMAIL,
                    ['leelafoundation323@gmail.com'],
                    fail_silently=True,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('home')

    events = Event.objects.filter(is_active=True).order_by('-date')[:5]
    testimonials = Testimonial.objects.all().order_by('-created_at')[:5]
    stats = ImpactStatistic.objects.first()
    
    # Global counts for the homepage
    total_volunteers = Volunteer.objects.count()
    total_events = Event.objects.count()
    
    context = {
        'events': events,
        'testimonials': testimonials,
        'form': volunteer_form,
        'contact_form': contact_form,
        'stats': stats or {'lives_touched': '12K+', 'bloom_rate': '85%', 'communities': '40+'},
        'total_volunteers': total_volunteers,
        'total_events': total_events
    }
    return render(request, 'home.html', context)

@login_required
def donate(request):
    donation_form = DonationForm()
    if request.method == 'POST':
        donation_form = DonationForm(request.POST)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            if request.user.is_authenticated:
                donation.user = request.user
            donation.save()
            messages.success(request, 'Thank you for your contribution! We will verify it soon.')
            return redirect('donate')
    context = {
        'donation_form': donation_form
    }
    return render(request, 'donation.html', context)


# authentication
def signup(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created successfully")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'auth/signup.html', context)


@login_required
def dashboard(request):
    # Calculate global impact statistics
    total_volunteers = Volunteer.objects.count()
    total_global_donations = Donation.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    total_events = Event.objects.count()
    
    context = {
        'total_volunteers': total_volunteers,
        'total_global_donations': total_global_donations,
        'total_events': total_events
    }
    return render(request, 'dashboard.html', context)