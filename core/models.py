from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    motivation_to_join = models.TextField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    volunteer_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Donation(models.Model):
    STATUS_CHOICES=(
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g., Beneficiary, Volunteer, Donor")
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ImpactStatistic(models.Model):
    lives_touched = models.CharField(max_length=20, default="12K+")
    bloom_rate = models.CharField(max_length=20, default="85%")
    communities = models.CharField(max_length=20, default="40+")

    def __str__(self):
        return "Global Impact Statistics"