from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

import authentication.views
import core.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', core.views.home, name='home'),
    path('posts/', core.views.display_posts, name='posts'),

    # path('feed/', core.views.feed, name='feed'),
    path('ticket/create', core.views.create_ticket, name='create_ticket'),
    path('profile-photo/upload', authentication.views.upload_profile_photo,
         name='upload_profile_photo'),
    path('review/create', core.views.create_review, name='create_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
