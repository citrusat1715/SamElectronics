from pandas import DataFrame, read_csv
import re

import pandas as pd
import sys                                          #used to determine py ver
                               #used to check version no mat
import math
import numpy as np
import re
from dateutil.parser import parse
from datetime import datetime

def rename_weekly(df):
    df.rename(columns=lambda x:(x.replace(' ','_')).lower(),inplace=True)
    df.rename(columns={'sub-rank': 'sub_rank', 'spif_1_-_$50_rp': 'spif1','spif_2_-_autopay':'spif2','port_type_e/i/n':'port_type','commission__payout':'commission_payout'}, inplace=True)    
    df.replace('',np.nan,inplace=True)
    return df
def rename_monthly(df):
   df.rename(columns={'IMEI/ICCID':'IMEI'},inplace=True)
   print(df.columns)
   df.rename(columns=lambda x:(x.replace('\n',' ').replace(' ','_').replace('__','_')).lower(),inplace=True)
   
   df.replace('',np.nan,inplace=True)
   return df

def operation_numeric_weekly(df):
    #Manually the columns with numeric values are specified and manipulated via pandas operation tools.
    #'-' is converted to 0
    #$ and other non-numeric characters are removed
    
    #print(df[['ar_code','location_code','ban','ctn','imei','operator_id','sub_rank']].replace('-','0'))
 try:
  
    df['ar_code']=df['ar_code'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['location_code']=df['location_code'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['ban']=df['ban'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['ctn']=df['ctn'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['imei']=df.imei.apply(str)
    df['imei']=df['imei'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['operator_id']=df['operator_id'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['sub_rank']=df['sub_rank'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['mrc']=df['mrc'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['previous_mrc']=df['previous_mrc'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['rrc']=df['rrc'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['activation_commission']=df['activation_commission'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['plan_migration_commission']=df['plan_migration_commission'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['incremental_commission']=df['incremental_commission'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['retention_rate']=df['retention_rate'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['retention_rate_commission']=df['retention_rate_commission'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['spif1']=df['spif1'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['spif2']=df['spif2'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['national_retail_activation']=df['national_retail_activation'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['device_upgrade']=df['device_upgrade'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['device_return']=df['device_return'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['manual_transaction']=df['manual_transaction'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['manual_payment']=df['manual_payment'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['offset']=df['offset'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['mdf_payment']=df['mdf_payment'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['commission_payout']=df['commission_payout'].map(convert_to_numeric).map(remove_non_numeric_characters)

   
 except Exception as e:
     print(e)
     return e
    
 return df
    
def operation_numeric_monthly(df):
    #Manually the columns with numeric values are specified and manipulated via pandas operation tools.
    #'-' is converted to 0
    #$ and other non-numeric characters are removed
    
    #print(df[['ar_code','location_code','ban','ctn','imei','operator_id','sub_rank']].replace('-','0'))

    df['location_id']=df['location_id'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['ctn']=df['ctn'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['imei']=df.imei.apply(str)
    
    df['imei']=df['imei'].map(convert_to_numeric).map(remove_non_numeric_characters).map(myformat)
    df['promotion_sale_price']=df['promotion_sale_price'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['imm_purchase_price']=df['imm_purchase_price'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['credit_amount']=df['credit_amount'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['imm_invoice_number']=df['imm_invoice_number'].map(convert_to_numeric).map(remove_non_numeric_characters)


    return df
           
def convert_to_numeric(row):
    row=str(row)
    row=row.replace('-','0') 
    return row
def remove_non_numeric_characters(row):
 row=str(row)
 row=re.sub('[^0-9.]','', row) 
 return row

def drop_nulls(df):   
    df=df.dropna()
    
    return df

    ##All those rows where count of null is greater than 5 are dropped. Rows with null count less than 5 are kept, and nulls are replaced with '-'
def rename_pos(df):
 
   df.rename(columns=lambda x:(x.replace('\n',' ').replace(' ','_').replace('__','_')).replace('#','number').lower(),inplace=True)
   df.rename(columns={'vendorsku': 'vendor_sku'},inplace=True)
   df.replace('',np.nan,inplace=True)
   return df
def drop_nulls_pos(df):
  
    df=df.fillna('-')
    df=df.reset_index(drop=True)
    return df

    ##All those rows where count of null is greater than 10 are dropped. Rows with null count less than 5 are kept, and nulls are replaced with '-'

def operation_numeric_pos(df):
    #Manually the columns with numeric values are specified and manipulated via pandas operation tools.
    #'-' is converted to 0
    #$ and other non-numeric characters are removed
    
    #print(df[['ar_code','location_code','ban','ctn','imei','operator_id','sub_rank']].replace('-','0'))


    df['unit_rebate']=df['unit_rebate'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['partial_cb']=df['partial_cb'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['total_rebate']=df['total_rebate'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['collected']=df['collected'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['tax_amount']=df['tax_amount'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['balance']=df['balance'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['carrier_price']=df['carrier_price'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['related_cost']=df['related_cost'].map(convert_to_numeric).map(remove_non_numeric_characters)
    df['related_sn']=df.related_sn.apply(str)
    df['tracking_number']=df.tracking_number.apply(str)
    df['related_sn']=df['related_sn'].map(check_length_imei).map(convert_to_numeric).map(remove_non_numeric_characters).map(myformat)
    df['vendor_sku']=df.vendor_sku.apply(str)
    df['vendor_sku']=df['vendor_sku'].map(myformat)
    df['tracking_number']=df['tracking_number'].map(myformat)
    
    df['related_price']=df['related_price'].map(convert_to_numeric).map(remove_non_numeric_characters)

    return df
    
   

def clean_weekly_file(weekly_file):
 try:
    df=pd.DataFrame(weekly_file)

   
    df=operation_numeric_weekly(df)       
    df=drop_nulls(df)    
  
 except Exception as e:
     return e
 else:
     return df

def clean_monthly_file(monthly_file):
  try:
    df=pd.DataFrame(monthly_file)   
    df=operation_numeric_monthly(df)       
    df=drop_nulls(df)

  except Exception as e:
 
     return e
  else:
     return df

    

def clean_pos_file(file):
 try:
    df=pd.DataFrame(file)
    df=operation_numeric_pos(df)       
    df=drop_nulls_pos(df)
    df[['unit_rebate','partial_cb','collected','collected','tax_amount','balance','carrier_price','related_cost','related_cost','related_price']]=df[['unit_rebate','partial_cb','collected','collected','tax_amount','balance','carrier_price','related_cost','related_cost','related_price']].apply(pd.to_numeric) 
 except Exception as e:
     print(e)

     return e
 else:
     return df
   

def check_for_float(x):
   try:
     x=float(x)

   except ValueError:
      x=None
      return x
   else:
      return x

def check_length_imei(x):
    if len(x)<15:
      if len(x)!=0:
        diff=15-len(x)
        imei='0'*diff + x
        return imei
    return x

def check_for_date_time(datetime):

   date=''
   z=str(datetime)
   z=z.replace('/','-')
   try:
      parse(z)
   except (ValueError,TypeError):

      date='NULL'
  
      return date
   else:
      date=datetime.date()
      
   return date
def check_for_date(date):

   dat=''
   z=str(date)
   z=z.replace('/','-')
   try:
      parse(z)
   except (ValueError,TypeError):
      dat='NULL'  
      return dat
   else:
      pattern1=re.compile(r'^[0-9]{4}-(0[1-9]|1[1-2])-[0-9]{2}')
      pattern2=re.compile(r'^(0[1-9]|1[1-2])-[0-9]{2}-[0-9]{4}')
      pattern3=re.compile(r'^[0-9]{2}-(0[0-9]|1[1-2])-[0-9]{4}')
      if pattern1.match(z):
          dat=datetime.strptime(z, '%Y-%m-%d').strftime('%Y-%m-%d')

      elif pattern2.match(z):
          print(z)
          dat=datetime.strptime(z, '%m-%d-%Y').strftime('%Y-%m-%d')
          

      elif pattern3.match(z):
          dat=datetime.strptime(z, '%d-%m-%Y').strftime('%Y-%m-%d')

      else:
          dat='NULL'
   return dat
def clean_date(date):
    if date=='NULL':
        date=None
        return date
    return date
 
def myformat(x):
    x=x.replace('.0','')
    return x

    
##def equalize_the_list(d,):
##    sorted_d=sorted(l.items(), reverse=True,key=operator.itemgetter(1))
##    if len(m)==len(v)==len(w):
##        print(x)
##    else:
##        l=[len(m),len(v),len(w)]
##        l=l.sorted(reverse=True)
##        if len(m)>l:
##            for i in range(0,2):
##                m=Monthly.objects.
        
##p=[0,2,3]
##d=[0,2]
##c=[0,2,3]
##p.sort(reverse=True)
##l={'weekly':len(p),'monthly':len(d)}
##print(l)
##print(p)
##import operator
##sorted_l = sorted(l.items(), reverse=True,key=operator.itemgetter(1))
##print(sorted_l)
###find the length of each and add blank to the one with less values
##   
##x={'weekly':[x for x in p],'monthly':[x for x in d]}
