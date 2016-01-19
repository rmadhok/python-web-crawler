# Import libraries
import os
import urllib
import urllib2
from BeautifulSoup import *
import re
import requests

# Set Directory path
dir = 'C:/Users/rmadhok/Dropbox (CID)/CAG/pdf'

# Set main URL with state links
url = 'https://nrhm-mis.nic.in/SitePages/DLHS-4.aspx?RootFolder=%2FDLHS4%2FState%20and%20District%20Factsheets&FolderCTID=0x012000742F17DFC64D5E42B681AB0972048759&View=%7bF8D23EC0-C74A-41C3-B676-5B68BDE5007D%7d'
print 'Collecting top-level state links from:', url 

# Set top - level URL
top = 'https://nrhm-mis.nic.in'

# Soupify state page and collect state URLs into array
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
divs = soup.findAll('div', {'class': 'ms-vb itx'})
state_links = []
for div in divs:
	state_url = top + div.a['href']
	state_links.append(str(state_url))

# Get district factsheet links
fact_links = []
for link in state_links:

	# Soupify each state URL
	state_html = urllib.urlopen(link).read()
	soup = BeautifulSoup(state_html)

	for div in soup.findAll('div', {'class': 'ms-vb itx'}):
		# Collect the factsheet link which is not a state-level pdf into an array
		factsheet_url = top + div.a['href']
		if not 'pdf' in factsheet_url:
			print 'Collecting factsheet from:', factsheet_url
			fact_links.append(str(factsheet_url))

# Download state-wise district fact-sheets
for factsheet in fact_links:
	# Switch to pdf folder
	os.chdir(dir)
	getstate = str(re.findall('Factsheets%2F([^ ]*)%2F', factsheet))
	state = getstate.replace('%20', ' ')

	# Create state folder if it doest not exist -- **NEED TO FIX THIS - IT IS NOT WORKING
	if not os.path.exists(state):
		os.mkdir(state)

	# Collect links to pdf file into array
	html = urllib.urlopen(factsheet).read()
	soup = BeautifulSoup(html)
	divs = soup.findAll('div', {'class': 'ms-vb itx'})
	pdflinks = []
	for div in divs:
		newurl = top + div.a['href']
		pdflink = newurl.replace(" ", "%20")
		pdflinks.append(str(pdflink))
		
	# cd into current states folder for inputting pdfs
	os.chdir(state)
	# download each district pdf file in state, if doesn't exist -- **NEED TO FIX IF STATEMENT. Currently downloading all files.
	for file in pdflinks: 
		filename = file.rsplit('/', 1)[-1]
		filename = filename.replace("%20", " ")
		if not os.path.isfile(file):
			urllib2.urlopen(file)
			urllib.urlretrieve(file, filename)
			print 'Downloading ' + str(filename) + ' From ' + state 
		else:
			print 'Already downloaded.'

# Clean Folder names
for folder in os.listdir(dir):
	os.rename(folder, folder.replace('[', ''))
	os.rename(folder, folder.replace(']', ''))
	os.rename(folder, folder.replace("'", " "))
	os.rename(folder, folder.replace(" ", ""))