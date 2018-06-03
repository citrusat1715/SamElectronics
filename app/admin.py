from django.contrib import admin
from app.models import Weekly,Monthly,POS,ImportHistory
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.db.models import Q
import re
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.conf.urls import url
from app import views
from mptt.admin import MPTTModelAdmin
admin.site.site_url='https://samelectronics.herokuapp.com/sam/home'



class WeeklyAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):

##    date_hierarchy = 'created_at'
    change_list_template = "admin/weekly/change_list.html"    
    list_display = ('location_code', 'ar_code',  'imei','activity','activation_commission','file_name','ctn_activation_date','commission_payout')    
    advanced_filter_fields = (
        'location_code', 'ar_code','mrc','imei','activity','activity_date','byod','ctn','mrc','port_type','ban','commission_payout','spif1','spif2','activation_commission','rrc')
    empty_value_display = '-empty-'
##    list_display_links = ('location_code',)    
    search_fields = ['imei']
          
          
class MonthlyAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
         change_list_template = "admin/monthly/change_list.html"
         advanced_filter_fields = (
        'imei', 'ctn','device_name','location_id','qualifying_activity_type','promotion_sale_price','promotion_category','imm_purchase_price','credit_amount')        
         search_fields = ['imei']
         list_display = ('imei', 'location_id',  'ctn','credit_amount','qualifying_activity_type','activity_date','file_name')

class PosAdmin(AdminAdvancedFiltersMixin,admin.ModelAdmin):
         change_list_template = "admin/pos/change_list.html"
         search_fields = ['related_sn']
         advanced_filter_fields = (
        'related_sn', 'tracking_number','product_name','related_product','sold_on','term_code','related_cost','invoiced_at','sales_person','file_name')      
         list_display=('related_sn', 'tracking_number','product_name','related_product','sold_on','term_code','related_cost','invoiced_at','sales_person','file_name')
# Register your models here.

admin.site.register(Weekly,WeeklyAdmin)
admin.site.register(Monthly,MonthlyAdmin)
admin.site.register(POS,PosAdmin)
admin.site.register(ImportHistory)




