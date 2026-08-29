from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.TextField(max_length = 500)
    picture = models.URLField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #The user who created the listing
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    #users who have a listing on their watchlist
    watchers = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlist"
    )
    def __str__(self):
        return self.title

class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    #receiving the bid
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    #user who placed bid
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    
    
    def __str__(self):
        return f"{self.bidder}, {self.amount} for {self.listing}"

class Comment(models.Model):
    text = models.TextField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add=True)
    #listing being commented on
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    #user who wrote the comment
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    
    def __str__(self):
        return f"{self.author} commented on {self.listing}"