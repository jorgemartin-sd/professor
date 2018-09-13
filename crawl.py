#!/usr/bin/python
import unirest, sys, sqlite3, robotparser
from bs4 import BeautifulSoup
from urlparse import urlparse

start_url = sys.argv[1]
to_crawl = []
crawled = []

def save(link, title, description, status, text):
	#Gen SQL
	text = text.replace("'", '').strip()	
	text = text.replace('"', '').strip()
	sql = "INSERT INTO links VALUES('" + link + "', '" + title + "', " + descripition + "', " + str(status) + ", '" + text + "')"
	
	#Insert in db
	db.execute(sql)
	db_con.commit()	

def robots(url):
	try:
		#Create robots.txt url	
		parsed_url = urlparse(url)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
		robot_url = domain + "robots.txt"

		#Check
		rp = robotparser.RobotFileParser()
		rp.set_url(robot_url)
		rp.read()	
		return rp.can_fetch("*", url)	
	except:
		return True

def fetch(url):
	#Check robots.txt
	if not robots(url):
		print(" ")
		print("Respecting: " + url)
		print("-----------------------------")
		print(" ")
		return ""	

	#Don't get banned content
	banned = ["google", "facebook", "tumblr", "twitter", ".png", ".jpg", ".webm", ".gif", ".mp4", ".mp3"]
	for ext in banned:
		if ext in url:	
			return ""

	#Download and parse
	try:
		doc = unirest.get(url)
		doc = doc.body
		print(" ")
		print("Harvesting: " + url)
		print("------------------------------")
		print(" ")
	except:
		return ""

	return doc

def get_links(doc):

	#Create Soup	
	soup = BeautifulSoup(doc, 'html.parser')

	#Get links
	links = soup.find_all('a')
	return links	

def add_link(doc, link):
	#Make sure it is a new link
	link = link.get('href')
	if link not in crawled and link not in to_crawl:
		try:
			if "http" in str(link):	
				#Add link to index
				to_crawl.append(link)
				print(link)

				#Add link/body to db
				soup = BeautifulSoup(doc, "html.parser")
				title = soup.title.string
				title = soup.find("meta", propertry="og:title")
				description = soup.find("meta", property="og:description")
				text = soup.get_text()				 		
				save(link, title, description, 0, text)
		except:
			pass	

#Setup

#Initialize db
db_con = sqlite3.connect("index.db")
db     = db_con.cursor()

try:
	db.execute('''
		CREATE TABLE links(
			link text,
			title text,
			description text,
			crawled int,
			body text
		)	
		'''
	)
except:
	#Add to lists
	rows = db.execute("select * from links")
	for row in rows:
		if row[2] == 0:
			to_crawl.append(row[0])
		else:
			crawled.append(row[0])

db_con.commit()

to_crawl.append(start_url)

#Loop
while True:
	#Move link from to_crawl to crawled
        if to_crawl[0]:	
            link = to_crawl.pop(0)
    
	#Make sure there is a link
	if link != "":
		try:
			#Add to crawled
			crawled.append(link)
			sql = "UPDATE links SET crawled = 1 WHERE link='" + link + "'"
			db.execute(sql)

			#Fetch page
			doc = fetch(link)

			#Get links
			links = get_links(doc)
			for link in links:
				add_link(doc, link)	
	
		except:
			print(" ")
			print("Skipping: " + link)
			print("------------------------------")
			print(" ")
