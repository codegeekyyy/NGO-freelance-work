from django.contrib import admin
from .models import Category, Event, Volunteer, Donation, ContactMessage, Testimonial, ImpactStatistic, GalleryPhoto, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3

@admin.register(ImpactStatistic)
class ImpactStatisticAdmin(admin.ModelAdmin):
    list_display = ('lives_touched', 'bloom_rate', 'communities')
    def has_add_permission(self, request):
        # Only allow one instance of stats
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'Category', 'date', 'is_active')
    list_filter = ('Category', 'is_active', 'date')
    search_fields = ('title', 'description', 'location')
    inlines = [EventImageInline]

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


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    exclude = ('category',)
