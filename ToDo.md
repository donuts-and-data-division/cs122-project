#To Do

# Big things
## Main map
Ari: Make "Search" Work + Research AJAX -- write code to call google place API with place_id when querying (i.e. get hours information).

Joan: Make autocomplete and html work

Jazz: Continue wrangling with script to map retailers to google place_id, longitude and latitude, price level, type
	take care of multiple place IDs
	
desgin filters, write query logic for filtering


## Grocery list
Emma: Research AJAX, conceptualize the grocery list 

Jazz: categorize retailers when multiple types are returned

determine foods available for each types
design multipier algorithm (e.g. location/region, store type, google $$ etc)

adjust serving size (lb vs loaf)


## Nice additions
write script that automates price updating
write script that checks for changes in SNAP list.
create updatable form => way for user to save grocery list.

### Small things
Organize repository
~~Emma stops being Anne~~

## Notes from check-in 2/8/17
Farmer's market: Can turn street addresses to lat and long using google maps api
Record linkage: How close name and addresses are, make an overall score

Grocery list: 
Field research about multipliers for store types
Try it at one store and then do it at another store with our calculator

Add crowdsourcing. 
	If something is too far from our average, do sanity checks for outlier, or until two different users input the same price
	If we see that there are systematic errors for a store (ex: 20% off), maybe need to recalibrate everything
	Fuelbuddy for inspiration

Geolocating - maybe just use haversine formula

