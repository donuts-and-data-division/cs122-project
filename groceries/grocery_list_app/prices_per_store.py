import pandas as pd 
import csv

def get_df(filename):

    csv_foods = 'food_prices_cleaned_separated.csv'
    csv_stores = 'snap_with_fm_and_dv.csv'

    foods_df = pd.read_csv(csv_foods)
    stores_df = pd.read_csv(csv_stores)

    foods_df.set_index(['food_name'], inplace=True, drop = False)

    new_df = pd.DataFrame().append(stores_df['Store_Name']).transpose()

    foods = foods_df['food_name'].tolist()
    food_prices = foods_df['food_price'].tolist()

    final_df = new_df.append(pd.DataFrame(food_prices).transpose())

    final_df.columns = ['Store_Name'] + foods

    for column in final_df:
        if column != "Store_Name":
            final_df[column] = foods_df.ix[column]['food_price']

    final_df[:-1].to_csv(path_or_buf = filename)