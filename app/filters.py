from django import forms
from app.models import Weekly,Monthly,POS
import django_filters
from django_filters import Filter,DateFromToRangeFilter
from django_filters.fields import Lookup




class ListFilter(Filter):
    def filter(self, qs, value):
        if value =='':
            return super(ListFilter, self).filter(qs, Lookup(value, 'in'))
        
        else:
           value_list=[]
           value=list(value)
           total_numbers=len(value)
           total_imeis=int(total_numbers/15)
           x=0
           for i in range(0,total_imeis):
            y=((i+1)*15)
            value_list.append(''.join(value[x:y]))
            x=y         
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))
class WeeklyFilter(django_filters.FilterSet):
    activity = django_filters.CharFilter(lookup_expr='icontains')
    imei = ListFilter(name='imei')
    ctn_activation_date__gt = django_filters.DateFilter(name='ctn_activation_date', lookup_expr='gte')
    ctn_activation_date__lt = django_filters.DateFilter(name='ctn_activation_date', lookup_expr='lte')
    commission_payout__gt = django_filters.NumberFilter(name='commission_payout', lookup_expr='gte')
    commission_payout__lt = django_filters.NumberFilter(name='commission_payout', lookup_expr='lte')
    location_code=django_filters.NumberFilter(name='location_code', lookup_expr='exact')
    class Meta:
        model =Weekly
        fields = ['imei', 'activity','ctn_activation_date','commission_payout','location_code']
        
class MonthlyFilter(django_filters.FilterSet):
    qualifying_activity_type = django_filters.CharFilter(name=' qualifying_activity_type',lookup_expr='icontains')
    imei = ListFilter(name='imei')
    activity_date__gt = django_filters.DateFilter(name='activity_date', lookup_expr='gte')
    activity_date__lt = django_filters.DateFilter(name='activity_date', lookup_expr='lte')
    credit_amount__gt = django_filters.NumberFilter(name='credit_amount', lookup_expr='gte')
    credit_amount__lt = django_filters.NumberFilter(name='credit_amount', lookup_expr='lte')
    location_id=django_filters.NumberFilter(name='location_id', lookup_expr='exact')
    ctn=django_filters.NumberFilter(name='ctn', lookup_expr='exact')
    class Meta:
        model =Monthly
        fields = ['imei', 'activity_date','qualifying_activity_type','credit_amount','location_id','ctn']
      

class PosFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(name='product_name',lookup_expr='icontains')
    related_product = django_filters.CharFilter(name='related_product',lookup_expr='icontains')
    invoiced_at=django_filters.CharFilter(name='invoiced_at',lookup_expr='icontains')
    related_sn = ListFilter(name='related_sn')
    tracking_number=django_filters.NumberFilter(name='tracking_number', lookup_expr='exact')
    
    class Meta:
        model =POS
        fields = ['related_sn', 'product_name','related_product','invoiced_at','tracking_number']
        

        
        
