from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

from authentication.views import signup_page, upload_profile_photo

from core.views import (create_review_from_ticket,
                        create_review,
                        create_ticket,
                        home,
                        display_posts,
                        follow_users, delete_follow, edit_ticket, edit_review
                        )

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
    path('signup/', signup_page, name='signup'),
    path('home/', home, name='home'),
    path('posts/', display_posts, name='posts'),

    path('ticket/create', create_ticket, name='create_ticket'),
    path('profile-photo/upload', upload_profile_photo,
         name='upload_profile_photo'),
    path('review-with-ticket/create', create_review, name='create_review'),
    path('review/<ticket>/create', create_review_from_ticket, name='create_review_from_ticket'),
    path('follow-users/', follow_users, name='follow_users'),
    path("delete_follow/<int:user_id>", delete_follow, name="delete_follow"),
    path("ticket/<int:ticket_id>/edit-ticket/", edit_ticket, name="edit_ticket"),
    path("review/<int:review_id>/edit-review/", edit_review, name="edit_review"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
