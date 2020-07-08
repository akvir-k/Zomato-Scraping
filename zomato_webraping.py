from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import os,json

def Scrape_area():
	if os.path.exists('zomato_area.json'):
		with open('zomato_area.json','r') as area:
			file=json.load(area)
		return file
	else:
		option = webdriver.Chrome('/home/aman/Desktop/Zomato_scraping/chromedriver')
		option.get('https://www.zomato.com/ncr')
		data=option.page_source
		# response = option.execute_script('return document.documentElement.outerHTML')

		soup=BeautifulSoup(data,'html.parser')

		segment=soup.find('div',class_='ui segment row')

		area=segment.find_all('a')

		list_area=[]
		for ar in area:

			name=''
			for i in ar.get_text().strip():
				if '(' in i:
					break
				else:
					name+=i
			area={}

			area['Area']=name.strip()
			area['url']=ar['href']
			list_area.append(area)
		option.close()
		with open('zomato_area.json','w+') as area:
			file=json.dump(list_area,area)
		return list_area

# pprint(Scrape_area())
