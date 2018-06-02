import csv
from polls.models import Weekly,Monthly,Vendor
from django.http import HttpResponse
from django.contrib.auth.models import User

def export_too_csv(request,x):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['IMEI', 'Location Code', 'Area Code', 'CTN'])
    print(x)

    weekly=Weekly.objects.filter(id__in=x).values_list('imei','location_code','ar_code','ctn')
    
    for w in weekly:
        print(w)
        writer.writerow(w)


    return response
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Weeklys')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Location Code', 'Area Code', 'IMEI', 'CTN ACTIVATION DATE', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Weekly.objects.filter(id__in=x).values_list('location_code', 'ar_code', 'imei', 'ctn_activation_date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num==3:
                ws.write(row_num, col_num, set_cell_date(row[col_num]), font_style)
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
