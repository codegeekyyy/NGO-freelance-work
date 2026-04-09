from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Testimonial, Donation, Volunteer, ImpactStatistic, GalleryPhoto, Category
import json
from django.db.models import Sum
from django.contrib import messages
from .forms import VolunteerForm, DonationForm, ContactForm, GalleryPhotoForm, TestimonialForm
from .brevo_email import send_brevo_email
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def home(request):
    volunteer_form = VolunteerForm()
    contact_form = ContactForm()
    upload_form = GalleryPhotoForm()
    testimonial_form = TestimonialForm()

    if request.method == 'POST':
        if 'volunteer_submit' in request.POST:
            volunteer_form = VolunteerForm(request.POST)
            if volunteer_form.is_valid():
                if request.user.is_authenticated and Volunteer.objects.filter(user=request.user).exists():
                    messages.error(request, 'You have already submitted a volunteer application.')
                    return redirect('home')

                volunteer = volunteer_form.save(commit=False)
                if request.user.is_authenticated:
                    volunteer.user = request.user
                volunteer.save()
                send_brevo_email(
                    subject=f'New Volunteer Application - {volunteer.name}',
                    body=(
                        f'New volunteer application received!\n\n'
                        f'Name        : {volunteer.name}\n'
                        f'Email       : {volunteer.email}\n'
                        f'Phone       : {volunteer.phone or "Not provided"}\n'
                        f'Motivation  : {volunteer.motivation_to_join or "Not provided"}\n'
                        f'Skills      : {volunteer.skills or "Not provided"}\n'
                    ),
                )
                messages.success(request, 'Thank you for your interest in volunteering!')
                return redirect('home')

        elif 'contact_submit' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                send_brevo_email(
                    subject=f'New Contact Message: {contact_form.cleaned_data["subject"]}',
                    body=(
                        f'New contact message received!\n\n'
                        f'Name    : {contact_form.cleaned_data["name"]}\n'
                        f'Email   : {contact_form.cleaned_data["email"]}\n'
                        f'Subject : {contact_form.cleaned_data["subject"]}\n'
                        f'Message : {contact_form.cleaned_data["message"]}\n'
                    ),
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('home')

        elif 'photo_submit' in request.POST and request.user.is_staff:
            upload_form = GalleryPhotoForm(request.POST, request.FILES)
            if upload_form.is_valid():
                upload_form.save()
                messages.success(request, 'Photo uploaded to gallery successfully!')
                return redirect('home')

        elif 'testimonial_submit' in request.POST and request.user.is_authenticated:
            testimonial_form = TestimonialForm(request.POST, request.FILES)
            if testimonial_form.is_valid():
                testimonial_form.save()
                messages.success(request, 'Thank you for sharing your Whispers of Impact!')
                return redirect('home')

    events = Event.objects.filter(is_active=True).order_by('-date')[:5]
    testimonials = Testimonial.objects.all().order_by('-created_at')[:5]
    stats = ImpactStatistic.objects.first()
    gallery_photos = GalleryPhoto.objects.all().order_by('-created_at')

    # Global counts for the homepage
    total_volunteers = Volunteer.objects.count()
    total_events = Event.objects.count()

    # Serialize for frontend JS
    photos_list = []
    for p in gallery_photos:
        photos_list.append({
            'id': p.id,
            'title': p.title or "Moment of Impact",
            'image': p.image.url,
            'description': p.description or "",
            'date': p.created_at.strftime('%Y-%m-%d')
        })

    context = {
        'events': events,
        'testimonials': testimonials,
        'form': volunteer_form,
        'contact_form': contact_form,
        'stats': stats or {'lives_touched': '12K+', 'bloom_rate': '85%', 'communities': '40+'},
        'total_volunteers': total_volunteers,
        'total_events': total_events,
        'upload_form': upload_form,
        'gallery_photos': gallery_photos,
        'gallery_photos_json': json.dumps(photos_list),
        'testimonial_form': testimonial_form,
    }
    return render(request, 'home.html', context)

def donate(request):
    donation_form = DonationForm()
    if request.method == 'POST':
        donation_form = DonationForm(request.POST, request.FILES)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            if request.user.is_authenticated:
                donation.user = request.user
            donation.save()
            
            # Email Notification to NGO via Brevo REST API
            proof_link = f"\nProof Image : {request.build_absolute_uri(donation.image.url)}" if donation.image else ""
            send_brevo_email(
                subject=f'New Donation: Rs.{donation.amount} from {donation.donor_name}',
                body=(
                    f'New donation notification received!\n\n'
                    f'Donor          : {donation.donor_name}\n'
                    f'Email          : {donation.email}\n'
                    f'Amount         : Rs.{donation.amount}\n'
                    f'Transaction ID : {donation.transaction_id or "Not Provided"}\n'
                    f'Payment Proof  : {"Attached" if donation.image else "Not Provided"}{proof_link}\n'
                ),
            )
            messages.success(request, f'Thank you, {donation.donor_name}! Your details and proof have been successfully recorded.')
                
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
    if request.user.is_staff:
        # NGO Owner View: Calculate global impact statistics
        total_volunteers = Volunteer.objects.count()
        total_global_donations = Donation.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
        total_events = Event.objects.count()
        
        context = {
            'is_staff': True,
            'total_volunteers': total_volunteers,
            'total_global_donations': total_global_donations,
            'total_events': total_events
        }
    else:
        # Regular User View: Fetch personal data
        user_donations = Donation.objects.filter(user=request.user).order_by('-date')
        user_total_donated = user_donations.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Check if the user has a volunteer profile
        volunteer_profile = Volunteer.objects.filter(user=request.user).first()
        volunteer_hours = volunteer_profile.volunteer_hours if volunteer_profile else 0
        
        context = {
            'is_staff': False,
            'user_donations': user_donations,
            'user_total_donated': user_total_donated,
            'volunteer_hours': volunteer_hours,
        }
        
    return render(request, 'dashboard.html', context)


def gallery(request):
    upload_form = GalleryPhotoForm()

    if request.method == 'POST' and request.user.is_staff:
        upload_form = GalleryPhotoForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('gallery')
        else:
            messages.error(request, 'There was an error uploading the photo. Please try again.')

    photos_qs = GalleryPhoto.objects.all().order_by('-created_at')
    
    # Serialize for frontend JS
    photos_list = []
    for p in photos_qs:
        photos_list.append({
            'id': p.id,
            'title': p.title or "Moment of Impact",
            'image': p.image.url,
            'description': p.description or "",
            'date': p.created_at.strftime('%Y-%m-%d')
        })

    context = {
        'photos': photos_qs,
        'photos_json': json.dumps(photos_list),
        'upload_form': upload_form,
    }
    return render(request, 'gallery.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)


def stories(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    testimonial_form = TestimonialForm()

    if request.method == 'POST' and 'testimonial_submit' in request.POST and request.user.is_authenticated:
        testimonial_form = TestimonialForm(request.POST, request.FILES)
        if testimonial_form.is_valid():
            testimonial_form.save()
            messages.success(request, 'Thank you for sharing your story!')
            return redirect('stories')

    context = {
        'testimonials': testimonials,
        'testimonial_form': testimonial_form,
    }
    return render(request, 'stories.html', context)


def impact(request):
    stats = ImpactStatistic.objects.first()
    events = Event.objects.all().order_by('-date')
    context = {
        'stats': stats or {'lives_touched': '12K+', 'bloom_rate': '85%', 'communities': '40+'},
        'events': events,
    }
    return render(request, 'impact.html', context)


def volunteer_view(request):
    volunteer_form = VolunteerForm()
    if request.method == 'POST':
        volunteer_form = VolunteerForm(request.POST)
        if volunteer_form.is_valid():
            if request.user.is_authenticated and Volunteer.objects.filter(user=request.user).exists():
                messages.error(request, 'You have already submitted a volunteer application.')
                return redirect('volunteer')
                
            volunteer = volunteer_form.save(commit=False)
            if request.user.is_authenticated:
                volunteer.user = request.user
            volunteer.save()
            send_brevo_email(
                subject=f'New Volunteer Application - {volunteer.name}',
                body=(
                    f'New volunteer application received!\n\n'
                    f'Name        : {volunteer.name}\n'
                    f'Email       : {volunteer.email}\n'
                    f'Phone       : {volunteer.phone or "Not provided"}\n'
                    f'Motivation  : {volunteer.motivation_to_join or "Not provided"}\n'
                    f'Skills      : {volunteer.skills or "Not provided"}\n'
                ),
            )
            messages.success(request, 'Thank you for your interest in volunteering!')
            return redirect('volunteer')
            
    context = {
        'form': volunteer_form,
    }
    return render(request, 'volunteer.html', context)


def about(request):
    stats = ImpactStatistic.objects.first()
    context = {
        'stats': stats or {'lives_touched': '12K+', 'bloom_rate': '85%', 'communities': '40+'},
    }
    return render(request, 'about.html', context)


def contact(request):
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            send_brevo_email(
                subject=f'New Contact Message: {contact_form.cleaned_data["subject"]}',
                body=(
                    f'New contact message received!\n\n'
                    f'Name    : {contact_form.cleaned_data["name"]}\n'
                    f'Email   : {contact_form.cleaned_data["email"]}\n'
                    f'Subject : {contact_form.cleaned_data["subject"]}\n'
                    f'Message : {contact_form.cleaned_data["message"]}\n'
                ),
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
            
    context = {
        'contact_form': contact_form,
    }
    return render(request, 'contact.html', context)