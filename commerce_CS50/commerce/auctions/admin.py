from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "username", "is_superuser")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
