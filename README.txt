######## CRAWLING INDIAN GOVERNMENT WEBSITES TO CONSTRUCT USEABLE DATA ##########

%%%%%% Introduction

This is my first full-fledged web scraper as I continue to improve my python skills. The Indian Government houses health data for each district in
each state (see link below). Their data storage systems are extremely outdated and all data are stored in PDF files (UGH!). To make matters worse, 
there are separate PDFs for each district, making ~600 in total. My goal is to cycle through each state, pull each PDF onto my machine to extract
the data, convert to CSV, and clean it. The output will be a sexy read-to-analyse district-level dataset of health indicators across India.

PDF text mining libraries like PdfMiner and pdf2txt.py were not running properly so I opted to merge all PDFs together and use an online converter 
which honestly worked faster and gave the same results.

%%%%%% Methodology

## Scrape.py
 
1. Scrape HTML of top-level website and collect links to district tables
2. Loop through each state URL, collect each district PDF URL, download PDF

## merge_state_dist_pdf.py

1. Use PyPDF2 library to extract only the health table page from each pdf
2. Merge all district PDFs in each state (end up with 28 state PDFs each with a page for each distrcit)
3. Merge all state PDFs

## Convert PDF to CSV using pdftables

1. I used the website instead of the python package because it was easier

## clean.do

1. Cleaned up and prepared for analysis
2. Reshape data to wide form

Link to website: https://nrhm-mis.nic.in/SitePages/DLHS-4.aspx?RootFolder=%2FDLHS4%2FState%20and%20District%20Factsheets&FolderCTID=0x012000742F17DFC64D5E42B681AB0972048759&View={F8D23EC0-C74A-41C3-B676-5B68BDE5007D}