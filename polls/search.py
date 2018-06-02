from polls.models import Weekly,POS,Monthly
import datetime
import dateutil.parser
import re
from django.utils.datastructures import MultiValueDictKeyError
def show_search_results(q,file,header):
    file=str(file).replace(' ',"").lower()
    header=str(header).replace(' ','_').lower()
    print(file,header)
    
    if 'choose' in file:
        return 'fielderror'
    elif 'choose' in header:
        return 'fielderror'
        
    if q=='':
     return 'emptysearch'


  
    file1=False
    file2=False
    file3=False
    all_file=False
    error=False
    if file=='file1':
        file1=True
    elif file=='file2':
        file2=True
    elif file=='file3':
        file3=True
    else:
        all_file=True
    if file1:
      queryset=''
      try:
        if header=='location_code':
            q=re.sub('[^0-9]','', q)
            try:
                q=int(q)
            except:
                error='error'
                return error
            queryset=Weekly.objects.filter(location_code=int(q))
        if header=='activity':
            queryset=Weekly.objects.filter(activity__icontains=str(q))
        if header=='imei':
            q=re.sub('[^0-9,]','', q)            
            if ',' in q:
                q=q.split(',')
                queryset=Weekly.objects.filter(imei__in=q)
            else:
                queryset=Weekly.objects.filter(imei=q)   
        if header=='ctn_activation_date':          
          q=str(q).replace(' ','')
          q=q.split('-')
          q=[q.replace('/','-') for q in q]
          start_date=q[0]
          end_date=q[1]
          queryset = Weekly.objects.filter(ctn_activation_date__gte=start_date,ctn_activation_date__lte=end_date)
          return queryset

##        if header=='commission_payout':
##            q=q.replace(' ','')
##            
##            q=q.split('-')
##
##            start=q[0]
##            end=q[1]
##            #<5.>5,5,=5-=9,
      except:
            return 'error'
      if len(queryset)==0:
            return 'noresults'
      return queryset    
           
    if file2:
        if header=='location_id':
           q=re.sub('[^0-9]','', q)
           try:
                q=int(q)
           except:
                error='error'
                return error
           queryset=Monthly.objects.filter(location_id=int(q))
           return queryset
        if header=='imei':
            q=re.sub('[^0-9,]','', q)
            
            if ',' in q:
                q=q.split(',')
                queryset=Monthly.objects.filter(imei__in=q)
                return queryset
            else:
                queryset=Monthly.objects.filter(imei=q)
                return queryset
        if header=='ctn':
            q=re.sub('[^0-9,]','', q)
            
            if ',' in q:
                q=q.split(',')
                queryset=Monthly.objects.filter(ctn__in=q)
                return queryset
            else:
                queryset=Monthly.objects.filter(ctn=q)
                return queryset

        if header=='qualifying_activity_type':
            queryset=Monthly.objects.filter(qualifying_activity_type__icontains=str(q))
            print(queryset)
            return queryset

        if header=='activity_date':
          
          q=str(q).replace(' ','')
          q=q.split('-')
          q=[q.replace('/','-') for q in q]
          start_date=q[0]
          end_date=q[1]
          queryset = Monthly.objects.filter(activity_date__gte=start_date,activity_date__lte=end_date)
          return queryset
        if header=='credit_amount':
         print('lolza')

                
    if file3:
        if header=='sold_on':
            print('')
           
        if header=='tracking_no':
           q=re.sub('[^0-9]','', q)
           try:
                q=int(q)
           except:
                error='error'
                return error
           queryset=POS.objects.filter(tracking_number=int(q))
           return queryset
        if header=='related_sn':
           q=re.sub('[^0-9,]','', q)
            
           if ',' in q:
                q=q.split(',')
                queryset=POS.objects.filter(related_sn__in=q)
                return queryset
           else:
                queryset=POS.objects.filter(related_sn=q)
                return queryset
           
            
            
        if header=='product_name':
         queryset=POS.objects.filter(product_name__icontains=str(q))
         print(queryset)
         return queryset
        if header=='related_product':
         queryset=POS.objects.filter(related_product__icontains=str(q))
         return queryset
         
        if header=='invoiced_at':
          
          
          queryset = POS.objects.filter(invoiced_at__icontains=str(q))
          return queryset


def normalize_querystring_weekly(querydict):
 try:
    l=querydict
    imei=l['imei']
    ctn_activation_date__gt=l['ctn_activation_date__gt']
    ctn_activation_date__lt=l['ctn_activation_date__lt']
    imei=re.sub('[^0-9,]','', imei)
    ctn_activation_date__gt=re.sub('[^0-9-]','',ctn_activation_date__gt)
    ctn_activation_date__lt=re.sub('[^0-9-]','',ctn_activation_date__lt)
    l['imei']=imei
    l['ctn_activation_date__gt']=ctn_activation_date__gt
    l['ctn_activation_date__lt']=ctn_activation_date__lt
 except MultiValueDictKeyError:
     pass

 return l

def normalize_querystring_monthly(querydict):
  try:
    l=querydict
    imei=l['imei']
    activity_date__gt=l['activity_date__gt']
    activity_date__lt=l['activity_date__gt']
    ctn=l['ctn']
    
    imei=re.sub('[^0-9,]','', imei)
    activity_date__gt=re.sub('[^0-9-]','',activity_date__gt)
    activity_date__lt=re.sub('[^0-9-]','',activity_date__lt)
    ctn=re.sub('[^0-9]','',ctn)
    
    l['imei']=imei
    l['activity_date__gt']=activity_date__gt
    l['activity_date__lt']=activity_date__lt
    l['ctn']=ctn
  except MultiValueDictKeyError:
      pass
  return l

def normalize_querystring_pos(querydict):
  try:
    l=querydict
    related_sn=l['related_sn']    
    related_sn=re.sub('[^0-9,]','', related_sn)    
    l['related_sn']=related_sn
  except MultiValueDictKeyError:
       pass
    
  return l        
