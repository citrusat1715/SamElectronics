from app.models import Monthly,Weekly,POS
global v_fil
v_fil=''

#returns the common imeis and uncommon imeis, if no common only goees imei
def compare_file1_and_file3(w_file,v_file):
    w=Weekly.objects.filter(file_name=w_file)
    v=POS.objects.filter(file_name=v_file)
    imei=[imei for imei in w]
    common_values=v.filter(related_sn__in=imei)  
    i=[i for i in common_values]
    common_items=list(v.filter(related_sn__in=i).values_list('related_sn'))
    if len(common_values)==0:
        common_items='nocommons'    
    uncommon_items=list(v.exclude(related_sn__in=i).values_list('related_sn'))
    if len(uncommon_items)==0:
        uncommon_items='nouncommons'
    return common_items,uncommon_items

def compare_file2_and_file3(m_file,v_file):
    m=Monthly.objects.filter(file_name=m_file)
    v=POS.objects.filter(file_name=v_file) 
    imei=[imei for imei in m]
    common_values=v.filter(related_sn__in=imei)

    i=[i for i in common_values]
    common_items=list(v.filter(related_sn__in=i).values_list('related_sn'))
    if len(common_values)==0:
        common_items='nocommons'    
    uncommon_items=list(v.exclude(related_sn__in=i).values_list('related_sn'))
    if len(uncommon_items)==0:
        uncommon_items='nouncommons'

    return common_items,uncommon_items

def compare_all_files(w_file,m_file,v_file,c13,c23):
    w=Weekly.objects.filter(file_name=w_file)
    m=Monthly.objects.filter(file_name=m_file)
    v=POS.objects.filter(file_name=v_file)
    imei_monthly=[imei for imei in m]
    c13 = [item for sublist in c13 for item in sublist]
    c23=[item for sublist in c23 for item in sublist]
  
    for i in c23:
        c13.append(c23)
    listo=c13
    c12=w.filter(imei__in=imei_monthly)
    c12=[imei for imei in c12]
    c123=list(v.filter(related_sn__in=c12).values_list('related_sn'))
    uc123=list(v.exclude(related_sn__in=listo).values_list('related_sn'))
 
    if len(c123)==0:
        
        c123='nocommons'
        
    if len(uc123)==0:
        uc123='nouncommons'
    return c123,uc123
    
def compare(request,w,m,v):
    print(w,m,v)
    if 'v_file' in request.session:
        del request.session['v_file']
    request.session['v_file']=v
    common_items_b_file1_file3,uncommon_items_b_file1_file3=compare_file1_and_file3(w,v)
    common_items_b_file2_file3,uncommon_items_b_file2_file3=compare_file2_and_file3(m,v)
    common_items_b_all_files,uncommon_items_b_all_files=compare_all_files(w,m,v,common_items_b_file1_file3,common_items_b_file2_file3)
    common_uncommon_file1={'c13':common_items_b_file1_file3,'uc13':uncommon_items_b_file1_file3}
    common_uncommon_file2={'c23':common_items_b_file2_file3,'uc23':uncommon_items_b_file2_file3}
    common_uncommon_all={'c123':common_items_b_all_files,
         'uc123':uncommon_items_b_all_files}   
    return common_uncommon_file1,  common_uncommon_file2,common_uncommon_all

def generate_queryset(request,value):
    if value=='nocommons':
     
     return 'nocommons'
    elif value =='nouncommons':
     return 'nouncommons'
    v_file=request.session['v_file']
    flat_list = [item for sublist in value for item in sublist]
    v=POS.objects.filter(file_name=v_file)
    v=v.filter(related_sn__in=flat_list)
    return v


