#Donuts-and-Data-Division
#generate data for calculate food category/price weights

import random
from sklearn import linear_model 
import numpy as np
import math
#import statsmodels.api as sm
from snap_test_2.models import SnapLocations


#prices for each category type taken by field research

array = np.loadtxt("store_prices.csv", delimiter=",", skiprows=1)
def generate_set(array):
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

result = get_coefficients(array)



#X = sm.add_constant(X)
#results = sm.OLS(Y,X).fit()
#print(results.summary())

"""
add interaction terms
for c in [0,1]:
    for c2 in range(2,5):
        np.hstack(X, (X[c]*X[c2]).reshape
interactions.append(X[c]*X[c2])    
create list of list (1 list of 5 interaction variables per obs)
np.insert(X, 14 or X.shape[1], list, axis = 1)    

print(X)
run regression
Y is list of normalized prices
X is list of dummy values for categories and prices 
"""

def get_multiplier(cat, price):
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

# grab distinct categories and price levels from model and turn into list
qs_cats = SnapLocations.objects.values_list('store_category').distinct() 
qs_price_levels = SnapLocations.objects.values_list('price_level').distinct() 
categories = []
price_levels = [] 
for i in qs_cats:
    categories.append(i[0])
for i in qs_price_levels:
    price_levels.append(i[0])

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
        multipliers[cat][price] = get_multiplier(cat, price)
     



    
