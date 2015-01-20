__author__ = 'Kaiqun'

import urllib2
from bs4 import BeautifulSoup
import re


def CheckPages(inputUrl):
	"""
	output : if None, only one page; if not None, multiple pages
	:rtype : object
	"""
	page = urllib2.urlopen(inputUrl).read()
	soup = BeautifulSoup(page)
	mydivs = soup.find_all("td", { "colspan" : "2" })

	Listing = []
	ReturnList = []

	for td in mydivs:
		if td.contents[0] == 'Page ':
			Listing.append(td)

	soup = BeautifulSoup(str(Listing[0]))
	for link in soup.find_all('a'):
		ReturnList.append(link.get('href'))

	return ReturnList


def CheckLetters(inputUrl):
	"""
	output : if None, alphabetical orders available; if not None, no alphabetical orders
	:rtype : object
	"""
	page = urllib2.urlopen(inputUrl).read()
	soup = BeautifulSoup(page)
	mydivs = soup.find_all("div", { "id" : "content" })

	ReturnList = []

	for td in mydivs:
		soup = BeautifulSoup(str(td.contents[7]))
		for link in soup.find_all('a'):
			ReturnList.append('http://dc.hometownlocator.com/' + link.get('href'))
	return ReturnList


def getSecondDegree(inputUrl):
	page = urllib2.urlopen(inputUrl).read()
	soup = BeautifulSoup(page)
	mySecDivs = soup.findAll("td", { "class" : "padright" })

	if mySecDivs:
		SecondDegreeUrls = []
		for td in mySecDivs:
			if str(td.contents[0])[0] == '<':
				m = re.search('(?<=href\="\.\./)(.*)(?=")', str(td))
				SecondDegreeUrls.append('http://dc.hometownlocator.com/' + m.group(0))
		return SecondDegreeUrls


def CrawlingLogic(inputURL):
	try:
		ReturnListing = []
		currentURL = inputURL

		LetterL = CheckLetters(currentURL)
		PageL = CheckPages(currentURL)

		if LetterL:
			for aletter in LetterL:
				try:
					currentURL = aletter
					if CheckPages(currentURL):
						ReturnListing += getSecondDegree(currentURL)
						for page in CheckPages(currentURL):
							currentURL = page
							ReturnListing += getSecondDegree(currentURL)
					else:
						ReturnListing += getSecondDegree(currentURL)
				except Exception, e:
					print e.message
					pass

		elif PageL:
			ReturnListing += getSecondDegree(currentURL)
			for page in PageL:
				try:
					currentURL = page
					ReturnListing += getSecondDegree(currentURL)
				except Exception, e:
					print e.message
					pass

		else:
			ReturnListing += getSecondDegree(currentURL)

		return ReturnListing
	except Exception, e:
		print e.message
		pass


if __name__ == '__main__':
	page = urllib2.urlopen('http://dc.hometownlocator.com/features/').read()
	soup = BeautifulSoup(page)
	mydivs = soup.findAll("tr", { "class" : "darkrow" })

	FirstDegreeUrls = []

	for item in mydivs:
		try:
			m = re.search('(?<=href\=")(.*)(?=")', str(item))
			FirstDegreeUrls.append('http://dc.hometownlocator.com/features/' + m.group(0))
		except:
			pass

	SecondDegreeUrls = []

	f = open('GazetteerURLs.txt','a')

	for line in FirstDegreeUrls:
		try:
			print len(CrawlingLogic(line))
			for oneUrl in CrawlingLogic(line):
				f.write(oneUrl + '\n')
		except Exception, e:
			print e.message

	f.close()