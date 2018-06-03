from django.conf.urls import url
from app import views as views



urlpatterns = [

   
    url(r'^home/', views.home, name="home"),
    url(r'^Import-Vendor-Ctn-Detail-File/', views.import_weekly_file, name="import_weekly_file"),
    url(r'^Import-Vendor-Trailing-Credit-File/', views.import_monthly_file, name="import_monthly_file"),
    url(r'^Import-Pos-Rebate-File/', views.import_pos_file, name="import_pos_file"),
    url(r'^choose-files-to-compare/', views.choose_files_to_compare, name="choose_files_to_compare"),   
    url(r'^results',views.results, name='search_results'),
     url(r'^search/(?P<file>\w+)$',views.search, name='search'),
    url(r'^Import-Vendor-Ctn-Detail-Data/(?P<action>\w+)$',views.upload_weekly_data, name='upload_weekly_data'),
    url(r'^import-Vendor-Trailing-Credit-Data/(?P<action>\w+)$',views.upload_monthly_data, name='upload_monthly_data'),
    url(r'^import-Pos-Rebate-data/(?P<action>\w+)$',views.upload_pos_data, name='upload_pos_data'),
    url(r'^uploadedfiles/(?P<ftype>\w+)$',views.files, name='files'),
    url(r'^delete/(?P<ftype>\w+)/(?P<fname>.+)$',views.delete,name='delete'),
     url(r'^comparison/results/(?P<method>\w+)/(?P<file>\w+)$',views.display_comparison_results,name='comparison_results'),    
    url(r'^export/(?P<file>\w+)', views.export_data, name="export"),


  
]
