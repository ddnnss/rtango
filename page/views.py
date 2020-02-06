import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from item.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from customuser.forms import SignUpForm, UpdateForm
from order.models import *
from cart.models import Cart
from customuser.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import Http404



def create_password():
    from random import choices
    import string
    password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    return password

def is_email(string):

    from django.core.exceptions import ValidationError
    from django.core.validators import EmailValidator

    validator = EmailValidator()
    try:
        validator(string)
    except ValidationError:
        return False

    return True

def check_email(request):
    return_dict = {}
    email = request.POST.get('email')
    print(email)
    email_error = ''
    if is_email(email):
        email_is_valid = True
    else:
        email_is_valid = False
        email_error = 'Указанный адрес почты не верный'

    try:
        user = User.objects.get(email=email)
    except:
        user = None

    if user:
        email_is_valid = False
        email_error = 'Указанный адрес почты уже зарегистрирован'

    return_dict['result'] = email_is_valid
    return_dict['email_error'] = email_error
    return JsonResponse(return_dict)


def order(request, order_code):
    try:
        order = Order.objects.get(order_code=order_code)
    except:
        order=None

    if order:
        return render(request, 'page/order_complete.html', locals())
    else:
        raise Http404
        # return render(request, '404.html', locals())

def about_us(request):
    title = 'О НАС'
    show_tags = True
    if request.GET.get('sendmail') == '1':
        users = User.objects.all()
        for user in users:
            msg_html = render_to_string('email/sendmail.html')
            send_mail('Летняя скидка -15% в Лакшми888', None, 'info@lakshmi888.ru', [user.email],
                  fail_silently=False, html_message=msg_html)
    return render(request, 'page/about_us.html', locals())


def robots(request):

    return render(request, 'page/robots.txt')

def sitemap(request):
    return render(request, 'page/sitemap.xml', content_type = "application/xhtml+xml")




def contacts(request):
    show_tags = True
    title = 'КОНТАКТНАЯ ИНФОРМАЦИЯ'
    return render(request, 'page/contacts.html', locals())


def dostavka(request):
    show_tags = True
    title = 'ИНФОРМАЦИЯ О ДОСТАВКЕ'
    return render(request, 'page/dostavka.html', locals())


def new(request):
    all_items = Item.objects.filter(is_new=True, is_active=True, is_present=True).order_by('-created_at')
    not_present = Item.objects.filter(is_new=True, is_active=True, is_present=False)
    data = request.GET

    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())
        if not items:
            items = all_items.filter(article__contains=search)
        search_qs = items

        param_search = search

    if filter == 'new':

        if search_qs:
            items = search_qs.filter(is_new=True)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            filter_sq = items
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':


        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items
        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)

    if page:
        canonical_link = '/new/'

    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)
    show_tags = False
    return render(request, 'page/new.html', locals())

def get_checkout(request):
    print(request.POST)
    return_dict = {}
    newSessionTemp = None
    if request.user.is_authenticated:
        print('New sessionTemp for reg user')
        try:
            SessionTemp.objects.get(user=request.user).delete()
            newSessionTemp = SessionTemp.objects.create(user=request.user)
            print('New sessionTemp  for reg user delete and create')
        except:
            newSessionTemp = SessionTemp.objects.create(user=request.user)
            print('New sessionTemp  for reg user create')
    else:
        s_key = request.session.session_key
        guest = Guest.objects.get(session=s_key)
        print('New sessionTemp for guest user')
        try:
            SessionTemp.objects.get(guest=guest).delete()
            newSessionTemp = SessionTemp.objects.create(guest=guest)
            print('New sessionTemp  for guest user delete and create')
        except:
            newSessionTemp = SessionTemp.objects.create(guest=guest)
            print('New sessionTemp  for guest user create')

    newSessionTemp.delivery = int(request.POST.get('delivery'))
    if request.POST.get('needPhoto'):
        newSessionTemp.needPhoto = True
    if request.POST.get('cardText'):
        newSessionTemp.card_text = request.POST.get('cardText')

    newSessionTemp.save()

    return_dict['result'] = True
    return JsonResponse(return_dict)

def checkout(request):
    show_tags = True
    if request.POST:

        if request.POST.get('form_type') == 'user_info':
            client = request.user
            mail_tmp = client.is_allow_email
            form = UpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                client.profile_ok = True
                client.is_allow_email = mail_tmp
                client.save(force_update=True)

                return HttpResponseRedirect('/checkout/')
            else:
                client = request.user
                form = UpdateForm(instance=client)
                return HttpResponseRedirect('/checkout/')

        if request.POST.get('form_type') == 'checkout':
            order_code = create_password()
            if request.user.used_promo:
                promo_id = request.user.used_promo.id
            else:
                promo_id = None
            order = Order.objects.create(client=request.user, promo_code_id=promo_id, order_code=order_code,
                                         payment_id=int(request.POST.get('payment')),
                                         shipping_id=int(request.POST.get('shipping')))
            order.save(force_update=True)
            all_cart_items = Cart.objects.filter(client_id=request.user.id)
            for item in all_cart_items:
                ItemsInOrder.objects.create(order_id=order.id, item_id=item.item.id, number=item.number,
                                            current_price=item.item.price)
                item.item.buys = item.item.buys + 1
                item.item.save(force_update=True)
            all_cart_items.delete()
            request.user.used_promo = None
            request.user.save(force_update=True)
            new_order = Order.objects.get(id=order.id)
            msg_html = render_to_string('email/new_order.html', {'order': new_order})
            send_mail('Заказ успешно размещен', None, 'info@lakshmi888.ru', [request.user.email],
                      fail_silently=False, html_message=msg_html)
            send_mail('Новый заказ', None, 'norply@lakshmi888.ru', ['info@lakshmi888.ru'],
                      fail_silently=False, html_message=msg_html)
            return HttpResponseRedirect('/order/{}'.format(new_order.order_code))


        if request.POST.get('form_type') == 'checkout_guest':

            s_key = request.session.session_key
            guest = Guest.objects.get(session=s_key)
            name = request.POST.get('name')
            family = request.POST.get('family')
            otchestvo = request.POST.get('otchestvo')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            country = request.POST.get('country')
            city = request.POST.get('city')
            post_code = request.POST.get('post_code')
            address = request.POST.get('address')
            shipping = int(request.POST.get('shipping'))
            payment = int(request.POST.get('payment'))
            with_register=request.POST.get('with_register')
            user = None
            order_code = create_password()




            if guest.used_promo:
                promo_id = guest.used_promo.id
                print('With promo')
            else:
                promo_id = None
                print('With no promo')

            if request.POST.get('with_register') == 'on':
                print('With register')
                password = create_password()
                user = User.objects.create_user(email=email, name=name, family=family, otchestvo=otchestvo, country=country,
                                         city=city, post_code=post_code, phone=phone, address=address, profile_ok=True,
                                         password=password)
                msg_html = render_to_string('email/register.html', {'login': email, 'password': password})
                send_mail('Регистрация на сайте LAKSHMI888', None, 'info@lakshmi888.ru', [email],
                          fail_silently=False, html_message=msg_html)
            else:
                guest.email = email
                guest.name = name
                guest.family = family
                guest.otchestvo = otchestvo
                guest.country = country
                guest.city = city
                guest.post_code = post_code
                guest.phone = phone
                guest.address = address
                guest.save(force_update=True)

            if user:
                order = Order.objects.create(client=user, promo_code_id=promo_id, order_code=order_code,
                                         payment_id=int(request.POST.get('payment')),
                                         shipping_id=int(request.POST.get('shipping')))
            else:
                order = Order.objects.create(guest=guest, promo_code_id=promo_id, order_code=order_code,
                                             payment_id=int(request.POST.get('payment')),
                                             shipping_id=int(request.POST.get('shipping')))
            order.save(force_update=True)
            all_cart_items = Cart.objects.filter(guest_id=guest.id)
            for item in all_cart_items:
                ItemsInOrder.objects.create(order_id=order.id, item_id=item.item.id, number=item.number,
                                            current_price=item.item.price)
                item.item.buys = item.item.buys + 1
                item.item.save(force_update=True)
            all_cart_items.delete()
            guest.used_promo = None
            guest.save(force_update=True)
            new_order = Order.objects.get(id=order.id)
            msg_html = render_to_string('email/new_order.html', {'order': new_order})
            send_mail('Заказ успешно размещен', None, 'info@lakshmi888.ru', [email],
                      fail_silently=False, html_message=msg_html)
            send_mail('Новый заказ', None, 'norply@lakshmi888.ru', ['info@lakshmi888.ru'],
                      fail_silently=False, html_message=msg_html)
            print('Email sent')
            return HttpResponseRedirect('/order/{}'.format(new_order.order_code))

        if request.POST.get('form_type') == 'new_checkout':
            print(request.POST)
            order_code = create_password()
            is_need_photo = False
            receiver_name = request.POST.get('receiver-name')
            receiver_phone = request.POST.get('receiver-phone')
            sender_name = request.POST.get('sender-name')
            sender_phone = request.POST.get('sender-phone')
            sender_email = request.POST.get('sender-email')
            order_date = request.POST.get('order-date')
            order_time = request.POST.get('order-time')
            is_need_phono = request.POST.get('order-photo')
            if is_need_phono:
                is_need_photo = True
            card_text = request.POST.get('order-card')


            shipping = request.POST.get('shipping')

            order = Order.objects.create(order_code=order_code,
                                         receiver_name=receiver_name,
                                        receiver_phone=receiver_phone,
                                        sender_name =sender_name,
                                        sender_phone =sender_phone,
                                        sender_email =sender_email,
                                        order_date =order_date,
                                        order_time =order_time,
                                        is_need_photo = is_need_photo,
                                        card_text = card_text,
                                         shipping_id=shipping)
            if request.user.is_authenticated:
                all_cart_items = Cart.objects.filter(client_id=request.user.id)
            else:
                s_key = request.session.session_key
                guest = Guest.objects.get(session=s_key)
                all_cart_items = Cart.objects.filter(guest=guest)
            for item in all_cart_items:
                ItemsInOrder.objects.create(order_id=order.id, item_id=item.item.id, number=item.number,
                                            current_price=item.item.price)
                item.item.buys = item.item.buys + 1
                item.item.save()
            all_cart_items.delete()
            # request.user.used_promo = None
            # request.user.save()
            new_order = Order.objects.get(id=order.id)
            # msg_html = render_to_string('email/new_order.html', {'order': new_order})
            # send_mail('Заказ успешно размещен', None, 'info@lakshmi888.ru', [request.user.email],
            #           fail_silently=False, html_message=msg_html)
            # send_mail('Новый заказ', None, 'norply@lakshmi888.ru', ['info@lakshmi888.ru'],
            #           fail_silently=False, html_message=msg_html)
            return HttpResponseRedirect('/order/{}'.format(new_order.order_code))



#-------------------------------------------------------------------------------GET request
    shipping = OrderShipping.objects.all()
    # payment = OrderPayment.objects.all()
    sessionTemp = None
    if request.user.is_authenticated:
        try:
            sessionTemp = SessionTemp.objects.get(user=request.user)
        except:
            pass

    else:
        s_key = request.session.session_key
        guest = Guest.objects.get(session=s_key)
        try:
            sessionTemp = SessionTemp.objects.get(guest=guest)
        except:
            pass


    if request.user.is_authenticated:
        client = request.user
        form = UpdateForm(instance=client)
        return render(request, 'page/checkout.html', locals())
    else:
        form = UpdateForm()
        return render(request, 'page/checkout.html', locals())




def index(request):
    show_tags = True
    title = ''
    description = ''
    keywords = ''
    most_view_items = Item.objects.all().order_by('-views')
    most_buys_items = Item.objects.all().order_by('-buys')
    banners = Banner.objects.filter(is_active=True).order_by('order')
    items_with_discount = Item.objects.filter(discount__gt=0)
    main_category = Category.objects.all()
    index_cats = main_category.filter(show_at_index=True)
    all_filters = Filter.objects.all()
    all_promotions = Promotion.objects.all()
    return render(request, 'page/index.html', locals())



def category(request, slug, subcat_slug):
    # try:
    print(subcat_slug)

    popular_category = Category.objects.all().order_by('-views')
    category = Category.objects.get(name_slug=slug)

    all_items = Item.objects.filter(category=category, is_active=True, is_present=True, is_optional=False).order_by('-created_at')
    category.views += 1
    category.save()
    tag_h1 = category.page_h1
    title = category.page_title
    description = category.page_description
    keywords = category.page_keywords
    if subcat_slug != 'all':
        filterItem = Filter.objects.get(name_slug=subcat_slug)
        all_items = all_items.filter(filter=filterItem.id)
        param_filter = filterItem.name_slug
        tag_h1 = filterItem.page_h1
        title = filterItem.page_title
        description = filterItem.page_description
        keywords = filterItem.page_keywords
    # except:
    #     raise Http404
        # return render(request, '404.html', locals())
    data = request.GET
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())


        if not items:
            items = all_items.filter(article__contains=search)

        search_qs = items
        param_search = search

    if filter == 'new':

        if search_qs:
            items = search_qs.filter(is_new=True)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            filter_sq = items
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':


        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)

            filter_sq = items

            param_filter = filter
        else:
            filterItem = Filter.objects.get(name=filter)
            items = all_items.filter(filter=filterItem.id)

            currentFilter = Filter.objects.get(name=filter)
            #seoText = currentFilter.seoText
            filter_sq = items

            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items

        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)


    try:
        items = items_paginator.get_page(page)
        show_tags = False
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/category.html', locals())


def item_page(request, cat_slug, item_slug):
    try:
        item = Item.objects.get(name_slug=item_slug)
        category = Category.objects.get(name_slug=cat_slug)
        item.views += 1
        item.save(force_update=True)

        # recomended = Item.objects.filter(subcategory_id=item.subcategory_id).order_by('-views')[:12]
        # title = item.name
        # description = item.description

    # print(recomended)
    except:
        raise Http404
        # return render(request, '404.html', locals())
    item_parts = ItemParts.objects.filter(item=item)
    all_shipping = OrderShipping.objects.all().order_by('-id')
    all_filters = item.filter.all()
    title = ''
    description = ''
    return render(request, 'item/item.html', locals())


def search(request):
    show_tags = False
    search_string = request.GET.get('search')
    page = request.GET.get('page')
    param_search = search_string
    try:
        items = Item.objects.filter(name_lower__contains=search_string.lower(), is_active=True)
    except:
        return render(request, '404.html', locals())
    if not items:
        items = Item.objects.filter(name_lower__contains=search_string.lower()[:-1], is_active=True)
    if not items:
        items = Item.objects.filter(article__contains=search_string)
    items_paginator = Paginator(items, 12)
    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/search.html', locals())


def customhandler404(request, exception, template_name='404.html'):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


def one_click(request):
    if request.POST.get('form_type') == 'oneclick':
        OneClick.objects.create(item_id=request.POST.get('item-id'),phone=request.POST.get('phone'))
    if request.POST.get('form_type') == 'callback':
        Callback.objects.create(name=request.POST.get('name'), phone=request.POST.get('phone'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))