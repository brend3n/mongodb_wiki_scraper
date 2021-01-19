import requests
import config
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup




DB_NAME = ''
COLLECTION_NAME = ''
CONNECT_STRING = ""
connect = pymongo.MongoClient(CONNECT_STRING)



client = connect
db = client.DB_NAME


def get_soup(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_random_page_url():
	page = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
	title = page["title"]
	description = page["extract"]
	url = page["content_urls"]["desktop"]["page"]

	# Uncomment to print information about the page
		# print(f"Title: {title}")
		# print(f"Description: {description}")
		# print(f"URL: {url}")
	page_name = title

	return url, page_name

def strip_link_prefix(link):
	link = link[6:]
	return link

def get_all_links(soup):
	links = []
	for link in soup.find_all('a'):
		l = link.get('href')
		l = str(l)
		if ("/wiki/" in l) and (":" not in l) and (".svg" not in l) and (".org" not in l) and ("Main_Page" not in l):
			# print(l)
			l = strip_link_prefix(l)
			links.append(l)

	return links


def store(page_name, links):
	# Store in: Database
	page_data_model = {
		"page_name" : page_name,
		"links" : links,
		"num_links" : len(links)
	}
	try:
		db.COLLECTION_NAME.insert_one(page_data_model)
	except Exception as e:
		print(f"Error: {e}")
		print(f"Could not insert link data of {page_name}.")
		return

	print(f"Successfully added link data of {page_name}.")

def check_if_exists(page_name):
        try:
            count = db.COLLECTION_NAME.count_documents({"page_name":page_name})
            if count > 0:
                return True
            return False
        except:
            print("Error in -> check_if_exists() function in wiki_scrape.py")


def run():
	url, page_name = get_random_page_url()
	page = get_soup(url)
	links = get_all_links(page)
	# print(links)
	return page_name, links

def clean_links(links):
	links = list(set(links)) 	
	# for link in links:
	# 	print(link)
	return links

def batch_store():
	i = 0
	while True:
		try:

			ran_page_name, links = run()

			if check_if_exists(ran_page_name):
				print(f"{ran_page_name} already exists in the database")
				print("Getting next page...")
				continue

			links = clean_links(links)
			store(ran_page_name, links)
			i+=1

		except:
			print("Error has occurred ...")
			print("Now continuing")
			batch_store()








