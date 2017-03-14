import pandas as pd
import recordlinkage as rl
import farmers_markets

def get_matches(filename):
    """
    Match farmer's markets scraped from DHS website with retailers in USDA database. 
    Add missing retailers to comprehensive database and add double value column with T/F value. 
    """

    #create dataframes
    markets_df = pd.read_csv('Farmers_Markets_Final.csv') 
    snap_df = pd.read_csv('store_locations_2017_01_10.csv') 

    #create new columns in the snap dataframe
    snap_df['Double Value'] = False
    snap_df['Farmers Market?'] = False

    #get pairs
    initial_matches = rl.Pairs(markets_df, snap_df)
    pairs = initial_matches.block('City') 

    #compare
    compare_df = rl.Compare(pairs, markets_df, snap_df)
    compare_df.exact('City', 'City', name='City')
    compare_df.string('Market Name', 'Store_Name', method='jarowinkler', threshold=0.85, name='Market Name')
    compare_df.exact('State', 'State', name='State')
    compare_df.exact('Zipcode', 'Zip5', name='Zip')
    compare_df.string('Address', 'Address', method='jarowinkler', threshold=0.65, name="Address")

    matches = compare_df.vectors[compare_df.vectors.sum(axis=1) > 4]

    #update double value and farmers markets columns
    matched_markets = []
    for index, row in matches.iterrows():
        m, s = index
        matched_markets.append(m)
        if markets_df.ix[m, 'Double Value'] == True:
            snap_df.ix[s, 'Double Value'] = True
        snap_df.ix[s, 'Farmers Market?'] = True

    #add missing markets to final snap csv
    missing_markets = []
    for index, row in markets_df.iterrows():
        if index not in matched_markets:
            missing_market_dict = {}
            missing_market_dict['Store_Name'] = markets_df.ix[index]['Market Name']
            missing_market_dict['Longitude'] = markets_df.ix[index]['Longitude']
            missing_market_dict['Latitude'] = markets_df.ix[index]['Latitude']
            missing_market_dict['Address'] = markets_df.ix[index]['Address']
            missing_market_dict['Address Line #2'] = None
            missing_market_dict['City'] = markets_df.ix[index]['City']
            missing_market_dict['State'] = markets_df.ix[index]['State']
            missing_market_dict['Zip5'] = markets_df.ix[index]['Zipcode']
            missing_market_dict['Zip4'] = None
            missing_market_dict['County'] = None
            missing_market_dict['Double Value'] = markets_df.ix[index]['Double Value']
            missing_market_dict['Farmers Market?'] = True

            missing_markets.append(missing_market_dict)

    final = snap_df.append(missing_markets, ignore_index=True)
    final.to_csv(filename)

