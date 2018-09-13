#!/usr/bin/python
import sqlite3

#Finds highest score
def find_max(links):
	max = 0
	for link in links:
		if link[2] > max:	
			max = link[2] 
	return max

#Sorts links
def sort(max, links):
	out = []
	while max > 0:
		for link in links:
			if link[2] == max:
				out.append(link)

		max -=1	
	return out

def query(query, page):
	#Get values from db
	print("Connecting to DB")
	db_con = sqlite3.connect("index.db")
	db     = db_con.cursor()

	print("Loading DB")
	rows = db.execute("select title, link, body from links")
	links = []
	for row in rows:
		link = [row[0], row[1], 0, row[2]]
		links.append(link)	

	#Check occurences of string
	print("Checking search terms")
	search_terms = query.lower().split(" ")
	for term in search_terms:
		for link in links:
			occurances = link[0].lower().count(term)
			occurances += link[3].lower().count(term)
			link[2] +=occurances

	#Get Max
	print("Finding Max...")
	max = find_max(links)
	print("Max Found: " + str(max))
	
	#Sort	
	print("Sorting...")
	links = sort(max, links)

	#Remove page text
	for link in links:
		link = link[0:3]

	#Output
	size = 10
	start = int(page) - 1
	start *=size
	end = int(page)
	end *=size	
	print "done"
	return links[start:end]
