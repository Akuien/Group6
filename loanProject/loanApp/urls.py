from django.urls import path,include

from loanApp.views import *
from django.contrib import admin
from allauth.account.views import PasswordResetView, PasswordResetDoneView
from django.conf import settings
from django.conf.urls.static import static
from loanApp.views import login_view
from .views import get_model_metadata


urlpatterns = [
    path('home', home, name='home'),
    #path('admin-dashboard',admin_dashboard, name='admin_dashboard'),
    path('user-dashboard', user_dashboard),
    path('applicants',applicants, name='applicants'),
    path('information',information, name='information'),
    path('delete', remove_user, name="remove_user"),
    path('performance',performance, name='performance'),
    path('reports',reports, name='reports'),
    path('predictions',predictions, name='predictions'),
    path('chat-assistance',chat_assistance, name='chat_assistance'),
    path('loan-history',loan_history, name='loan_history'),
    path('privacy-policy',privacy_policy, name='privacy_policy'),
    path('view-profile',view_profile, name='view_profile'),
    path('reset-password',reset_password, name='reset_password'),
    path('create-application',create_applicant, name='create_applicant'),
    path('get_model_metadata/', get_model_metadata, name='get_model_metadata'),
    path('', welcome, name='welcome'),
    path('login/', login_view, name ='login'),
    path('accounts/', include('allauth.urls')),
    path("profile/<str:id>/", profile, name="profile"),
    path("update/", update, name="update"),
    path('accounts/password-reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/password-reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('register/', register, name='register'),
    path('logout_user',logout_user, name='logout'),
    path('deleteImage', delete_image)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)