import django_tables2 as tables
from .models import Person

class WeeklyTable(tables.Table):
    class Meta:
        model = Person
        template_name = 'django_tables2/bootstrap.html'
