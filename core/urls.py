from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('donate/', views.donate, name='donate'),

    # auth login
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # protected dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # photo gallery
    path('gallery/', views.gallery, name='gallery'),

    # eventsdetail
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    
    #Routes
    path('stories/', views.stories, name='stories'),
    path('impact/', views.impact, name='impact'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]