from snap_test_2.models import SnapLocations, FoodPrices, Multipliers, StorePriceModel,UserData

TOO_HIGH = 2
TOO_LOW = .5
THRESHOLD = 8

def update_price_estimate(store_id, food_id, new_price_data):
    '''
    Assumes big model with a current price estimate ('price_estimate') 
    and list of user-inputted prices ('user_input)
    '''
    # Store the input data for future analysis
    UserData(store_id=store_id, food_id=food_id, user_price=new_price_data).save()
    # Update current estimates.
    # Using a roundabout way to avoid unneeded database calls.
    try:
        data = get_StorePrice(store_id=store_id, food_id=food_id)

    except:
        return "Exception Raised store_id or food id not valid"

    current_estimate = data.users_mean #a float
    m = data.n
    n = m + 1
    if n >= THRESHOLD:
        if estimate_out_of_bounds(current_estimate, new_price_data):
            return "Estimate out of bounds"      
    else:
        store = SnapLocations.objects.get(store_id=store_id)
        store_category = store.store_category
        price_level = store.price_level
        multiplier =  Multipliers.objects.get(store_category=store_category, 
                                              price_level=price_level).multiplier
        # note FoodPrices is the one database where we use the auto generated id.

        base_estimate = FoodPrices.objects.get(id=food_id).food_price   
        current_estimate =  (1 -(n/THRESHOLD))*(base_estimate*multiplier) +(n/THRESHOLD)*current_estimate  
        if estimate_out_of_bounds(current_estimate, new_price_data):
            return "Estimate out of bounds" 
    print("Updating")
    data.n = n
    data.users_mean =  (current_estimate*m + new_price_data)/n
    data.save()



def get_StorePrice(store_id, food_id):
    '''
    On the fly database entry. If we've never looked up the store + food combo, 
    create a new entry. Then return the model instance.
.    '''
    try:
       data = StorePriceModel.objects.get(store_id=store_id, food_id=food_id)
    except:
        if not FoodPrices.objects.filter(id=food_id) or not SnapLocations.objects.filter(store_id=store_id):
            raise StorePriceModel.DoesNotExist
        StorePriceModel(store_id=store_id, food_id=food_id, n = 0, users_mean=0).save()
        #There's repeated code, but it means one fewer db call.
        data = StorePriceModel.objects.get(store_id=store_id, food_id=food_id)
    return data


def estimate_out_of_bounds(current_estimate, new_price_data):
    '''
    Test whether the estimate is "reasonable" based on our TOO_HIGH and TOO_LOW multipliers
    '''
    return (current_estimate*TOO_HIGH < new_price_data) or (current_estimate*TOO_LOW > new_price_data)


def get_price_estimate(store_id, food_id):
    '''
    Assumes big model with a current price estimate ('price_estimate') 
    and list of user-inputted prices ('user_input)
    '''
    print("I'm in")
    try:
        data = get_StorePrice(store_id=store_id, food_id=food_id)
        print("I got", data)
    except:
        return "Exception Raised store_id or food id not valid"
    

    current_estimate = data.users_mean #a float
    n = data.n
    print('N =',n)

    if n >= THRESHOLD:
        return round(current_estimate,2)

    # This method requires more database calls, but avoids having to populate the 
    # giant database  everytime we change the multipliers formula.
    # an alternative to consider is cacheing data as the database is called.
    # We would have an additional column called stored_data and after running the
    # else statement .save() it to the model the first time this is ran.
    # On subsequent calls, we'd check for that number. If we substantially change our
    # estimates, we can flush the column.

    else: 
        store = SnapLocations.objects.get(store_id=store_id)
        store_category = store.store_category
        price_level = store.price_level
        multiplier =  Multipliers.objects.get(store_category=store_category, price_level=price_level).multiplier
        base_estimate = FoodPrices.objects.get(id=food_id).food_price
        return round(((1- (n/THRESHOLD))*(base_estimate*multiplier) + 
                        (n/THRESHOLD)*current_estimate), 2)