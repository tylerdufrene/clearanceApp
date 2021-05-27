import django_filters
from django import forms
from store.models import Products
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES
from django_filters import Filter, FilterSet
from django_filters.fields import Lookup



class ProductFilter(FilterSet):
    brands = django_filters.ModelMultipleChoiceFilter(
    field_name='Products',
    to_field_name='brand',
    lookup_expr='in',
    queryset=Products.objects.all()    
    )
    sizes = django_filters.ModelMultipleChoiceFilter(
        field_name='Products',
        to_field_name='sizes',
        lookup_expr='in',
        queryset=Products.objects.all()
    )
    def show(self, value):
        return print(self.brands)
    class Meta:
        model = Products 
        fields = {'brand': ['exact','in'],
                  'sizes':['exact','in']}
    # other fields
        

        
        

