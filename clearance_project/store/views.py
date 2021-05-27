from django.shortcuts import render
from django_filters import rest_framework as filters
from store.models import Products
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, generics, filters as rf_filters
from store.serializers import ProductSerializer



def index(request):
    brands = Products.objects.order_by('brand').values_list('brand', flat=True).distinct()
    brand_list = request.GET.getlist('brand')
    if brand_list:
        product_items = Products.objects.filter(brand__in=brand_list).order_by('discount').distinct()
    else:
        product_items = Products.objects.all()
    # product_filter = ProductFilter({'brand':'adidas'}, queryset=Products.objects.)
    # products = product_filter.qs
    print(request.GET.getlist('brand'))
    # products = Products.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(product_items, 60)
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
        
    return render(request, 'index.html', {'products':response, 
                                          'brands':brands,
                                          'filter': product_items
                                          })
    # brand = request.GET.get('brand')
    # products = Products.objects.all()
    # brand_filter = ProductFilter(request.GET, queryset=products)
    # qs = Products.objects.all()
    
    # paginator = Paginator(products, 60) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    
    


    # if is_valid_queryparam(brand):
    #     qs = qs.filter(brand=brand)
        
    # return  render(request, 'index.html', {'products':products, 'brands': brands,
    #                                        'page_obj': page_obj, 'filter': qs, })

def test(request):
    products = Products.objects.all()
    return render(request, 'test.html', {'data': products})