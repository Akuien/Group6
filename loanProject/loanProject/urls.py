from django.urls import path,include

from loanApp.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from loanApp.views import login_view
from allauth.account.views import PasswordResetView, PasswordResetDoneView
from loanApp.views import profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('loanApp.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)