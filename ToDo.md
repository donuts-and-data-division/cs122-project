Nice Powerpoint
Split up tasks know what we are saying.

#To Do
# Big things

## Joan updates 3/13
changed all references to auto --> home

can't easily change name snap_test_2 without redoing migrations, so I didn't do anything with that

Regarding pull_user_data integration with price_weights (hi Ari): not all categories show up in the pandas df from pull_user_data, presumably because users have not submitted prices for all category types and you used the get dummies method? That could be problematic because we want a standardized df coming out of that script. Could you modify it? Ideatlly it would output the same column order as the csv. I've written a few lines in price_weights to read in the pull_user_data output, but I'm not sure how to make this py file flexible enough for one time use (initial seeding of multipliers) as well as automated scriped. Probably something in __main__?

Dedup (hi Jazz): I've uploaded an Excel file that highlights all the duplicates.I think it makes more sense to dedup at the end of the snapmap2.py file. I'm not too familiar with your work in this file so maybe you can think of the most efficient way to do this, but we need to somehow set the Google columns blank for those specific duplicates.  

## Main map

Tuesday:
DEDUP
There are currently duplicate places (i.e. 2 Hyde Park Produce results) (maybe updating database will fix this)

Add about page
Add way to send us angry emails.

~~Hours string formatting in info window

Make URLs urls in info window

~~Change urls so map shows up without "auto" in the url.

Make scripts __name__ == "__main__": functions.?

Nice to have:
Hidable filters?

## Grocery list
determine foods available for each types

Add some instruction? (Perhaps instead of the cute snapmap, we can write "Make grocery list" 

## Operational things
update repo / clean up code
VM on flash drive

## Nice additions
write script that automates price updating -- write code that manipulates result from pull_user_data.py to match regression reqs
write script that checks for changes in SNAP list.
create updatable form => way for user to save grocery list.
adjust serving sizes (lb vs loaf)

### Small things
Organize repository
~~Emma stops being Anne~~

