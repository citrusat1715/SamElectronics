from django.contrib import admin
from polls.models import Weekly,Monthly,POS,ImportHistory
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.db.models import Q
import re
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.conf.urls import url
from polls import views
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
    def view_location_code(self, obj):
        return obj.location_code
##    def upper_case_name(obj):
##     return ("%s %s" % (obj.first_name, obj.last_name)).upper()
##    upper_case_name.short_description = 'Name'
    exclude = ('file_name',)
##    raw_id_fields = ['parent']
#    inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]
##    prepopulated_fields = {"slug": ("title",)}
##    search_fields = ['upc', 'title']

    def get_search_results(self, request, queryset, search_term):
        
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if ',' in search_term:
            
         search_term=search_term.replace(' ','')   
         search_term=list(search_term.split(','))
         queryset=self.model.objects.filter(imei__in=search_term)
         print(search_term)
        print(queryset)        
        return queryset, use_distinct            
          
    def remove_non_numeric_characters_and_convert_to_list(self,search_term):
      
        search_term=re.sub('[^0-9,]','', search_term)
            
        search_term=list(search_term.split(','))
        return search_term
class MonthlyAdmin( admin.ModelAdmin):
         change_list_template = "admin/monthly/change_list.html"
         advanced_filter_fields = (
        'imei', 'ctn','device_name','location_id','qualifying_activity_type','promotion_sale_price','promotion_category','imm_purchase_price','credit_amount')
        
         search_fields = ['imei']
         list_display = ('imei', 'location_id',  'ctn','credit_amount','qualifying_activity_type','activity_date','file_name')

class PosAdmin( admin.ModelAdmin):
         change_list_template = "admin/vendor/change_list.html"
       
         
   
         list_display=('product_name','invoiced_at','related_sn','file_name')
# Register your models here.

admin.site.register(Weekly,WeeklyAdmin)
admin.site.register(Monthly,MonthlyAdmin)
admin.site.register(POS,PosAdmin)
admin.site.register(ImportHistory)
