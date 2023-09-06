from django.contrib import admin
from core.models import Ticket, Review, UserFollow


class TicketAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


class UserFollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ticket, TicketAdmin)

admin.site.register(Review, ReviewAdmin)

admin.site.register(UserFollow, UserFollowAdmin)
