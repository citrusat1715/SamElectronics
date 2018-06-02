from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
class Weekly(models.Model):
    ar_code=models.CharField(max_length=200,blank=True,null=True)                     
    location_code=models.CharField(max_length=200,blank=True,null=True)               
    store_name=models.CharField(max_length=120,blank=True,null=True)                     
    activity=models.CharField(max_length=120,blank=True,null=True)                    
    ctn_activation_date= models.DateField(blank=True,null=True)            
    activity_date  = models.DateField(blank=True,null=True)               
    cancel_date= models.CharField(max_length=10,blank=True,null=True)                
    byod=models.CharField(max_length=2,blank=True,null=True)                       
    auto_pay=models.CharField(max_length=2,blank=True,null=True)                      
    port_type=models.CharField(max_length=23,blank=True,null=True)              
    ban=models.CharField(max_length=200,blank=True,null=True)                            
    ctn=models.CharField(max_length=200,blank=True,null=True)                          
    imei=models.CharField(max_length=200,blank=True,null=True)                            
    operator_id=models.CharField(max_length=200,blank=True,null=True)           
    sub_rank=models.CharField(max_length=200,blank=True,null=True)                       
    mrc=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                          
    previous_mrc=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)              
    rrc=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                    
    previous_rrc=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)             
    activation_commission=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)       
    plan_migration_commission=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)     
    incremental_commission=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)       
    retention_rate=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)               
    retention_rate_commission=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    spif1=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)  
    spif2=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)               
    national_retail_activation=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)     
    device_upgrade=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                
    device_return=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                  
    manual_transaction=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)           
    manual_payment=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                  
    offset=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                         
    mdf_payment=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)                     
    commission_payout=models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)              
    comment=models.TextField(blank=True)
    file_name=models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        verbose_name = 'VENDOR CTN DETAIL '
        verbose_name_plural = 'VENDOR CTN DETAIL  '
    
    
    def __str__(self):
        return str(self.imei)
    def get_absolute_url(self):
  
     return reverse('viewWeekly', kwargs={'objectId':self.id})

class Monthly(models.Model):
    location_id=models.CharField(max_length=200,blank=True,null=True)
    location_name=models.CharField(max_length=200,blank=True,null=True)
    activity_date=models.DateField(null=True,blank=True)
    imei=models.CharField(max_length=200,null=True,blank=True)
    ctn=models.CharField(max_length=200,null=True,blank=True)
    qualifying_activity_type=models.CharField(max_length=200,null=True, blank=True)
    product_sku=models.CharField(max_length=200,null=True,blank=True)
    device_name=models.CharField(max_length=200,null=True,blank=True)
    promotion_name=models.CharField(max_length=200,null=True,blank=True)
    promotion_start_date=models.DateField(null=True,blank=True)
    promotion_end_date=models.DateField(null=True,blank=True)
    promotion_category=models.CharField(max_length=200,blank=True,null=True)
    promotion_sale_price=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    imm_purchase_price=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    credit_amount=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    payment_date=models.DateField(null=True,blank=True)
    ship_date=models.DateField(null=True,blank=True)
    imm_invoice_number=models.CharField(max_length=200,null=True,blank=True)
    reason=models.CharField(max_length=200,null=True,blank=True)
    file_name=models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        verbose_name = 'VENDOR TRAILING CREDIT'
        verbose_name_plural = 'VENDOR TRAILING CREDIT'
        
    def __str__(self):
        return str(self.imei)
    def get_absolute_url(self):
  
     return reverse('viewMonthly', kwargs={'objectId':self.id})


class POS(models.Model):
    invoice_number=models.CharField(max_length=200,null=True,blank=True)
    tracking_number=models.CharField(max_length=200,null=True,blank=True)
    qty=models.CharField(max_length=200,null=True,blank=True)
    product_sku=models.CharField(max_length=200,null=True,blank=True)
    product_name=models.CharField(max_length=200,null=True,blank=True)
    unit_rebate=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    partial_cb=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    total_rebate=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    collected=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    balance=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    tax_amount=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    carrier_price=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    related_product=models.CharField(max_length=200,null=True,blank=True)
    related_sku=models.CharField(max_length=200,null=True,blank=True)
    related_sn=models.CharField(max_length=200,null=True,blank=True)
    related_cost=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    related_price=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    rate_plan=models.CharField(max_length=200,null=True,blank=True)
    rate_plan_2=models.CharField(max_length=200,null=True,blank=True)
    term_code=models.CharField(max_length=200,null=True,blank=True)
    customer=models.CharField(max_length=200,null=True,blank=True)
    sales_person=models.CharField(max_length=200,null=True,blank=True)
    sales_person_id=models.CharField(max_length=200,null=True,blank=True)
    sold_on=models.DateField(null=True,blank=True)
    invoiced_by=models.CharField(max_length=200,null=True,blank=True)
    invoiced_at=models.CharField(max_length=200,null=True,blank=True)
    original_invoice=models.CharField(max_length=200,null=True,blank=True)
    original_sales_date=models.CharField(max_length=200,null=True,blank=True)
    flagged=models.CharField(max_length=200,null=True,blank=True)
    reconciled=models.CharField(max_length=200,null=True,blank=True)
    reconciled_by=models.CharField(max_length=200,null=True,blank=True)
    reconciled_on=models.CharField(max_length=200,null=True,blank=True)
    adjusted=models.CharField(max_length=200,null=True,blank=True)
    charge_back=models.CharField(max_length=200,null=True,blank=True)
    journal_number=models.CharField(max_length=200,null=True,blank=True)
    contract_number=models.CharField(max_length=200,null=True,blank=True)
    customer_identifier=models.CharField(max_length=200,null=True,blank=True)
    comments=models.CharField(max_length=200,null=True,blank=True)
    comments_2=models.CharField(max_length=200,null=True,blank=True)
    soc_code=models.CharField(max_length=200,null=True,blank=True)
    soc_code_2=models.CharField(max_length=200,null=True,blank=True)
    extra_field=models.CharField(max_length=200,null=True,blank=True)
    zip_code=models.CharField(max_length=200,null=True,blank=True)
    region=models.CharField(max_length=200,null=True,blank=True)
    district=models.CharField(max_length=200,null=True,blank=True)
    vendor_account_name=models.CharField(max_length=200,null=True,blank=True)
    vendor_number=models.CharField(max_length=200,null=True,blank=True)
    vendor_sku=models.CharField(max_length=200,null=True,blank=True)
    scd_response=models.CharField(max_length=200,null=True,blank=True)
    file_name=models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        verbose_name = 'POS REBATE'
        verbose_name_plural = 'POS REBATE'

    def __str__(self):
        return str(self.related_sn)

    def get_absolute_url(self):
  
     return reverse('viewPos', kwargs={'objectId':self.id})



class ImportHistory(models.Model):
    file_type=models.CharField(max_length=25,blank=True,null=False)
    file_name=models.CharField(max_length=200,blank=True,null=False)
    import_date=models.DateField(auto_now_add=True)
    remarks=models.CharField(max_length=200,blank=False,null=False)
    count=models.IntegerField(null=False,blank=False)
    
    

    
