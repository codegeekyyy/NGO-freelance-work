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
]