from grocery_list_app.models import FoodPrices
import csv

csv_file = 'food_prices_cleaned_separated.csv'

with open(csv_file) as f:
    ls = list(csv.reader(f))
    for line in ls[1:]:
        food_name = line[0]
        food_quantity = line[1]
        food_price = line[2]
        food_type = line[4]
        #date_last_updated = line[3]
        
        FoodPrices(food_name = food_name, food_quantity = food_quantity, \
            food_price = food_price, food_type = food_type).save()