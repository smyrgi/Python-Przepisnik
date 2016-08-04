#!/usr/bin/env python2
# -*- coding: utf-8 -*-


##################### POBIERANIE DANYCH ###############################

# importowanie modułów
import requests
from bs4 import BeautifulSoup
import re
import os
import codecs
import shutil
import linecache
import unicodecsv as csv

# stworzenie folderu na dane 
pwd = os.path.abspath(__file__)[:-len(__file__)]
if not os.path.exists("data"):
    os.mkdir("data")
path = pwd+"data/images"
if not os.path.exists(path):
    os.mkdir(path)

def myreplace(text):	
	dic = {"ż":"z", "ź":"z", "ć":"c", "ś":"s", "ą":"a", "ę":"e", "ó":"o", "ł":"l", "ń":"n", "Ż":"Z", "Ź":"Z", "Ć":"C", "Ą":"A", "Ę":"E", "Ś":"S", "Ó":"O", "Ł":"L", "Ń":"N", " ":"-"}
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text


#-----------------------------------------------------------
# czytanie adresów ze strony i zapisanie ich do pliku "links"
# czytanie nazw ze strony i zapisanie ich do pliku "names"

#csvfile = open(os.path.join("data", "data.csv"), 'a')
csvpath = pwd+"data/data.csv"

if os.path.exists(csvpath) :
	csvfile = open( csvpath, 'a+')
	fieldnames = ['name', 'link', 'ingredients', 'recipe']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="|")
else:
	csvfile = open( csvpath, 'w')
	fieldnames = ['name', 'link', 'ingredients', 'recipe']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="|")
	writer.writeheader()

reader = csv.DictReader(csvfile, delimiter='|')
links = [ row['link'] for row in reader]
base_url = "http://pychotka.pl"
#for i in range(22,220,22)

print "\nAktualizacja w toku...\n"
for t in range(14,20,2):
	index_url = "http://pychotka.pl/Strona-" + str(t)
	r = requests.get(index_url)
	soup = BeautifulSoup(r.content, "lxml")
	recipe_links = [link for link in soup.find_all('a',title=True) if (link["href"][:1]=="/") ]
	if recipe_links == [] : 
		#print 'continue1'
		continue
	i=1
	for link in recipe_links[:18]:
			if (link["title"][:15]).encode('utf-8')=="Czytaj więcej: ":
				#print 'continue2'
				continue
		#if i%2==0: 
			### --------------- Linki i Nazwy -----------
			url = link["href"]
			name = link["title"]
			recipe=''
			ingredients=''
			url = base_url + url
			if url in links : 
				#print 'continue3'
				continue
			r = requests.get(url)
			soup = BeautifulSoup(r.content, "lxml")	
			### --------------- Instrukcje -----------
			soupfind = soup.find('ol', itemprop="recipeInstructions")
			if soupfind == None : 
				#print 'continue4'
				continue
			else:
				recipe_tag = [text for text in soupfind]
			if recipe_tag == [] : 
				#print 'continue5'
				continue
			for tag in recipe_tag[1:-1]:
				source = str(tag)
				soup1 = BeautifulSoup(source, "lxml")
				recipe_text = [text for text in soup1.find_all('div')]
				if recipe_text == [] : 
					#print 'break1'
					break
				for text in recipe_text:
					text = text.contents[0]
					text = unicode(text) 
					text = text[5:].encode('utf-8')
					recipe = recipe + text + '\n'
			### --------------- Składniki -----------
			recipe_ingred = [ingred for ingred in soup.find_all('ul', class_="") ] 
			if recipe_ingred == [] : 
				#print 'continue6'
				continue
			source = str(recipe_ingred[0])
			soup1 = BeautifulSoup(source, "lxml")
			recipe_ingred = [text1 for text1 in soup1.find_all('li')]
			if recipe_ingred == [] : 
				#print 'continue7'
				continue
			for ingred in recipe_ingred:
				try: 
					ingred = ingred.contents[0]	
				except: 
					#print 'break2'
					break
				ingred = unicode(ingred) 
				ingred = ingred[4:].encode('utf-8')
				ingredients=ingredients+ingred + "\n"
			### --------------- Zdjęcia -----------
			recipe_foto = [foto for foto in soup.find_all('img',alt=True,title=True) if (foto["src"][:5]=="foto/" and foto["src"][-4:]==".jpg" and foto["alt"]==foto["title"] )]
			if recipe_foto == [] : 
				#print 'continue8'
				continue
			for foto in recipe_foto:
				url1 = foto["src"] 
				url1 = base_url + "/" + url1
			filename = "img_" + name + ".jpg"
			filename = myreplace(filename.encode('utf8'))
			file_image = open( os.path.join("data/images", filename), 'wb')
			r = requests.get(url1, stream=True)
			shutil.copyfileobj(r.raw, file_image)
			### --------------- Zapisanie do .csv -----------
			name = name.encode('utf-8') 
			url = url.encode('utf-8') 
			row = [] 
			writer.writerow({'name': name, 'link': url, 'ingredients': ingredients, 'recipe': recipe})
			print "Dodano przepis: " + name
			del r, soup, soup1, recipe_foto
			file_image.close()
		#i=i+1
#-----------------------------------------------


print 'Aktualizacja ukończona \n'



