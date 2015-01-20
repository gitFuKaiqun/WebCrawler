__author__ = 'Kaiqun'

import urllib2
from bs4 import BeautifulSoup


if __name__ == '__main__':
	GFile = open('GazetteerURLs.txt', 'r')
	ResultingFile = open('Gazetteer.csv', 'a')

	ResultingFile.write('Id,Name,Category,Type,Class,Latitude,Longitude\n')

	count = 0

	for line in GFile:
		try:
			tmpList = []
			page = urllib2.urlopen(line.strip()).read()
			soup = BeautifulSoup(page)
			mydivs = soup.find_all("div", { "id" : "contentNoCol" })

			oneTable = str(mydivs[0].contents[14].contents[1].contents[3].contents[1])
			soup = BeautifulSoup(oneTable)
			mytrs = soup.find_all("tr")

			tmpList.append(str(mytrs[7].contents[3].contents[0].contents[0]))
			tmpList.append(str(mytrs[0].contents[3].contents[0]).replace(',', ''))
			tmpList.append(str(mytrs[1].contents[3].contents[0]).replace(',', ''))
			tmpList.append(str(mytrs[2].contents[3].contents[0]).replace(',', ''))
			tmpList.append(str(mytrs[3].contents[3].contents[0]).replace(',', ''))
			tmpList.append(str(mytrs[5].contents[3].contents[0]).replace(',', ''))
			tmpList.append(str(mytrs[6].contents[3].contents[0]).replace(',', ''))

			ResultingFile.write(','.join(tmpList) + '\n')

			count += 1

			print 'Done --- ' + tmpList[1] + '\t\t\t\t\t\t\t\t\t\t\t' + str(count / 4.71) + '%'
		except Exception, e:
			print e.message

	ResultingFile.close()