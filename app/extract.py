import urllib
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import html5lib
"""
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
"""

#filter strings to be used in Flipkart's url

class Flip:
	def __init__(self,req):
		self.req = req
		self.filters = {'company':'facets.brand%5B%5D=','price_from':'facets.price_range.from=','price_to':'facets.price_range.to=','ram':'facets.ram%5B%5D=','os':'facets.operating_system%5B%5D=',
	'network':'facets.network_type%5B%5D=','screen_size':'facets.screen_size%5B%5D=','battery':'facets.battery_capacity%5B%5D=','camera':'facets.primary_camera%5B%5D='}

	#creates a nice list of params to be included in Flipkart's url
	def create_filters(self):
		#if price_to is in req but price_from is not then must set price_from as 'Min'
		if 'price_to' in self.req and 'price_from' not in self.req:
			self.req['price_from'] = 'Min'
		#Append units i.e. GB to ram size if it's given in the user requirements
		try:
			self.req['ram'] += ' GB'
		except KeyError:
			pass

		#Fix screen size. For Flipkart screen size has to be in ranges. Absolute values not allowed
		try:
			ss = self.req['screen_size']
			ss = float(ss)
			if ss < 3:
				ss = "Less than 3 inch"
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

		except KeyError:
			pass

		#Fixing battery capacities
		try:
			bat = self.req['battery']
			bat = float(bat)
			if bat < 1000:
				bat = "Less+than+1000+mAh"
			elif 1000 <= bat <= 1999:
				bat = "1000+-+1999 mAh"
			elif 2000 <= bat <= 2999:
				bat = "2000+-+2999 mAh"
			elif 3000 <= bat <= 3999:
				bat = "3000+-+3999 mAh"
			elif 4000 <= bat <= 4999:
				bat = "4000+-+4999 mAh"
			elif bat >= 5000:
				bat = "5000+mAh+&+Above"

			self.req['battery'] = bat
		except KeyError:
			pass

		filt = []
		for k,v in self.req.items():
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
            url = url2 + "&" + urllib.urlencode(payload,True)									#urllib.parse.urlencode appends the params properly to the url and don't forget the & after url2
            #print(url)

            #Running Chrome headless using xvfb and pyvirtualdisplay
            display = Display(visible=0, size=(800, 600))
            display.start()
            driver = webdriver.Chrome()


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

            #print item_list
            return item_list


            #STUFF I TRIED AND FAILED
            """
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
            """
            #driver = webdriver.Chrome()
            #driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
            #driver.implicitly_wait(90)

            #driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
            #driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
            #driver.set_window_size(1120, 550)
            #delay = 90 # seconds
            #driver.implicitly_wait(delay)
            """
            xpath = '//*[@id="container"]/div/div[1]/div[2]/div/div[2]/div/div[3]/div[1]'
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
                print("Page is ready!")
            except TimeoutException:
                print("Loading took too much time!")
            """

if __name__ == "__main__":
    req = {'company':'Lenovo','price_to':'20000','ram':'2','network':'4G'}
    f = Flip(req)
    f.extract()
