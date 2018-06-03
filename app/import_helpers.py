from app.models import Weekly, POS,  Monthly,ImportHistory

def check_for_file_name_pos(file_name):
    v=ImportHistory.objects.filter(file_type='PosFile')
    for f in v:
     if f.file_name==file_name:
        return 'notunique'
    return 'unique'

        
def check_for_file_name_weekly(file_name):
    v=ImportHistory.objects.filter(file_type='WeeklyCTNFile')
    for f in v:
     if f.file_name==file_name:
        return 'notunique'
    return 'unique'
def check_for_file_name_monthly(file_name):
    v=ImportHistory.objects.filter(file_type='MonthlyTrailingFile')
    for f in v:
     if f.file_name==file_name:
        return 'notunique'
    return 'unique'
