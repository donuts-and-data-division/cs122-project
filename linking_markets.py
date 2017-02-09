import numpy
import pandas as pd
import jellyfish
import scipy
import sklearn
import numexpr
import recordlinkage as rl

markets_df = pd.read_csv('markets.csv') #need to update file name
snap_df = pd.read_csv('snap.csv') #need to update file name


initial_matches = rl.Pairs(markets_df, snap_df)

pairs = initial_matches.block('State') #need to reformat markets csv so that state and city are in separate columns

compare_df = rl.Compare(pairs, markets_df, snap_df)
compare_df.exact('name of city column in markets_df', 'name of city column in snap_df', name='City')
compare_df.string('name of market in markets_df', 'name of market in snap_df', method='jarowinkler', threshold=0.85)
compare_df.exact('name of state column in markets_df', 'name of state column in snap_df')


#Code below from example

'''
dfA, dfB = load_febrl4()
# Indexation step
pcl = rl.Pairs(dfA, dfB)
pairs = pcl.block('given_name')
# Comparison step
compare_cl = rl.Compare(pairs, dfA, dfB)
compare_cl.exact('given_name', 'given_name', name='given_name')
compare_cl.string('surname', 'surname', method='jarowinkler', threshold=0.85, name='surname')
compare_cl.exact('date_of_birth', 'date_of_birth', name='date_of_birth')
compare_cl.exact('suburb', 'suburb', name='suburb')
compare_cl.exact('state', 'state', name='state')
compare_cl.string('address_1', 'address_1', threshold=0.85, name='address_1')
# Classification step
matches = compare_cl.vectors[compare_cl.vectors.sum(axis=1) > 3]
print(len(matches))


c.string('name_a', 'name_b', method='jarowinkler', threshold=0.85)
c.exact('sex', 'gender')
c.date('dob', 'date_of_birth')
c.string('str_name', 'streetname', method='damerau_levenshtein', threshold=0.7)
c.exact('place', 'placename')
c.numeric('income', 'income', method='gauss', offset=3, scale=3, missing_value=0.5)
'''