# Snap map

##Data Sources:
1) Snap Retailer Locations: https://www.fns.usda.gov/snap/retailerlocator
Downloaded 1/10/2017

2) Google Places API
Through snapmap2.py, we connect the data downloaded from 1) to the appropriate place ID, location, address, and cost category. We do this through an inital Nearby Search using the given address, followed by Searches using the given retailer name. This information will later be used for Place Details requests that return information like formatted address and phone number.

Note: Need to decide how to handle requests that return no results and requests that return more than one results. Currently, the first 100 retailers in Illinois return 8 "none" and 19 "more than one".  


2) Food prices: https://data.bls.gov/cgi-bin/dsrv?ap
Selected U.S. City Average, All food items (155 total selected), Dec 2016 price, filtered down to items with available pricing data

3) Farmers markets with double value coupons:


##Links to policy related content:
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

