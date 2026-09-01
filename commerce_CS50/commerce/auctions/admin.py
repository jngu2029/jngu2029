from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "username", "is_superuser")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidder", "amount")
    
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
