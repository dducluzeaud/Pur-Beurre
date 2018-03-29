from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

from .models import Products


def index(request):
    return render(request, 'openfoodfacts/index.html')


def search(request):
    query = request.GET.get('query')

    # query match product_name
    category_p = Products.objects.filter(product_name__iexact=query).first()

    # query don't match exactly but can match product_name
    if not category_p:
        category_p = Products.objects.filter(product_name__icontains=query).first()

    # query doesn't match at all
    if not category_p:
        raise Http404
    else:
        products_list = Products.objects.filter(category=category_p.category)
        products_list = products_list.order_by('nutriscore')
        products_list = products_list.exclude(product_name=query)


    # Slices pages
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'paginate': True,
        'query': query,
        'title': category_p.product_name,
        'img': category_p.img
    }
    return render(request, 'openfoodfacts/search.html', context)

def detail(request, id_product):
    product = get_object_or_404(Products, pk=id_product)

    fat_index_img = ""
    saturated_fat_index_img = ""
    salt_index_img = ""
    sugar_index_img = ""
    url = "https://static.openfoodfacts.org/images/misc/"
    if product.fat < 3:
        fat_index_img = url + "low_30.png"
    elif 3 <= product.fat <20:
        fat_index_img = url + "moderate_30.png"
    else:
        fat_index_img = url + "high_30.png"

    if product.saturated_fat < 1.5:
        saturated_fat_index_img = url + "low_30.png"
    elif 1.5 <= product.saturated_fat < 5:
        saturated_fat_index_img = url + "moderate_30.png"
    else:
        saturated_fat_index_img = url + "high_30.png"

    if product.salt < 0.3:
        salt_index_img = url + "low_30.png"
    elif 0.3 <= product.salt < 1.5:
        salt_index_img = url + "moderate_30.png"
    else:
        salt_index_img = url + "high_30.png"

    if product.sugar < 5:
        sugar_index_img = url + "low_30.png"
    elif 5 <= product.sugar < 12.5:
        sugar_index_img = url + "moderate_30.png"
    else:
        sugar_index_img = url + "high_30.png"

    print(fat_index_img, "fat_index_img" )

    context = {
        "product": product.product_name,
        "img": product.img,
        "nutriscore": product.nutriscore,
        "fat": product.fat,
        "saturated_fat": product.saturated_fat,
        "salt": product.salt,
        "sugar": product.sugar,
        "fat_index_img": fat_index_img,
        "saturated_fat_index_img": saturated_fat_index_img,
        "salt_index_img": salt_index_img,
        "sugar_index_img": sugar_index_img,
        "redirection": product.url
    }
    return render(request, 'openfoodfacts/detail.html', context)
