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
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['id','title','description','rich_text_description','availability','condition','price','link',
                     'image_link','brand','additional_image_link','age_group','color','gender','item_group_id',
                     'google_product_category','product_type','sale_price','sale_price_effective_date','size',
                     'offer_price','offer_price_effective_date','visibility','inventory'])
    all_items = Item.objects.all()
    for item in all_items:
        writer.writerow(
            ['id', 'title', 'description', 'rich_text_description', 'availability', 'condition', 'price', 'link',
             'image_link', 'brand', 'additional_image_link', 'age_group', 'color', 'gender', 'item_group_id',
             'google_product_category', 'product_type', 'sale_price', 'sale_price_effective_date', 'size',
             'offer_price', 'offer_price_effective_date', 'visibility', 'inventory'])



    return response

