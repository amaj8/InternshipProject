# Flipkart_data_extractor
So extract.py basically
* fiddles around with Flipkart's URL by appending the filters
* uses selenium to extract dynamic JS data from the site
* uses BeautifulSoup to parse the data
* runs chrome in headless mode using xvfb and pyvirtualdisplay

One has to provide the requirements/filters in a dict and pass to the Flip class and create a new object. Then call the extract and the print functions.
Useful if you have a system that extracts requirements from the user which you can then pass to this, although it's kinda slow. 
