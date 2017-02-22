from grocerylist.models import FoodPrices
import csv

csv_file = 'food_prices_cleaned_separated.csv'

with open(csv_file) as f:
    ls = list(csv.reader(f))
    for line in ls[1:]:
        food_name = line[1]
        food_quantity = line[2]
        food_price = line[3]
        date_last_updated = line[4]
        
        SnapLocations(food_name = food_name, food_quantity = food_quantity, \
        date_last_updated = date_last_updated).save()