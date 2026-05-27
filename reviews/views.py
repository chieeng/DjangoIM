from django.shortcuts import render
from .models import Review


def reviews_list(request):
    """List all reviews"""
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'reviews/reviews_list.html', context)
