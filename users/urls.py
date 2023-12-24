'''urls for the users app'''
from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LoginView,
)

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='users\\templates\\registration\\logged_out.html'), name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='users\\templates\\registration\\password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users\\templates\\registration\\password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users\\templates\\registration\\password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users\\templates\\registration\\password_reset_done.html'), name='password_reset_complete'),
    #registration page
    path('sign-up/', views.sign_up, name='sign-up'),
    # profile page
    path('create-profile', views.create_profile, name='create-profile'),
    path('profile/<str:username>', views.profile, name='profile')
]