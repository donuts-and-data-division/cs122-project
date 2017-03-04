import django_tables2 as tables
from .models import SnapLocations

class ResultsTable(tables.Table):
    class Meta:
        model = SnapLocations
        attrs = {'id': 'results-table'}
        fields = ['googlename', 'googleaddress']

