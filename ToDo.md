#To Do

# Big things
## Main map
write script to map retailers to google place_id, longitude and latitude, price level, type
finish matching farmers market double value indicators to locations
Questions: 
Should we use record linkage to match multiple outputs?
What to do with imperfect matches (no results, more than one result)? Can we manually add in info if we have a few number of exceptions?

set up geoquery capabilities -- how to enter info into form, get geocoded location and then query database to get view.
Question: Suggestions on best way to do this? Do we need to use postgreSQL?

write code to call google place API with place_id when querying (i.e. get hours information).
design map / geoquety integration
desgin filters, write query logic for filtering


## Grocery list
categorize retailers when multiple types are returned
determine foods available for each types
design multipier algorithm (e.g. location/region, store type, google $$ etc)

create updatable form => way for user to save grocery list.
  * not doing this, may require user accounts

## Nice additions
write script that automates price updating
write script that checks for changes in SNAP list.

### Small things
~~Emma stops being Anne~~

