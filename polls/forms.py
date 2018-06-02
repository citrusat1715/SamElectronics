from polls.models import Monthly
from django import forms



class MonthlyForm(forms.ModelForm):
    class Meta:
        model =Monthly
        fields = ['imei', 'activity_date','qualifying_activity_type','credit_amount','location_id','ctn']
