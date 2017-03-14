from django.core.management.base import BaseCommand, CommandError
from pull_user_data import get_user_data
from price_weights import multipliers_dict
import numpy as np
from snap_test_2.models import Multipliers, SnapLocations

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        out_table = get_user_data()
        
        #Rearrange columns to match legacy code
        out_table = out_table[
        [0,1,"Grocery","Convenience Store","Gas Station","Other","$$","$$$","$"]
        ]
        array = np.array(out_table)

        qs = SnapLocations.objects.all()
        categories = {q.store_category for q in qs} 
        price_levels = {q.price_level for q in qs} 


        Multipliers.objects.all().delete()
        multipliers = multipliers_dict(array)
        for store_category in categories:
            for price_level in price_levels:
                multiplier = multipliers[store_category][price_level]    
                Multipliers(store_category=store_category, price_level=price_level, multiplier=multiplier).save()
