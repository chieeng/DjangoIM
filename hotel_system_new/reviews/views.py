from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Review


@login_required(login_url='accounts:login')
def reviews_list(request):
    """List all reviews"""
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'reviews/reviews_list.html', context)
