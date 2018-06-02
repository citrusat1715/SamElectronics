from django.conf.urls import include, url
from django.contrib import admin
from polls import views as views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sam/', include('polls.urls')),
    url(r'^advanced_filters/', include('advanced_filters.urls')),
    url(r'^admin/polls/pos/(?P<objectId>[0-9]+)/change/',views.viewPos,name='viewPos'),
    url(r'^admin/polls/weekly/(?P<objectId>[0-9]+)/change/',views.viewWeekly,name='viewWeekly'),
    url(r'^admin/polls/monthly/(?P<objectId>[0-9]+)/change/',views.viewMonthly,name='viewMonthly'),
    url(r'^admin/polls/$',views.viewAdmin,name='admin'),
    

]


admin.site.search_form = 'admin/my_custom_search_form.html'
admin.autodiscover()
