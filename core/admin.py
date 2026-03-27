from django.contrib import admin
from .models import Category, Event, Volunteer, Donation, ContactMessage, Testimonial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'Category', 'date', 'is_active')
    list_filter = ('Category', 'is_active', 'date')
    search_fields = ('title', 'description', 'location')

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('donor_name', 'transaction_id', 'email')
    readonly_fields = ('date',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at')
    search_fields = ('name', 'content')