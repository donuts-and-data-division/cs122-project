import pandas as pd
import recordlinkage as rl

def get_matches():

    markets_df = pd.read_csv('Farmers_Markets.csv') 
    snap_df = pd.read_csv('store_locations_IL.csv') 

    initial_matches = rl.Pairs(markets_df, snap_df)
    pairs = initial_matches.block('City') 

    compare_df = rl.Compare(pairs, markets_df, snap_df)
    compare_df.exact('City', 'City')
    compare_df.string('Market Name', 'Store_Name', method='jarowinkler', threshold=0.85)
    compare_df.exact('State', 'State', name='State')
    compare_df.exact('Zipcode', 'Zip5', name='Zip')
    #compare_df.string('Address', 'Address', method='jarowinkler', threshold=0.85)

    matches = compare_df.vectors[compare_df.vectors.sum(axis=1) > 3]
    print(len(matches))
