from snap_test_2.models import SnapLocations, Multipliers, UserData, FoodPrices
import sqlite3
import os
import pandas as pd
import numpy as np
#from pa3


def get_user_data():
    DATA_DIR = os.path.dirname(__file__)
    DATABASE_FILENAME = os.path.join(DATA_DIR, 'geodjango.db')
    db = sqlite3.connect(DATABASE_FILENAME)
    c = db.cursor()

    query = "SELECT userdata.user_price,prices.food_price,places.store_category,\
             places.price_level FROM snap_test_2_userdata \
             AS userdata JOIN snap_test_2_foodprices AS prices \
             ON userdata.food_id == prices.id JOIN snap_test_2_snaplocations \
             AS places ON userdata.store_id==places.store_id"
    sql_args = [] 
    q = c.execute(query, sql_args)
    output = q.fetchall()
    #header = [clean_header(s) for s in get_header(c)]
    db.close()

    output = pd.DataFrame(output)
    store_dummies = pd.get_dummies(output[2]) 
    price_dummies = pd.get_dummies(output[3]) 

    return pd.concat((output.ix[:,0:1], store_dummies, price_dummies), axis = 1)
    

if __name__=="__main__":
    out_table = get_user_data()
    print("data is in 'out_table'" )