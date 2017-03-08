#Donuts-and-Data-Division
#generate data for calculate food category/price weights

import random
from sklearn import linear_model 
import numpy as np
import math
import statsmodels.api as sm



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

constant = result["intercept_"]
coefficients = result["coef_"]
print (constant)
print (coefficients)


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

 