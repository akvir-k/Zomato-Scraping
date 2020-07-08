from zomato_webraping import Scrape_area
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import time,os,json

def Resturant_details(data):
	if not os.path.exists(data['Area']):
		os.makedirs(data['Area'])
	url=data['url']
	option = webdriver.Chrome('/home/aman/Desktop/Zomato_scraping/chromedriver')
	
	option.get(url)
	page_data=option.page_source
	soup1=BeautifulSoup(page_data,'html.parser')

	#Find the pages of all:
	find_page=soup1.find('div',class_='search-pagination-top')
	Number_page=find_page.find('div',class_='res-right').a['href']
	page_url=''
	for link in Number_page:
		if '=' in link:
			page_url='https://www.zomato.com'+page_url+link
			break
		else:
			page_url+=link
	page_no=find_page.find('div',class_='pagination-number').get_text().strip()
	total_page=0
	for page in range(len(page_no)):
		if ' ' in page_no[page]:
			total_page=(page_no[page+1::])
	option.close()


	# Get all Data from website and store in page list:

	Page_list=[]
	for no in range(1,int(total_page)+1):
		if not os.path.exists(data['Area']+'/Page='+str(no)+'.json'):
		
			link_url=page_url+str(no)	
			browser = webdriver.Chrome('/home/aman/Desktop/Zomato_scraping/chromedriver')
			# print(link_url)
			browser.get(link_url)
			pages_data=browser.page_source
			soup=BeautifulSoup(pages_data,'html.parser')	
		
			content=soup.find('div',id='orig-search-list')
			div_content=content.find_all('div',class_='card')
			# return div_content
			page=content.find_all('div',class_='content')
			for pa in page:
				title=pa.find('div',class_='col-s-12')
				name=title.find_all('a')

				for i in name:
					if 'result-title' in i['class']:
						Rest_name=(i.get_text().strip())

				raw=pa.find('div',class_='row')
				# Address of resturant
				style=''
				find_style=raw.find('div',class_='search-result-address')
				if find_style!=None:
					style=raw.find('div',class_='search-result-address').get_text().strip()

				search_rating=raw.find('div',class_='search_result_rating')
				# Rating of resturant
				rating=''
				if search_rating.find('div',class_='rating-popup')!=None:
					rating=search_rating.find('div',class_='rating-popup').get_text().strip()
				# votes of Resturant
				votes=''
				if search_rating.find('span')!=None:

					votes=search_rating.find('span').get_text().strip() # Customer votes 

				# Find Cusinies of Resturants 
				search_text=pa.find('div',class_='search-page-text')
				clearfix=search_text.find('div',class_='clearfix')
				find_a=clearfix.find_all('a')
				Cusinies=[]
				for i in find_a:
					Cusinies.append(i.get_text().strip())

				# Find rate of food:
				sear_cost=search_text.find('div',class_='res-cost').get_text().strip()
				cost=''
				for j in range(len(sear_cost)):
					if sear_cost[j] in '₹':
						cost+=sear_cost[j+1::]
						break
				
				# Find Time of Resturant
				
				sear_time=search_text.find('div',class_='res-timing')
				time_rest=''	
				if sear_time!=None:
					time_rest=sear_time.find('div').get_text().strip()
				
				# Find Features of Resturant

				sear_features=search_text.find('div',class_='res-collections')
				Features=[]
				if sear_features!=None:
					fea_data=sear_features.find('div')
					collection=fea_data.find_all('a')			
					for coll in collection:
						Features.append(coll.get_text().strip())
					# print(Features)
				
				# Find Resturant Food's image:
				search_image=pa.find('div',class_='search_left_featured').a['href']
				
				# Discount offer
				discount=[]
				offer=search_text.find('div',class_='res-offers')
				if offer!=None:
					discount.append(offer.find('div').a.get_text().strip())
					
				# div_class=offer.find('div')
				# return div_class
				# Collect All file in a Dictionary
				list_dict={'Resturant_Name':'','Food_Image':'','Address':'','Cusinies':'','Cost':'','Time':'','Featured':'','Rating':'','Customer_vote':'','Discount':''}
				list_dict['Resturant_Name']=Rest_name
				list_dict['Food_Image']=search_image
				list_dict['Address']=style
				list_dict['Cusinies']=Cusinies
				list_dict['Cost']=cost
				list_dict['Time']=time_rest
				list_dict['Featured']=Features
				list_dict['Rating']=rating
				list_dict['Customer_vote']=votes
				list_dict['Discount']=discount

				Page_list.append(list_dict)
					
			browser.close()
			with open(data['Area']+'/Page='+str(no)+'.json','w+')as file:
				files=json.dump(Page_list,file)

			time.sleep(4)
		pprint(Page_list)	
	return Page_list
pprint(Resturant_details(Scrape_area()[1]))
