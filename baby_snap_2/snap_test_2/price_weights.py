#Donuts-and-Data-Division
#generate data for calculate food category/price weights

import random
from sklearn import linear_model 
import numpy as np
import math
from snap_test_2.models import SnapLocations

#import statsmodel.api as sm



#prices for each category type taken by field research
'''
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
    #return array2
    array3 = np.concatenate((array, array2), axis=0)
    return array3


array3 = generate_set(array)
Y = []
for row in array3:
    val = math.log(row[0]/row[1])
    Y.append(val)
print(Y)
X = []
for row in array3:
    X.append(row[7:10])
     
X = sm.add_constant(X)
results = sm.OLS(Y,X).fit()
print(results.summary())
'''

#reg = linear_model.LinearRegression(fit_intercept=True)
#reg.fit(X, Y)
#returns array of coefficients
#print (reg.__dict__["intercept_"], reg.coef_)   

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

#reg = linear_model.LinearRegression(fit_intercept=True)
#reg.fit(X, Y)
#returns array of coefficients
#print (reg.coef_)


"""
all_items = [Grocery_1_apple, Grocery_2_apple, Grocery_3_apple, Grocery_1_banana, Grocery_2_banana, Grocery_3_banana, Grocery_1_pb, Grocery_2_pb, Grocery_3_pb, Grocery_1_chips, Grocery_2_chips, Grocery_3_chips, Gas_unknown_apple, Gas_unknown_banana, Gas_unknown_pb, Gas_unknown_chips, CS_2_apple, CS_2_banana, CS_2_pb, CS_2_chips]

def random_Y_set(food_categories = all_items):
    
    #Food categories is list of list where each list represents one item at one #location type
    
    all_Y = []
   
    for list in food_categories: 
        price = list[0]
        for i in range(10):
            add_price = price + random.uniform(-1,1)*0.2*price
            list.append(add_price)
        print (list)
        all_Y += list
    print (all_Y)
"""   

qs_cats = SnapLocations.objects.values_list('store_category').distinct() 
qs_price_levels = SnapLocations.objects.values_list('price_level').distinct() 
categories = []
price_levels = [] 
for i in qs_cats:
    categories.append(i[0])
for i in qs_price_levels:
    price_levels.append(i[0])

COEFF = reg.coef_
INTERCEPT = reg.intercept_
INTERCEPT_6 = 3 # made up number for $$$$/$$$$$ based on patterns from other dollar signs
print(cats)
print(price_levels)

multipliers = {}
for cat in categories:
    for price in price_levels:
        d[cat][price] = get_multiplier(cat, price)

def get_multiplier(cat, price):
    # helper function to calculate multiplier based on estimated regression coefficients
    
    d = {c: 0 for c in categories}
    d1 = {p: 0 for p in price_levels}
    d.update(d1)

    