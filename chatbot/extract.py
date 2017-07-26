import urllib
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import html5lib

from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

"""
chrome_options = Options()  
chrome_options.add_argument("--headless")  
"""

GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = Options()
chrome_options.binary_location = GOOGLE_CHROME_BIN
chrome_options.add_argument("--headless")
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

#filter strings to be used in Flipkart's url


class Flip:
	def __init__(self,req):
		self.req = req
		self.filters = {'company':'facets.brand%5B%5D=','price_from':'facets.price_range.from=','price_to':'facets.price_range.to=','ram':'facets.ram%5B%5D=','os':'facets.operating_system%5B%5D=',
		'network':'facets.network_type%5B%5D=','screen_size':'facets.screen_size%5B%5D=', 'min_screen_size':'facets.screen_size%5B%5D=', 'max_screen_size':'facets.screen_size%5B%5D=',
		'battery':'facets.battery_capacity%5B%5D=','camera':'facets.primary_camera%5B%5D=','memory':'facets.internal_storage%5B%5D='}
	#creates a nice list of params to be included in Flipkart's url
	def create_filters(self):
		#if price_to is in req but price_from is not then must set price_from as 'Min'
		if 'price_to' in self.req and 'price_from' not in self.req:
			self.req['price_from'] = 'Min'
		#Append units i.e. GB to ram size if it's given in the user requirements
		try:
			if self.req['ram']:
				self.req['ram'] += '%2BGB'
		except KeyError:
			pass

		#Fix screen size. For Flipkart screen size has to be in ranges. Absolute values not allowed
		try:
			ss = self.req['screen_size']
			ss = float(ss)
			if ss < 3:
				ss = "Less+than+3 inch"
			elif 3<= ss <= 3.4:
				ss = "3+-+3.4 inch"
			elif 3.5 <= ss <= 3.9:
				ss = "3.5+-+3.9 inch"
			elif 4 <= ss <= 4.4:
				ss = "4+-+4.4 inch"
			elif 4.5 <= ss <= 4.9:
				ss = "4.5+-+4.9 inch"
			elif 5 <= ss <= 5.1:
				ss = "5+-+5.1+inch"
			elif 5.2 <= ss <= 5.4:
				ss = "5.2+-+5.4 inch"
			elif 5.5 <= ss <= 5.6:
				ss = "5.5+-+5.6 inch"
			elif 5.7 <= ss <= 5.9:
				ss = "5.7+-+5.9 inch"
			elif ss >=6:
				ss = "6+inch+&+above"

			self.req['screen_size'] = str(ss)

		except (KeyError,ValueError):
			pass


		#Fix min screen size. For Flipkart screen size has to be in ranges. Absolute values not allowed
		try:
			ss = self.req['min_screen_size']
			ss = float(ss)
			if ss < 3:
				ss = "Less+than+3 inch"
			elif 3<= ss <= 3.4:
				ss = "3+-+3.4 inch"
			elif 3.5 <= ss <= 3.9:
				ss = "3.5+-+3.9 inch"
			elif 4 <= ss <= 4.4:
				ss = "4+-+4.4 inch"
			elif 4.5 <= ss <= 4.9:
				ss = "4.5+-+4.9 inch"
			elif 5 <= ss <= 5.1:
				ss = "5+-+5.1+inch"
			elif 5.2 <= ss <= 5.4:
				ss = "5.2+-+5.4 inch"
			elif 5.5 <= ss <= 5.6:
				ss = "5.5+-+5.6 inch"
			elif 5.7 <= ss <= 5.9:
				ss = "5.7+-+5.9 inch"
			elif ss >=6:
				ss = "6+inch+&+above"

			self.req['min_screen_size'] = str(ss)

		except (KeyError,ValueError):
			pass

		#Fix max screen size. For Flipkart screen size has to be in ranges. Absolute values not allowed
		try:
			ss = self.req['max_screen_size']
			ss = float(ss)
			if ss < 3:
				ss = "Less+than+3 inch"
			elif 3<= ss <= 3.4:
				ss = "3+-+3.4 inch"
			elif 3.5 <= ss <= 3.9:
				ss = "3.5+-+3.9 inch"
			elif 4 <= ss <= 4.4:
				ss = "4+-+4.4 inch"
			elif 4.5 <= ss <= 4.9:
				ss = "4.5+-+4.9 inch"
			elif 5 <= ss <= 5.1:
				ss = "5+-+5.1+inch"
			elif 5.2 <= ss <= 5.4:
				ss = "5.2+-+5.4 inch"
			elif 5.5 <= ss <= 5.6:
				ss = "5.5+-+5.6 inch"
			elif 5.7 <= ss <= 5.9:
				ss = "5.7+-+5.9 inch"
			elif ss >=6:
				ss = "6+inch+&+above"

			self.req['max_screen_size'] = str(ss)

		except (KeyError,ValueError):
			pass

		try:
			bat = self.req['battery']
			bat = float(bat)
			if bat < 1000:
				bat = "Less than 1000 mAh"
			elif 1000 <= bat <= 1999:
				bat = "1000 - 1999 mAh"
			elif 2000 <= bat <= 2999:
				bat = "2000 - 2999 mAh"
			elif 3000 <= bat <= 3999:
				bat = "3000 - 3999 mAh"
			elif 4000 <= bat <= 4999:
				bat = "4000 - 4999 mAh"
			elif bat >= 5000:
				bat = "5000 mAh & Above"

			self.req['battery'] = bat
		except (KeyError,ValueError):
			pass


		#Fixing min battery capacities
		try:
			bat = self.req['min_battery']
			bat = float(bat)
			if bat < 1000:
				bat = "Less than 1000 mAh"
			elif 1000 <= bat <= 1999:
				bat = "1000 - 1999 mAh"
			elif 2000 <= bat <= 2999:
				bat = "2000 - 2999 mAh"
			elif 3000 <= bat <= 3999:
				bat = "3000 - 3999 mAh"
			elif 4000 <= bat <= 4999:
				bat = "4000 - 4999 mAh"
			elif bat >= 5000:
				bat = "5000 mAh & Above"

			self.req['min_battery'] = bat
		except (KeyError,ValueError):
			pass

		#Fixing max battery capacities
		try:
			bat = self.req['max_battery']
			bat = float(bat)
			if bat < 1000:
				bat = "Less than 1000 mAh"
			elif 1000 <= bat <= 1999:
				bat = "1000 - 1999 mAh"
			elif 2000 <= bat <= 2999:
				bat = "2000 - 2999 mAh"
			elif 3000 <= bat <= 3999:
				bat = "3000 - 3999 mAh"
			elif 4000 <= bat <= 4999:
				bat = "4000 - 4999 mAh"
			elif bat >= 5000:
				bat = "5000 mAh & Above"

			self.req['max_battery'] = bat
		except (KeyError,ValueError):
			pass

		
		#Fixing camera
		try:
			camera = self.req['camera']
			camera = float(camera)
			if camera < 2:
				camera = "Below 2 MP"
			elif 2 <= camera <= 2.9:
				camera = "2 - 2.9 MP"
			elif 3 <= camera <= 4.9:
				camera = "3 - 4.9 MP"
			elif 5 <= camera <= 7.9:
				camera = "5 - 7.9 MP"
			elif 8 <= camera <= 11.9:
				camera = "8 - 11.9 MP"
			elif 12 <= camera <= 12.9:
				camera = "12 - 12.9 MP"
			elif 13 <= camera <= 15.9:
				camera = "13 - 15.9 MP"
			elif 16 <= camera <= 20.9:
				camera = "16 - 20.9 MP"
			elif camera >= 21:
				camera = "21 MP & Above"

			self.req['camera'] = camera
		except (KeyError,ValueError):
			pass
		
		

		filt = []
		for k,v in self.req.items():
			if v:
				filt.append(self.filters[k]+v)

		return filt 				#our list of URL params is ready!


	#Show time!
	def extract(self):
		#url1 = 'https://www.flipkart.com/mobiles-accessories/mobiles/pr?otracker=categorytree'
		url2 = 'https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy,4io'

		#Important! Give ram size only. Don't write units
		#And everything must be in strings
		#req = {'company':'Lenovo','price_to':'20000','ram':'2','network':'4G'}
		#req  = {}
		filt = self.create_filters()																#filt now stores the list of params to be included in the url
		payload = {'p%5B%5D':filt, 'q':'phones'}												#q-> query string, p handles the filters
		url = url2 + "&" + urllib.urlencode(payload, True)									#urllib.parse.urlencode appends the params properly to the url and don't forget the & after url2
		print url
		#return url

		#Running Chrome headless using xvfb and pyvirtualdisplay
		#display = Display(visible=0, size=(800, 600))
		#display.start()
		#driver = webdriver.Chrome()


		driver.get(url)

		data = driver.page_source								#Selenium gets me all the Javascript dynamic data
		#print(data)

		#with open('log.txt','w') as f:
		#	f.write(data)

		soup = bs(data,'html5lib')								#pass the data to BS to create a BS object soup

		base_url = "https://www.flipkart.com"					#need this to append to the <a> tag's href since relative url is given

		item_list = []

		#And now reck the data to get to the product info
		try:
			parent_div = soup.find('div',{'class':'_2SxMvQ'}).find('div',{'class':'_3T_wwx'})			#this div contains all the product contents

			for item_div in parent_div.findAll('div',{'class':'col _2-gKeQ'}):							#find all the div classes with that attribute - each div is for one product
				item = {}
				#prints name of product
				#print item_div.find('img')['alt']
				item['img'] = item_div.find('img')['src']
				item['name'] = item_div.find('img')['alt']
				#URL of product
				#print base_url+item_div.find('a')['href']
				item['url'] = base_url+item_div.find('a')['href']
				#specs
				item['spec'] = []
				for spec in item_div.find('ul',{'class':'vFw0gD'}).findAll('li'):
					#print spec.string
					item['spec'].append(spec.string)

				item_list.append(item)

		except:
			#print "Oops! No results were found"
			pass

		print item_list
		self.item_list = item_list
		return item_list

	def display(self):
		if not self.item_list:
			print "Oops! No results were found"
		for item in self.item_list:
			print item['name']
			print item['url']
			for spec in item['spec']:
				print spec


if __name__ == "__main__":
    req = {'min_screen_size':'5','max_screen_size':'6','battery':''}
    f = Flip(req)
    f.extract()
    f.display()
#'company':'Lenovo','price_to':'20000','ram':'2','network':'4G',
