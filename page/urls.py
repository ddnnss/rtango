"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('category/<slug>/', views.category, name='category'),
    path('category/<slug>/<subcat_slug>', views.category, name='category'),
    path('category/<cat_slug>/<item_slug>/', views.item_page, name='item_page'),
    # path('subcategory/<subcat_slug>/', views.subcategory, name='subcategory'),
    path('one_click/', views.one_click, name='one_click'),
    path('search/', views.search, name='search'),
    path('about_us/', views.about_us, name='about_us'),
    path('contacts/', views.contacts, name='contacts'),
    path('dostavka/', views.dostavka, name='dostavka'),
    path('checkout/', views.checkout, name='checkout'),
    path('get_checkout/', views.get_checkout, name='get_checkout'),
    path('check_email/', views.check_email, name='check_email'),
    path('order/<order_code>', views.order, name='order'),
    path('robots.txt', views.robots, name='robots'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('payment/', views.payment, name='payment'),
    path('delivery/', views.delivery, name='delivery'),
    path('sber_success/', views.sber_success, name='sber_success'),
    path('sber_fail/', views.sber_fail, name='sber_fail'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout_page, name='logout'),
    # path('profile/<nickname_req>', views.profile, name='profile'),
    # path('del_message/', views.del_message, name='del_message'),
    # path('bonus_pack/', views.bonus_pack, name='bonus_pack'),
    # path('about_us/', views.about_us, name='about_us'),
    # path('rules/', views.rules, name='rules'),
    # path('add_to_player_balance/', views.add_to_player_balance, name='add_to_player_balance'),
    # path('about_bonus_pack/', views.about_bonus_pack, name='about_bonus_pack'),




    # path('statistic/', views.statistic, name='statistic'),

]
