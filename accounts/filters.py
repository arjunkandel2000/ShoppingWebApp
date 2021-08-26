from django.db.models import fields
import django_filters
from django_filters import DateFilter,CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet): # OrderFilter inheriting from django_filters
    start_date = DateFilter(field_name='date_created', lookup_expr='gte') # inheriting from above DateFilter and customizing date. lookup_expr='gte' gives greater or equal to date
    end_date = DateFilter(field_name='date_created', lookup_expr='gte')
    note = CharFilter(field_name='note' ,lookup_expr='icontains') # icontains ignore case-sensitiviry
    class Meta:
        model = Order
        fields = '__all__' # taking all the fields from Order model and if we want certain fileds we should make a list like below line
        exclude = [ 'customer', 'date_created'] # excluding the customer field and date_created fields in search form because we are in customer's page