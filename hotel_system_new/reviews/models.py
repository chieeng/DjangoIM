from django.db import models
from accounts.models import CustomUser
from rooms.models import Room


class Review(models.Model):
    """Review model"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"Review {self.review_id} - {self.customer.username} ({self.rating} stars)"
