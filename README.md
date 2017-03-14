# Snap map

## Data Sources:
1) Snap Retailer Locations: https://www.fns.usda.gov/snap/retailerlocator
Downloaded 1/10/2017 as store_locations_IL.csv

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


## File Descriptions
- building_price_model.py
- data_to_model.py: Transfers the record linkage results from snapresultsChicago2.csv into a Django model (model name: SnapLocations)
- placesAPI.py
- price_weights.py: Process price points collected through fieldwork by simulation additional data points, running regression to estimate multipliers, and transferring multipliers into a Django model (model name: multiplier)
- pricesAPI.py
- prices_to_model.py
- replace_field_data_to_model.py
- pull_user_data.py

## Links to policy related content:
*Original Snap maps*

[Inside Gov](http://snap-retailers.insidegov.com/#main)

[USDA "load balancer"](http://snap-load-balancer-244858692.us-east-1.elb.amazonaws.com/snap/main.swf?wmode=transparent)

*Farmer's Markets*

[Policy report about SNAP & Farmer's Markets (2010)](http://cclhdn.org/wp-content/uploads/2013/02/RealFoodRealChoice_SNAP_FarmersMarkets.pdf)


*Nutritious, Delicious and Affordable*

[What's a serving (heart.org)](http://www.heart.org/HEARTORG/Caregiver/Replenish/WhatisaServing/What-is-a-Serving_UCM_301838_Article.jsp#.WIqWZvkrJhE)

[Fruit and Veg Prices (USDA)](https://www.ers.usda.gov/data-products/fruit-and-vegetable-prices/)

[Food Pyramid](https://www.cnpp.usda.gov/sites/default/files/archived_projects/FGPPamphlet.pdf)

## Links to technical documents:
[Our Page!](http://donutsanddatadivision.pythonanywhere.com/)

[Google Place Search documentation](https://developers.google.com/places/web-service/search)

[Google Maps API](https://developers.google.com/maps/documentation/javascript/importing_data#data)

[Google Autocomplete API for search field on website](https://developers.google.com/maps/documentation/javascript/places-autocomplete)

[requests] (http://docs.python-requests.org/en/master/)

[Django Girls Deploy a website](https://tutorial.djangogirls.org/en/deploy/)

[MarkDown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Django's [Geodjango tutorial](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/tutorial/)

Blog post on [geodjango with leaflet](http://blog.mathieu-leplatre.info/geodjango-maps-with-leaflet.html)

Recordlinkage documentation (http://recordlinkage.readthedocs.io/en/latest/about.html)
