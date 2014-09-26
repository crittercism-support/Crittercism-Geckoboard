Crittercism-Geckoboard Integration
======================

This serves as a sample proof of concept to show some of the things the Crittercism API can do when combined with another BI tool. A screenshot of the Geckoboard dashboard can be seen here: [Click Me!]([Imgur](http://i.imgur.com/E7qOIjd.png).

This script utilizes the unirest and urllib2 libraries.

Please note: widgets/charts/graphs will first need to be generated via the Geckoboard portal, then you can push data using this script to each widget/chart/graph. Within the script you'll see notes on what type of widget/chart/graph will need to be generated ahead of time. Please e-mail me at ajohal@crittercism.com if you have any questions.


TODO List:
======================
* Fix/refine my Python code.
* Dynamic generation of Crittercism Access Token upon expiration.
* Add time series line/area graphs
* Adjust code to populate past data, currently data starts from the first day this script is run, meaning it can take some days/weeks for certain charts to fill up.
* Possibly add widget/chart/graph creation as a part of this script, so that you never need to manually create a new widget unless need be.
