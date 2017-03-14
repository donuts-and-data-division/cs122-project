#Donuts-and-Data-Division
#generate data for calculate food category/price weights

import random
from sklearn import linear_model 
import numpy as np
import math
from snap_test_2.models import SnapLocations, Multipliers
from pull_user_data import get_user_data

# get user data and turn into array
out_table = get_user_data()
out_table.columns = [] # DECLARE COLUMN NAMES HERE
array = np.array(out_table) # THIS SHOULD OVERWRITE THE FILE + ARRAY BELOW?

#prices for each category type taken by field research
FILE = "store_prices.csv"
array = np.loadtxt(FILE, delimiter=",", skiprows=1)

# import distinct categories and prices from Snap Locations
qs = SnapLocations.objects.all()
categories = {q.store_category for q in qs} 
price_levels = {q.price_level for q in qs} 

def generate_set(array):
    '''
    generate additional data to run regression
    '''
    array2 = []
    for row in array:
        price = row[0]
        rest = row[1:14]
        for i in range(10):
            new_price = price + random.uniform(-1,1)*0.2*price
            new_price = [new_price]
            new_price.extend(rest)
            array2.append(new_price)
    array3 = np.concatenate((array, array2), axis=0)
    return array3

def get_coefficients(array):
    '''
    run linear regression to estimate coefficients for price levels and store categories
    '''
    array3 = generate_set(array)
    Y = []
    
    #Y values as distance from CPI price
    for row in array3:
        val = math.log(row[0]/row[1])
        Y.append(val)
    
    #dummy variables for each categegory and price minus 1
    X = []
    for row in array3:
        X.append(row[5:10])

    reg = linear_model.LinearRegression(fit_intercept=True)
    reg.fit(X, Y)
    #returns dictionary that includes constant and coefficients
    return reg.__dict__

def get_multiplier(cat, price, INTERCEPT, COEFF):
    '''
    helper function to calculate multiplier based on estimated regression coefficients
    '''
    d = {c: 0 for c in categories}
    d1 = {p: 0 for p in price_levels}
    d.update(d1)

    # if price level is unavailable, treat is as $
    # assuming that Farmer's Markets have same multiplier as $$ Grocery Store
    if cat == "Farmer's Market":
        d['Grocery Store'] = 1
        d['$$'] = 1
    # assuming that Unknown store types have same multiplier as Other
    elif cat == 'Not available':
        d['Other'] = 1
        d[price] = 1
    else:
        d[cat] = 1
        d[price] = 1
    
    yhat = INTERCEPT \
        + COEFF[0]*d['Convenience Store'] \
        + COEFF[1]*d['Gas Station'] \
        + COEFF[2]*d['Other'] \
        + COEFF[3]*d['$$'] \
        + COEFF[4]*d['$$$'] \
        + COEFF[5]*d['$$$$'] 
    yhat = math.exp(yhat)
    return yhat

def multipliers_dict(array):
    '''
    build dictionary of multipliers to feed into model
    '''
    result = get_coefficients(array)
    INTERCEPT = result["intercept_"]
    COEFF = list(result["coef_"])
    COEFF_6 = 0.35 # made up number for $$$$/$$$$$ based on patterns from other dollar signs
    COEFF.append(COEFF_6)
    multipliers = {}
    for cat in categories:
        for price in price_levels:
            if multipliers.get(cat) is None: 
                multipliers[cat] = {}
            if multipliers[cat].get(price) is None:
                multipliers[cat][price] = {}
            multipliers[cat][price] = get_multiplier(cat, price, INTERCEPT, COEFF)
    return multipliers

# put multipliers into database/model
Multipliers.objects.all().delete()
multipliers = multipliers_dict(array)
for store_category in categories:
    for price_level in price_levels:
        multiplier = multipliers[store_category][price_level]    
        Multipliers(store_category=store_category, price_level=price_level, multiplier=multiplier).save()
    
