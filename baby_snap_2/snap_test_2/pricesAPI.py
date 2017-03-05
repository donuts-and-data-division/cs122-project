from models import SnapLocations, FoodPrices

TOO_HIGH = 2
TOO_LOW = .5
THRESHOLD = 8

def update_price_estimate(store_id, food_id, new_price_data):
    '''
    Assumes big model with a current price estimate ('price_estimate') 
    and list of user-inputted prices ('user_input)
    '''
    #Probably use a different database ...
    data = FakeModel.object.get(store_id=store_id, food_id=food_id)
    current_estimate = data.price_estimate #a float

    if current_estimate*TOO_HIGH < new_price_data or current_estimate*TOO_LOW > price_estimate:
        return "Estimate out of bounds"


    current_user_data = data.user_input #a list or np array
    n = len(current_user_data)
    user_mean = mean(current_user_data)

    #reverse procedure to remember base_price (avoids call to database)
    base_price = (current_estimate - user_mean*(n/THRESHOLD)) / (1 - (n/THRESHOLD))
    '''
    # Alternatively
    store = SnapLocations.object.get(store_id =store_id)
    # All of these field names are made up....
    base_price = FoodPrices.object.get(store_type = store.store_type, price_level = store.price_level).price
    '''
    n += 1
    data.user_data += [new_price_data]

    if n >= THRESHOLD:
        data.price_estimate = mean(data.user_data)
    else:    
        data.price_estimate = (1- (n/THRESHOLD))*base_price + (n/THRESHOLD)*mean(data.user_data)
        
    data.save()
