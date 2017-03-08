from snap_test_2.models import SnapLocations, Multipliers, UserData, FoodPrices


data = UserData.objects.all()
# Unpack data into numpy array




qs = SnapLocations.objects.all()
categories = {q.store_category for q in qs} ## will need to unpack query set
price_levels = {q.price_level for q in qs} ## will need to unpack query set

for store_category in categories:
    if store_category == 'grocery':
        multiplier = 1.5
    else:
        multiplier = 1
    for price_level in price_levels:
        Multipliers(store_category=store_category, price_level=price_level, multiplier=multiplier).save()