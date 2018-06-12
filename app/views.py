
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse

from django import forms
import django_excel as excel
from app.models import Monthly,Weekly,POS,ImportHistory
from app.comparison import generate_queryset,compare
from app.import_helpers import check_for_file_name_pos,check_for_file_name_weekly,check_for_file_name_monthly

from pandas import DataFrame, read_csv
import re

from app.helper import clean_weekly_file,clean_monthly_file,clean_pos_file,check_for_float,clean_date,myformat,rename_pos, rename_weekly,rename_monthly,check_for_date_time,check_for_date
from app.search import show_search_results,normalize_querystring_weekly,normalize_querystring_pos,normalize_querystring_monthly
import pandas as pd
import sys                                          #used to determine py ver
                                  #used to check version no mat
import math
import numpy as np
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render
from .filters import WeeklyFilter,PosFilter,MonthlyFilter
import csv
from django.http import HttpResponse
import json
from datetime import datetime

data = [
    [1, 2, 3],
    [4, 5, 6]
]


class UploadFileForm(forms.Form):
    file = forms.FileField()
    file_name=forms.CharField(max_length=200)
class SelectFileForm(forms.Form):
    option1 = forms.CharField(max_length=1)
    option2 = forms.CharField(max_length=1)
    option3 = forms.CharField(max_length=1)
    


# Create your views here.
class DateTimeEncoder(json.JSONEncoder):
    # default JSONEncoder cannot serialize datetime.datetime objects
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = obj.strftime('%s')
        else:
            encoded_object = super(self, obj)
        return encoded_object

class JsonResponse(HttpResponse):
    def __init__(self, content, mimetype='application/json', status=None, content_type='application/json'):
        json_text = json.dumps(content, cls=DateTimeEncoder)
        super(JsonResponse, self).__init__(
            content=json_text,
            status=status,
            content_type=content_type)
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                       'from your cloned repository:')
        })


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)


def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(
        data, file_type, file_name=file_name)


def home(request):



    return render (request, 'home.html')

def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_weekly_file(request):

    if 'file_name' in request.session:
        del request.session['file_name']
    if 'df' in request.session:
        del request.session['df']
                    
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
                          
        if form.is_valid():
            file=request.FILES['file']
            file_name=request.POST.get('file_name')        
            check=check_for_file_name_weekly(file_name)
            if check =='notunique':
             messages.error(request, 'Please Use a Unique Name')
             return redirect('import_weekly_file')
            
            file_name=(re.sub('[^0-9a-zA-Z]+', '', file_name))
            df=DataFrame(file.get_dict())

            df.columns=df.iloc[0]
            df=df.drop(df.index[[0]]).reset_index(drop=True).reindex()
            try:
                df=rename_weekly(df)
                df['ctn_activation_date']=df['ctn_activation_date'].map(check_for_date).astype(str)
                df['activity_date']=df['activity_date'].map(check_for_date).astype(str)
                df['cancel_date']=df['activity_date'].map(check_for_date).astype(str)
            except:
                      messages.error(request, 'UPLOAD FAILED. MAKE SURE THE FILE HAS CORRECT HEADERS')
                      return redirect('import_weekly_file')
                        
            
            df=df.to_dict()
            request.session['df']=df
            request.session['file_name']=file_name
            action='clean'
            return redirect('upload_weekly_data', action )        
           

    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {'form': form})
def import_monthly_file(request):

      if 'file_name' in request.session:
         del request.session['file_name']
      if 'df' in request.session:
        del request.session['df']
                    
      if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)                          
        if form.is_valid():
            file=request.FILES['file']
            file_name=request.POST.get('file_name')        
            check=check_for_file_name_monthly(file_name)
            if check =='notunique':
             messages.error(request, 'Please Use a Unique Name')
             return redirect('import_monthly_file')
            file_name=(re.sub('[^0-9a-zA-Z]+', '', file_name))            
            df=DataFrame(file.get_dict())
            df.columns=df.iloc[0]
            df=df.drop(df.index[[0]]).reset_index(drop=True).reindex()
            df=rename_monthly(df)
            try:
           
                df['activity_date']=df['activity_date'].map(check_for_date).astype(str)
                df['promotion_start_date']=df['promotion_start_date'].map(check_for_date).astype(str)
                df['promotion_end_date']=df['promotion_end_date'].map(check_for_date).astype(str)
                df['ship_date']=df['ship_date'].map(check_for_date).astype(str)
                df['payment_date']=df['payment_date'].map(check_for_date).astype(str)
            except:
                messages.error(request, 'UPLOAD FAILED. MAKE SURE THE FILE HAS CORRECT HEADERS')
                return redirect('import_monthly_file')
            df=df.to_dict()
                        

            request.session['df']=df
            request.session['file_name']=file_name
            action='clean'
            return redirect('upload_monthly_data', action )        
      else:
        form = UploadFileForm()
      return render(
        request,
        'upload_form.html',
        {'form': form})

def import_pos_file(request):
      if 'file_name' in request.session:
         del request.session['file_name']
      if 'df' in request.session:
        del request.session['df']
                    
      if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)                          
        if form.is_valid():
            file=request.FILES['file']
            file_name=request.POST.get('file_name')
            check=check_for_file_name_pos(file_name)
            if check =='notunique':
             messages.error(request, 'Please Use a Unique Name')
             return redirect('import_pos_file')
            file_name=(re.sub('[^0-9a-zA-Z]+', '', file_name))
            df=DataFrame(file.get_dict())
            
 
            df.columns=df.iloc[1]
            df=df.drop(df.index[[0,1]]).reset_index(drop=True).reindex()
            try:
                df=rename_pos(df)            
                df['sold_on']=df['sold_on'].map(check_for_date_time)
                df['sold_on']=df['sold_on'].astype(str)            
                df['original_sales_date']=df['original_sales_date'].astype(str)
            except:
                messages.error(request, 'UPLOAD FAILED. MAKE SURE THE FILE HAS CORRECT HEADERS')
                return redirect('import_pos_file')
           
            df=df.to_dict()
            i=0

                       
            request.session['df']=df
            request.session['file_name']=file_name
            action='clean'
            return redirect('upload_pos_data', action )     
            
        else:
             error=str(df)
            
             return render(
                 request,
                 'upload_form.html',
                 {'upload_error': df})
            
      else:
        form = UploadFileForm()
      return render(
        request,
        'upload_form.html',
        {'form': form})
def upload_weekly_data(request,action):
    if action=='clean':        
     df=request.session['df']
     df=clean_weekly_file(df)     
     if (type(df).__name__)=='DataFrame':        
         action='import'
         df=df.to_dict('dict')
         request.session['dicto']=df
         print(df['imei'])

         return redirect('upload_weekly_data', action)
     else:
      e=df
      error='UPLOAD FAILED DUE TO WRONG FILE FORMAT. PLEASE CHECK THE FILE AND TRY AGAIN. ERROR KEYWORD:'+e
      messages.error(error)  
      return redirect('import_weekly_file')

    
    if action =='import':
         listo=request.session['dicto']        
         rows=len(listo['imei'])
        
         ob=[]
         file_name=request.session['file_name']
   
         for i in range(0,rows):
          i=str(i)
          try:
             ob.append(Weekly(file_name=file_name,ar_code=listo['ar_code'][i],location_code=listo['location_code'][i],store_name=listo['store_name'][i],
             activity=listo['activity'][i],ctn_activation_date=clean_date(listo['ctn_activation_date'][i]),
             activity_date=clean_date(listo['activity_date'][i]),cancel_date=clean_date(listo['cancel_date'][i]),
             byod=listo['byod'][i],auto_pay=listo['auto_pay'][i],port_type=listo['port_type'][i],ban=listo['ban'][i],
             ctn=listo['ctn'][i],imei=listo['imei'][i],operator_id=listo['operator_id'][i],sub_rank=listo['sub_rank'][i],
             mrc=listo['mrc'][i],previous_mrc=listo['previous_mrc'][i],rrc=listo['rrc'][i],previous_rrc=listo['previous_rrc'][i],
             activation_commission=listo['activation_commission'][i],plan_migration_commission=listo['plan_migration_commission'][i],
             incremental_commission=listo['incremental_commission'][i],retention_rate=listo['retention_rate'][i],
             retention_rate_commission=listo['retention_rate_commission'][i],spif1=listo['spif1'][i],spif2=listo['spif2'][i],
             national_retail_activation=listo['national_retail_activation'][i],device_upgrade=listo['device_upgrade'][i],
             device_return=listo['device_return'][i],manual_transaction=listo['manual_transaction'][i],
             manual_payment=listo['manual_payment'][i],offset=listo['offset'][i],mdf_payment=listo['mdf_payment'][i],
             commission_payout=listo['commission_payout'][i],comment=listo['comment'][i]))
          except ValidationError:
                continue                
         try:
            with transaction.atomic():
                Weekly.objects.bulk_create(ob)
                   
         except Exception as e:
            errors='Errors'+str(e)
            messages.error(request,errors)
            return redirect('import_weekly_file')

         else:
             i=ImportHistory(file_type='WeeklyCTNFile',file_name=file_name,count=rows,remarks='Successful')
             i.save()
             messages.success(request, 'File Imported Successfully successful')
             return redirect('/admin/app/weekly')

     
def upload_monthly_data(request,action):  
    if action=='clean':        
     df=request.session['df']
     
     df=clean_monthly_file(df)
    
     
     
     if (type(df).__name__)=='DataFrame':
        
         action='import'
         df=df.to_dict('dict')
         request.session['dicto']=df
         return redirect('upload_monthly_data', action)
     else:

      e=str(df)
      error='UPLOAD FAILED DUE TO WRONG FILE FORMAT. PLEASE CHECK THE FILE AND TRY AGAIN. ERROR KEYWORD:'+e
      messages.error(error)  
      return redirect('import_monthly_file')

    if action =='import':
         listo=request.session['dicto']
         rows=len(listo['imei'])
         ob=[]
         file_name=request.session['file_name']
     
         for i in range(0,rows):
          i=str(i)
          try:
            file_name=request.session['file_name']
            ob.append(Monthly(file_name=file_name,location_id=listo['location_id'][i],location_name=listo['location_name'][i],activity_date=clean_date(listo['activity_date'][i]),imei=listo['imei'][i],ctn=listo['ctn'][i],qualifying_activity_type=listo['qualifying_activity_type'][i],product_sku=listo['product_sku'][i],device_name=listo['device_name'][i],promotion_name=listo['promotion_name'][i],promotion_start_date=clean_date(listo['promotion_start_date'][i]),promotion_end_date=clean_date(listo['promotion_end_date'][i]),promotion_category=listo['promotion_category'][i],promotion_sale_price=listo['promotion_sale_price'][i],imm_purchase_price=listo['imm_purchase_price'][i],credit_amount=listo['credit_amount'][i],payment_date=clean_date(listo['payment_date'][i]),ship_date=clean_date(listo['ship_date'][i]),imm_invoice_number=listo['imm_invoice_number'][i],reason=listo['reason'][i]))
    
          except ValidationError:
                continue                
         try:
            with transaction.atomic():
                Monthly.objects.bulk_create(ob)
                   
         except Exception as e:
            errors='Errors'+str(e)
            messages.errors(request,errors)
            return redirect('import_monthly_file')
         else:
             i=ImportHistory(file_type='MonthlyTrailingFile',file_name=file_name,count=rows,remarks='Successful')
             i.save()
             
             messages.success(request, 'File Imported Successfully successful')
             return redirect('/admin/app/monthly')


def upload_pos_data(request,action):
    if action =='clean':
     df=request.session['df']
     
     df=clean_pos_file(df)     
     if (type(df).__name__)=='DataFrame':
        action='import'
        df=df.to_dict('dict')
   
        request.session['dicto']=df
        return redirect('upload_pos_data', action)
     else:
      e=str(df)
      error='UPLOAD FAILED DUE TO WRONG FILE FORMAT. PLEASE CHECK THE FILE AND TRY AGAIN. ERROR KEYWORD:'+e
      messages.error(request,error)  
      return redirect('import_pos_file')
    
    if action =='import':

         listo=request.session['dicto']
         rows=len(listo['related_sn'])
         ob=[]
         file_name=request.session['file_name']
         
         for i in range(0,rows):
          i=str(i)
          try:
                ob.append(POS(
                file_name=file_name,invoice_number=listo['invoice_number'][i],tracking_number=listo['tracking_number'][i],qty=listo['qty'][i],product_sku=listo['product_sku'][i],
                product_name=listo['product_name'][i],unit_rebate=check_for_float(listo['unit_rebate'][i]),partial_cb=check_for_float(listo['partial_cb'][i]),
                total_rebate=check_for_float(listo['total_rebate'][i]),collected=check_for_float(listo['collected'][i]),balance=check_for_float(listo['balance'][i]),
                tax_amount=check_for_float(listo['tax_amount'][i]),carrier_price=check_for_float(listo['carrier_price'][i]),related_product=listo['related_product'][i],
                related_sku=listo['related_sku'][i],related_sn=(listo['related_sn'][i]),related_cost=check_for_float(listo['related_cost'][i]),
                related_price=check_for_float(listo['related_price'][i]),rate_plan=listo['rate_plan'][i],rate_plan_2=listo['rate_plan_2'][i],term_code=listo['term_code'][i],
                customer=listo['customer'][i],sales_person=listo['sales_person'][i],sales_person_id=listo['sales_person_id'][i],
                invoiced_by=listo['invoiced_by'][i],invoiced_at=listo['invoiced_at'][i],original_invoice=listo['original_invoice'][i],
                original_sales_date=listo['original_sales_date'][i],flagged=listo['flagged'][i],reconciled=listo['reconciled'][i],
                reconciled_by=listo['reconciled_by'][i],reconciled_on=listo['reconciled_on'][i],adjusted=listo['adjusted'][i],charge_back=listo['charge_back'][i],
                journal_number=listo['journal_number'][i],contract_number=listo['contract_number'][i],sold_on=clean_date(listo['sold_on'][i]),customer_identifier=listo['customer_identifier'][i],
                comments=listo['comments'][i],comments_2=listo['comments_2'][i],soc_code=listo['soc_code'][i],soc_code_2=listo['soc_code'][i],extra_field=listo['extra_field'][i],zip_code=listo['zip_code'][i],
                region=listo['region'][i],district=listo['district'][i],vendor_account_name=listo['vendor_account_name'][i],vendor_number=listo['vendor_number'][i],vendor_sku=listo['vendor_sku'][i],
                scd_response=listo['scd_response'][i]))
          except ValidationError:
                continue                
         try:
            with transaction.atomic():
                POS.objects.bulk_create(ob)
                   
         except Exception as e:
            errors='Errors'+str(e)
            messages.error(request,errors)
            return redirect('import_pos_file')
         else:
             i=ImportHistory(file_type='PosFile',file_name=file_name,remarks='Successful',count=rows,import_date=datetime.now())
             i.save()

             messages.success(request, 'File Imported Successfully successful')
             return redirect('/admin/app/pos')
def choose_files_to_compare(request):


    m=list(Monthly.objects.values_list('file_name',flat=True).distinct())

    w=list(Weekly.objects.values_list('file_name',flat=True).distinct())
    v=list(POS.objects.values_list('file_name',flat=True).distinct())
    if request.method=="POST":
  
     w=request.POST.get('weekly_field')
     v=request.POST.get('vendor_field')
     m=request.POST.get('monthly_field')
     c_un_1,c_un_2,c_un_all=compare(request,w,m,v)
     if 'file1' in request.session:
         del request.session['file1']
     if 'file2' in request.session:
         del request.session['file2']
     if 'file3' in request.session:
         del request.session['file3']
     request.session['file1']=c_un_1
     request.session['file2']=c_un_2
     request.session['file3']=c_un_all    
     method='common'
     file='file1'
     return redirect('comparison_results', method,file) 
    return render(
        request,
        'choose_compare.html',
        {'weekly':w,'monthly':m,'vendor':v})
def display_comparison_results(request,method,file):
    if file=='file1':
        results=request.session['file1'] 
        if method=='common':
            results=generate_queryset(request,results['c13'])
            if request.method=="POST":
             if results!='nocommons':
                op=[i.pk for i in results]              
                request.session['export']=op
                return redirect ('export','pos')
             else:
                 messages.error(request,'EXPORT FAILED.TRY AGAIN WITH A VALID QUERYSET')
                 return redirect(request.META.get('HTTP_REFERER'))
            display='COMMON IMEIS BETWEEN POS REBATE AND VENDOR CTN DETAIL'
            none='NO COMMON IMEIS BETWEEN POS REBATE AND VENDOR CTN DETAIL'
            if results=='nocommons':
             return render(request,'comparison_results.html',{'none':none,'display':display})
            return render(
                request,
                'comparison_results.html',
                {'results':results,'display':display}
                )
        if method=='uncommon':
            results=generate_queryset(request,results['uc13'])
            if request.method=="POST":
             if results!='nouncommons':
                 
              op=[i.pk for i in results]              
              request.session['export']=op
              return redirect ('export','pos')
             else:
                 messages.error(request,'EXPORT FAILED.TRY AGAIN WITH A VALID QUERYSET')
                 return redirect(request.META.get('HTTP_REFERER'))
            display='UNIQUE IMEIS BETWEEN POS REBATE AND VENDOR CTN DETAIL'
            none='NO UNIQUE IMEIS BETWEEN POS REBATE AND VENDOR CTN DETAIL'
            if results=='nouncommons':
             return render(request,'comparison_results.html',{'none':none,'display':display})
            return render(
                request,
                'comparison_results.html',
                {'results':results,'display':display}
                )
    if file=='file2':
        results=request.session['file2'] 
        if method=='common':
            results=generate_queryset(request,results['c23'])
            if request.method=="POST":
             if results!='nocommons':
              op=[i.pk for i in results]              
              request.session['export']=op
              return redirect ('export','pos')
             else:
                 messages.error(request,'EXPORT FAILED.TRY AGAIN WITH A VALID QUERYSET')
                 return redirect(request.META.get('HTTP_REFERER'))
            display='COMMON IMEIS BETWEEN POS REBATE AND VENDOR TRAILING CREDIT'
            none='NO COMMON IMEIS BETWEEN POS REBATE AND VENDOR TRAILING CREDIT'
            if results=='nocommons':
             return render(request,'comparison_results.html',{'none':none,'display':display})
            return render(
                request,
                'comparison_results.html',
                {'results':results,'display':display}
                )
        if method=='uncommon':
            results=generate_queryset(request,results['uc23'])
            if request.method=="POST":
             if results!='nouncommons':
                 
              op=[i.pk for i in results]              
              request.session['export']=op
              return redirect ('export','pos')
             else:
                 messages.error(request,'EXPORT FAILED.TRY AGAIN WITH A VALID QUERYSET')
                 return redirect(request.META.get('HTTP_REFERER'))
            display='UNIQUE IMEIS BETWEEN POS REBATE AND VENDOR TRAILING CREDIT'
            none='NO UNIQUE IMEIS BETWEEN POS REBATE AND VENDOR TRAILING CREDIT'
            if results=='nouncommons':
             return render(request,'comparison_results.html',{'none':none,'display':display})
            return render(
                request,
                'comparison_results.html',
                {'results':results,'display':display}
                )
    if file=='all':
        results=request.session['file3'] 
        if method=='common':
            results=generate_queryset(request,results['c123'])       
            if request.method=="POST":
             if results!='nocommons':
              op=[i.pk for i in results]              
              request.session['export']=op
              return redirect ('export','pos')
             else:
                 messages.error(request,'EXPORT FAILED.TRY AGAIN WITH A VALID QUERYSET')
                 return redirect(request.META.get('HTTP_REFERER'))
                
            display='COMMON IMEIS BETWEEN ALL FILES '
            none='NO COMMON IMEIS BETWEEN ALL FILES'
            if results=='nocommons':
             return render(request,'comparison_results.html',{'none':none,'display':display})
            return render(
                request,
                'comparison_results.html',
                {'results':results,'display':display}
                )
        if method=='uncommon':
            results=generate_queryset(request,results['uc123'])
            if request.method=="POST":
             if results!='nouncommons':                 
              op=[i.pk for i in results]              
              request.session['export']=op
              return redirect ('export','pos') 
             else:
                 messages.error(request,'EXPORT FAILED.TRY AGAIN WITH A VALID QUERYSET')
                 return redirect(request.META.get('HTTP_REFERER'))
            display='UNIQUE IMEIS BETWEEN ALL FILES'
            none='NO UNIQUE IMEIS BETWEEN ALL FILES'
            
            if results=='nouncommons':
             return render(request,'comparison_results.html',{'none':none,'display':display})
            return render(
                request,
                'comparison_results.html',
                {'results':results,'display':display}
                )
        

def results(request, template_name="asdl.html"):
    
    if request.method=="POST":
        q = request.POST.get('q', '')
        field1 = request.POST.get('field1', '')
        field2 = request.POST.get('field2', '')
        x=show_search_results(q,field1,field2)
        file=str(field1).replace(' ',"").upper()
        if x =='error':
            error='INVALID SEARCH. TRY AGAIN AND MAKE SURE THAT YOU FOLLOW THE SEARCH GUIDELINES'
            return render(request,'comparison_results.html', {'error':error})
        elif x =='filederror':
            error='PLEASE CHOOSE ALL THE FIELDS TO SEARCH.TRY AGAIN'
            return render(request,'comparison_results.html' ,{'error':error})
        elif x=='emptysearch':
            error='PLEASE ENTER THE VALUE TO SEARCH.TRY AGAIN'
            return render(request,'comparison_results.html' ,{'error':error})
        elif x=='noresults':
            noresults='NO RESULTS FOUND FOR THE QUERY. TRY CHANGING VALUE'
            return render(request,'comparison_results.html', {'noresults':noresults,'file':file})
        else:
            return render(request,'comparison_results.html', {'results':x,'file':file})
        
    return render(
        request,
        'asd1.html')
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def search(request,file):

    if file =='file1':            
        l=normalize_querystring_weekly(request.GET.copy())
        weekly_list = Weekly.objects.all()    
        weekly_filter = WeeklyFilter(l, queryset=weekly_list)
        print(weekly_filter)
        if request.method=='POST':
         x=[x.id for x in weekly_filter.qs]
         request.session['export']=x
         return redirect ('export','weekly')
        
        return render(request, 'filter_weekly.html', {'filter': weekly_filter})

            
       
        
    if file=='file2':
        l=normalize_querystring_monthly(request.GET.copy())
        monthly_list = Monthly.objects.all()    
        monthly_filter = MonthlyFilter(l, queryset=monthly_list)
        if request.method=='POST':
         x=[x.id for x in monthly_filter.qs]
   
         request.session['export']=x
         return redirect('export','monthly')
        return render(request, 'filter_monthly.html', {'filter': monthly_filter})
    if file=='file3':
        l=normalize_querystring_pos(request.GET.copy())
        POS_list = POS.objects.all()    
        POS_filter = PosFilter(l, queryset=POS_list)
        if request.method=='POST':
         x=[x.id for x in POS_filter.qs]
         request.session['export']=x
         return redirect('export','pos')
        return render(request, 'filter_pos.html', {'filter': POS_filter})
    if file=='all':
       q=request.GET.get('q')
       header=request.GET.get('header')
       request.session['q']=q
       request.session['header']=header

       if header=='CTN': 
        q=re.sub('[^0-9]','',q)
        w=Weekly.objects.filter(ctn=q)
        v=POS.objects.filter(tracking_number=q)
        m=Monthly.objects.filter(ctn=q)
        if len(m)==0 and len(w)==0 and len(v)==0:
            display='NO RESULTS FOUND IN THREE FILES'
            return render(request, 'filter_all.html',
                     {'w':w,'m':m,'v':v,'display':display})
        display='RESULTS FOUND. CHOOSE THE FILE TO DISPLAY RESULTS'
        return render(request, 'filter_all.html',
                     {'w':w,'m':m,'v':v,'display':display})
       
       if header=='IMEI':
        q=re.sub('[^0-9]','',q)
        value_list=[]
        value=list(q)
        total_numbers=len(value)
        total_imeis=int(total_numbers/15)
        x=0
        for i in range(0,total_imeis):
         y=((i+1)*15)
         value_list.append(''.join(value[x:y]))
         x=y
        w=Weekly.objects.filter(imei__in=value_list)
        v=POS.objects.filter(related_sn__in=value_list)
        m=Monthly.objects.filter(imei__in=value_list)
        if len(m)==0 and len(w)==0 and len(v)==0:
            display='NO RESULTS FOUND IN THREE FILES'
            return render(request, 'filter_all.html',
                     {'w':w,'m':m,'v':v,'display':display})
        display='RESULTS FOUND. CHOOSE THE FILE TO DISPLAY RESULTS'
        return render(request, 'filter_all.html',
                     {'w':w,'m':m,'v':v,'display':display})
        
       if header=='ACTIVITY':
        q=re.sub('\+',' ',q)       
        w=Weekly.objects.filter(activity__icontains=q)
        v=POS.objects.filter(term_code__icontains=q)
        m=Monthly.objects.filter(qualifying_activity_type__icontains=q)
        
        if len(m)==0 and len(w)==0 and len(v)==0:
            display='NO RESULTS FOUND IN THREE FILES'
            return render(request, 'filter_all.html',
                     {'w':w,'m':m,'v':v,'display':display})
        display='RESULTS FOUND. CHOOSE THE FILE TO DISPLAY RESULTS'
        return render(request, 'filter_all.html',
                     {'w':w,'m':m,'v':v,'display':display})
       
       return render(request, 'filter_all.html'
                     )

def export_data(request, file):

    if file=='weekly':
        queryset=''
        column_names = ['ar_code' ,'location_code' ,'store_name' ,'activity' ,'ctn_activation_date' ,'activity_date' ,'cancel_date' ,'byod' ,'auto_pay' ,'port_type' ,'ban' ,'ctn' ,'imei' ,'operator_id' ,'sub_rank' ,'mrc' ,'previous_mrc' ,'rrc' ,'previous_rrc' ,'activation_commission' ,'plan_migration_commission' ,'incremental_commission' ,'retention_rate' ,'retention_rate_commission' ,'spif1' ,'spif2' ,'national_retail_activation' ,'device_upgrade' ,'device_return' ,'manual_transaction' ,'manual_payment' ,'offset' ,'mdf_payment' ,'commission_payout' ,'comment']
        s=str(request.META.get('HTTP_REFERER'))
        if 'search/all' in s:
            header= re.search('header=(.*)&', s)            
            value= re.search('q=(.*)$', s)
            try:
             header=header.group(1)
             value=value.group(1)             
            except:
                messages.error(request,'PLEASE TRY AGAIN WITH VALID QUERYSET TO EXPORT')
                return redirect(request.META.get('HTTP_REFERER'))
            if header=='CTN':
             value=re.sub('[^0-9]','',value)
             print(value)
             queryset=Weekly.objects.filter(ctn=value)
             print(queryset)
            if header=='IMEI':
             value=re.sub('[^0-9]','',value)
             queryset=Weekly.objects.filter(imei=value)
             
            if header=='ACTIVITY':
             value=re.sub('\+',' ',value)

             queryset=Weekly.objects.filter(activity__icontains=value)
             
        else:
         x=request.session['export']
         queryset=Weekly.objects.filter(id__in=x)
        return excel.make_response_from_query_sets(queryset,column_names,'xls', file_name="customWeeklyCTNfile")
    if file=='monthly':
        queryset=''
        column_names=['location_id' ,'location_name' ,'activity_date' ,'imei' ,'ctn' ,'qualifying_activity_type' ,'product_sku' ,'device_name' ,'promotion_name' ,'promotion_start_date' ,'promotion_end_date' ,'promotion_category' ,'promotion_sale_price' ,'imm_purchase_price' ,'credit_amount' ,'payment_date' ,'ship_date' ,'imm_invoice_number' ,'reason']
        s=str(request.META.get('HTTP_REFERER'))
        if 'search/all' in s:
            try:
                header= re.search('header=(.*)&', s)
                header=header.group(1)
                value= re.search('q=(.*)$', s)
                value=value.group(1)
            except:
                 messages.error(request,'PLEASE TRY AGAIN WITH VALID QUERYSET TO EXPORT')
                 return redirect(request.META.get('HTTP_REFERER'))
            if header=='CTN':
             value=re.sub('[^0-9]','',value)
             queryset=Monthly.objects.filter(ctn=value)
            if header=='IMEI':
             value=re.sub('[^0-9]','',value)
             queryset=Monthly.objects.filter(imei=value)
            if header=='ACTIVITY':
             value=re.sub('\+',' ',value)             
             queryset=Monthly.objects.filter(qualifying_activity_type__icontains=value)
        else:
           x=request.session['export']
           queryset=Monthly.objects.filter(id__in=x)
        return excel.make_response_from_query_sets(queryset,column_names,'xls', file_name="customMonthlyTrailingfile")
    if file=='pos':
         queryset=''
         column_names=['invoice_number' ,'tracking_number' ,'qty' ,'product_sku' ,'product_name' ,'unit_rebate' ,'partial_cb' ,'total_rebate' ,'collected' ,'balance' ,'tax_amount' ,'carrier_price' ,'related_product' ,'related_sku' ,'related_sn' ,'related_cost' ,'related_price' ,'rate_plan' ,'rate_plan_2' ,'term_code' ,'customer' ,'sales_person' ,'sales_person_id' ,'sold_on' ,'invoiced_by' ,'invoiced_at' ,'original_invoice' ,'original_sales_date' ,'flagged' ,'reconciled' ,'reconciled_by' ,'reconciled_on' ,'adjusted' ,'charge_back' ,'journal_number' ,'contract_number' ,'customer_identifier' ,'comments' ,'comments_2' ,'soc_code' ,'soc_code_2' ,'extra_field' ,'zip_code' ,'region' ,'district' ,'vendor_account_name' ,'vendor_number' ,'vendor_sku' ,'scd_response']
         s=str(request.META.get('HTTP_REFERER'))
         print(s)
         if 'search/all' in s:
            header= re.search('header=(.*)&', s)
            try:
                header=header.group(1)
                value= re.search('q=(.*)$', s)
                value=value.group(1)
            except:
                messages.error(request,'PLEASE TRY AGAIN WITH VALID QUERYSET TO EXPORT')
                return redirect(request.META.get('HTTP_REFERER'))
            if header=='CTN':
             value=re.sub('[^0-9]','',value)
             
             queryset=POS.objects.filter(tracking_number=value)
            if header=='IMEI':
             value=re.sub('[^0-9]','',value)
             queryset=POS.objects.filter(related_sn=value)
            if header=='ACTIVITY':
             value=re.sub('\+',' ',value)
             queryset=POS.objects.filter(term_code__icontains=value)
         else:
          x=request.session['export']
          queryset=POS.objects.filter(id__in=x)
         return excel.make_response_from_query_sets(queryset,column_names,'xls', file_name="customPOSfile")
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")
           

  
def files(request, ftype):
## wf=Weekly.objects.values_list('file_name').distinct()
## wf=[i for x in wf for i in x]
 wf=ImportHistory.objects.filter(file_type='WeeklyCTNFile')
 vf=ImportHistory.objects.filter(file_type='PosFile')
 mf=ImportHistory.objects.filter(file_type='MonthlyTrailingFile')

 

 if ftype=='weekly':
        display='Weekly CTN Files'
        print(ftype)
        return render(request, 'files.html',{'files':wf,'display':display,'ftype':ftype}
                     )
 if ftype=='monthly':
     display='Monthly Trailing Files'


     return render(request, 'files.html',{'files':mf,'display':display,'ftype':ftype})
 if ftype=='pos':
     display='POS Files'
     return render(request, 'files.html',{'files':vf,'display':display,'ftype':ftype})
def delete(request,ftype,fname,template_name='delete.html'):
  if request.method=='POST':
    if request.POST.get('Yes'):
     if ftype=='weekly':
         Weekly.objects.filter(file_name=fname).delete()
         ImportHistory.objects.filter(file_type='WeeklyCTNFile').filter(file_name=fname).delete()
     if ftype=='monthly':
        Monthly.objects.filter(file_name=fname).delete()
        ImportHistory.objects.filter(file_type='MonthlyTrailingFile').filter(file_name=fname).delete()
     if ftype=='pos':
         POS.objects.filter(file_name=fname).delete()
         ImportHistory.objects.filter(file_type='PosFile').filter(file_name=fname).delete()
     referer=request.session.get('referer')
     return redirect(referer)
    else:
        referer=request.session.get('referer')
        return redirect(referer)
        
  else:
      if 'referer' in request.session:
          del request.session['referer']
      referer=request.META.get('HTTP_REFERER')
      request.session['referer']=referer
  return render(request, template_name, {'fname':fname})
  
    
def viewPos(request, objectId):
    return redirect('viewPos', objectId=objectId)


def viewWeekly(request, objectId):
    return redirect('viewWeekly', objectId=objectId)
def viewMonthly(request, objectId):
    return redirect('viewMonthly', objectId=objectId)
def viewAdmin(request):
    return redirect('admin')



    


