from django.conf.urls import include, url
from django.contrib import admin
from app import views as views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sam/', include('app.urls')),
    url(r'^advanced_filters/', include('advanced_filters.urls')),
    url(r'^admin/app/pos/(?P<objectId>[0-9]+)/change/',views.viewPos,name='viewPos'),
    url(r'^admin/app/weekly/(?P<objectId>[0-9]+)/change/',views.viewWeekly,name='viewWeekly'),
    url(r'^admin/app/monthly/(?P<objectId>[0-9]+)/change/',views.viewMonthly,name='viewMonthly'),
    url(r'^admin/app/$',views.viewAdmin,name='admin'),
    

]


admin.site.search_form = 'admin/my_custom_search_form.html'
admin.autodiscover()
