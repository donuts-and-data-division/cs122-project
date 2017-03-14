'''
Reads data from csv to models.UserData

Inputs: csv_file
'''

from snap_test_2.models import UserData
import csv

csv_file = 'store_prices_for_model.csv'

UserData.objects.all().delete()


with open(csv_file) as f:
    ls = list(csv.reader(f))
    for line in ls[1:]:
        user_price = line[0]
        food_id = line[1]
        store_id = line[2]
        
        UserData(user_price=user_price, food_id=food_id,store_id=store_id).save()

