from django.shortcuts import render
from django.http import JsonResponse, Http404
from item.models import Item,ItemImage
from cart.models import Cart
from customuser.models import User, Guest
import csv
from django.http import HttpResponse

def quick_view(request):
    return_dict = {}
    data = request.POST
    print(data)
    item_id = int(data.get('item_id'))
    item = Item.objects.get(id=item_id)
    images = ItemImage.objects.filter(item_id=item_id)
    if item.discount > 0:
        return_dict['item_price_discount'] = item.discount_value
    return_dict['item_id'] = item.id
    return_dict['item_name'] = item.name
    return_dict['item_name_slug'] = item.name_slug
    return_dict['item_description'] = item.description
    return_dict['item_price'] = item.price
    return_dict['item_discount'] = item.discount
    return_dict['item_new'] = item.is_new
    return_dict['item_article'] = item.article
    return_dict['item_present'] = item.is_present
    return_dict['item_images'] = list()
    for image in images:
        return_dict['item_images'].append(image.image_small)
    return JsonResponse(return_dict)


def feed(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fb_feed.csv"'

    writer = csv.writer(response)
    writer.writerow(['id','availability','condition','description','image_link','link','title','price',
                     'brand'])
    all_items = Item.objects.all()
    for item in all_items:
        writer.writerow(
            [item.id,'in stock','new',f'http://46.229.214.96/{item.description,item.images.first().image.url}',
             f'http://46.229.214.96/category/{item.category.first().name_slug}/{item.name_slug}/',item.name,f'{item.price} RUB',
                     item.name])



    return response

