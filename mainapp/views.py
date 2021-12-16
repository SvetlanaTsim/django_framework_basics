from django.shortcuts import render

from mainapp.models import Product


def products(request):
    title = 'каталог'
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    products_main = Product.objects.all()[::-1][:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'products_main': products_main,
    }
    return render(request, 'mainapp/products.html', context=context)
