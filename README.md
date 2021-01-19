### mongodb_wiki_scraper
Script that fills up a Mongo database with Wikipedia page data for network analysis of associated links.

This assumes that you already have an empty mongodb cluster set up.

#### Once a mongodb cluster is created,
 1. Add a database
 2. Add a collection in that database
 3. Take note of the connection string


#### In wiki_scraper_tool.py,
#### Change the fields for:
`DB_NAME`
`COLLECTION_NAME`
`CONNECT_STRING `
