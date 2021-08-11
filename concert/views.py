from django.shortcuts import render
from concert.models import ConcertList

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    concerts = ConcertList.objects.all()

    # Available books (status = 'a')
    num_yedang_available = ConcertList.objects.filter(place__exact='예술의전당').count()
    num_lotte_available = ConcertList.objects.filter(place__exact='롯데콘서트홀').count()
    num_kumho_available = ConcertList.objects.filter(place__exact='금호아트홀').count()
    num_sejong_available = ConcertList.objects.filter(place__exact='세종문화회관').count()
    num_thehouse_available = ConcertList.objects.filter(place__exact='더하우스콘서트').count()

    # The 'all()' is implied by default.
    
    context = {
        'num_concerts': concerts.count(),
        'num_yedang_available': num_yedang_available,
        'num_lotte_available' : num_lotte_available,
        'num_kumho_available': num_kumho_available,
        'num_sejong_available': num_sejong_available,
        'num_thehouse_available': num_thehouse_available,
        'concerts' : concerts
    }

    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)