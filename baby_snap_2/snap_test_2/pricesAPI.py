from models import SnapLocations, FoodPrices, Multipliers, StorePriceModel

TOO_HIGH = 2
TOO_LOW = .5
THRESHOLD = 8

def update_price_estimate(store_id, food_id, new_price_data):
    '''
    Assumes big model with a current price estimate ('price_estimate') 
    and list of user-inputted prices ('user_input)
    '''
    # Store the input data for future analysis
    UserDataModel(store_id=store_id, food_id=food_id, user_price=new_price_data).save()


    # Update current estimates.
    # Using a roundabout way to avoid unneeded database calls.
    data = StorePriceModel.object.get(store_id=store_id, food_id=food_id)
    current_estimate = data.users_mean #a float
    m = data.n
    n = m + 1
    if n >= THRESHOLD:
        if estimate_out_of_bounds(current_estimate, new_price_data):
            return "Estimate out of bounds"      
    else:
        store = SnapLocations.object.get(store_id=store_id)
        store_category = store.store_category
        price_level = store.price_level
        multiplier =  Multipliers.object.get(store_category=store_category, price_level=price_level)
        base_estimate = FoodPrices.object.get(food_id=food_id)   
        current_estimate =  (1 -(n/THRESHOLD))*(base_estimate*multiplier) +(n/THRESHOLD)*current_estimate  
        if not estimate_out_of_bounds(current_estimate, new_price_data):
            return "Estimate out of bounds" 
    print("Updating")
    data.users_mean =  (current_estimate*m + new_price_data)/n
    data.save()
    


def estimate_out_of_bounds(current_estimate, new_price_data):
    if current_estimate*TOO_HIGH < new_price_data or current_estimate*TOO_LOW > price_estimate:
        return True


def get_price_estimate(store_id, food_id):
    '''
    Assumes big model with a current price estimate ('price_estimate') 
    and list of user-inputted prices ('user_input)
    '''
   
    data = StorePriceModel.object.get(store_id=store_id, food_id=food_id)
    current_estimate = data.users_mean #a float
    n = data.n
    

    if n >= THRESHOLD:
        return current_estimate

    # This method requires more database calls, but avoids having to populate the 
    # giant database  everytime we change the multipliers formula.
    # an alternative to consider is cacheing data as the database is called.
    # We would have an additional column called stored_data and after running the
    # else statement .save() it to the model the first time this is ran.
    # On subsequent calls, we'd check for that number. If we substantially change our
    # estimates, we can flush the column.

    else: 
        store = SnapLocations.object.get(store_id=store_id)
        store_category = store.store_category
        price_level = store.price_level
        multiplier =  Multipliers.object.get(store_category=store_category, price_level=price_level)
        base_estimate = FoodPrices.object.get(food_id=food_id)
        return (1- (n/THRESHOLD))*(base_estimate*multiplier)+ (n/THRESHOLD)*mean(data.user_data)