import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://kolkata.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render(request, 'Base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser') #extracts the HTML of the page
    post_listings = soup.find_all('li', {'class': 'result-row'}) #extracting all the deatils of list elemets
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').get_text()
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').get_text()
        else:
            post_price = 'Price not Available'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url='https://craigslist.org/images/peace.jpg'
        final_postings.append((post_title,post_url,post_price,post_image_url))

    stuff_for_frontend = {
        'search':search,
        'final_postings':final_postings,
    }
    return render(request, 'My_App/new_search.html', stuff_for_frontend)
