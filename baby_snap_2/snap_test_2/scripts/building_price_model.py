'''
Script to build StorePriceModel 
-- note we can reinitiated with or without running this code
because the model priceAPI file will automatically create new rows
'''

from snap_test_2.models import SnapLocations, FoodPrices, StorePriceModel

qs = SnapLocations.objects.all()
store_ids = [q.store_id for q in qs] ## will need to unpack query set

fs = FoodPrices.objects.all()
food_ids = [f.id for f in fs] ## will need to unpack query set

# When we limit food type by store type we can make this model smaller
# Get categories:
# [(q.store_ids, q.store_category) for q in qs]
# we'd also grab the filter columns from the FoodPrice model.

for store_id in store_ids:
    for food_id in food_ids:
        StorePriceModel(store_id= store_id, food_id=food_id, n=0, users_mean=0).save()


