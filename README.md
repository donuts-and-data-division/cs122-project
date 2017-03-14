# Snap map

## Data Sources:
1) Snap Retailer Locations: https://www.fns.usda.gov/snap/retailerlocator
Downloaded 1/10/2017 as store_locations_IL.csv
Main retailer data source

2) Farmers markets with double value coupons: 
    http://www.dhs.state.il.us/page.aspx?item=44172
Farmer's Markets included in this source but not in the USDA database were added. In addition, those that accept double value coupons were matched with the USDA entry and flagged. The final results are in Snap_With_Markets.csv. 

3) Google Places API
Through snapmap2.py, we connect the data downloaded from 1) to the appropriate place ID, location, address, and cost category. We do this through an inital Nearby Search using the given address, followed by Searches using the given retailer name. The matched place ID is used in a Place Details search return information including formatted address and phone number.

If a retailer from 1) does not return any results from the Google API search, only the information from the original data source is included in the database. The same is done for retailers that return results considered a "bad match" based on a comparison of Google address and name vs original data source. 

Final results are in snapresultstestChicago2.csv. 

4) Yelp API
For retailers that were matched with Place ID's from Google and have phone numbers returned from the Place Details search, Yelp cost (ranging from $ to $$$$$) are added to retailer information.

5) Food prices: https://data.bls.gov/cgi-bin/dsrv?ap
Selected U.S. City Average, All food items (155 total selected), Dec 2016 price, filtered down to items with available pricing data

6) Field research: We visited seven stores of varying categories and price levels to record prices of available food items from the CPI list. The stores were: CVS on 53rd (convenience store $$), Hyde Park Produce (grocery $), Whole Foods (grocery $$$), BP (gas unknown), 7-eleven on 58 E Lake St. (convenience store $$), Open Produce (grocery $$), and Target (other $$). Recorded price points can be found [here](https://docs.google.com/spreadsheets/d/1XIhF04hT3vKJzueRmdIF5lUWUIPM8AxkgeCzGnTnn7c/edit?usp=sharing).

## File Descriptions
- building_price_model.py: Builds the StorePriceModel using the SnapLocations and FoodPrices models
- data_to_model.py: Transfers the record linkage results from snapresultsChicago2.csv into a Django model (model name: SnapLocations)
- placesAPI.py: Gets the bounding box for a given address in order to set the map
- price_weights.py: Process price points collected through fieldwork by simulation additional data points, running regression to estimate multipliers, and transferring multipliers into a Django model (model name: multiplier)
- pricesAPI.py: Retrieves and updates data from the StorePriceModel based on user inputs
- prices_to_model.py: Reads data from the csv into the FoodPrices model
- replace_field_data_to_model.py: Reads data from the csv into a Django model (model name: UserData)
- pull_user_data.py
- snapmap2.py: Connects the database to Places IDs
- farmers_markets.py: Web scraping of farmers markets from DHS website, including additional locations not in main retailer data source and double value coupon indicator
- linking_markets.py: Record linkage of scraped farmers market details to main retailer data source
- auto_multipliers.py: a management script that (in theory) automatically updates the multipliers
- crontab_text.txt: the crontab text that would run auto_multipliers.py every two weeks

## Links to policy related content:
*Original Snap maps*

[Inside Gov](http://snap-retailers.insidegov.com/#main)

[USDA "load balancer"](http://snap-load-balancer-244858692.us-east-1.elb.amazonaws.com/snap/main.swf?wmode=transparent)

*Farmer's Markets*

[Policy report about SNAP & Farmer's Markets (2010)](http://cclhdn.org/wp-content/uploads/2013/02/RealFoodRealChoice_SNAP_FarmersMarkets.pdf)


## Links to technical documents we utilized:
[Google Place Search documentation](https://developers.google.com/places/web-service/search)

[Google Maps API](https://developers.google.com/maps/documentation/javascript/importing_data#data)

[Google Autocomplete API for search field on website](https://developers.google.com/maps/documentation/javascript/places-autocomplete)

[requests] (http://docs.python-requests.org/en/master/)

[Django Girls Deploy a website](https://tutorial.djangogirls.org/en/deploy/)

[MarkDown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Django's [Geodjango tutorial](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/tutorial/)

Blog post on [geodjango with leaflet](http://blog.mathieu-leplatre.info/geodjango-maps-with-leaflet.html)

Recordlinkage documentation (http://recordlinkage.readthedocs.io/en/latest/about.html)
