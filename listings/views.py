from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices

from .models import Listing

def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    # Создаем список фотографий, если они существуют
    photos = []
    for i in range(1, 7):  # Поддержка до 6 фотографий
        photo_attr = f'photo_{i}'
        if hasattr(listing, photo_attr):
            photo = getattr(listing, photo_attr)
            if photo:
                photos.append(photo)
    
    context = {
        'listing': listing,
        'photos': photos,
    }
    
    return render(request, 'listings/listing.html', context)


def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)