# Import Modules
import os 
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger 

# Set Path
dir = 'C:/Users/rmadhok/Dropbox (CID)/CAG/pdf'
os.chdir(dir)


# Get only PDF pages containing tables
folders = os.listdir(dir)
for folder in folders:
	os.chdir(dir+"/"+folder)
	files = os.listdir(".")

	# Extract pages 5 in each pdf for each state
	for pdf in files:
		print 'Getting table 5 from ' + pdf + ' of ' + folder
		output = PdfFileWriter()
		input1 = PdfFileReader(open(pdf, "rb"))
		output.addPage(input1.getPage(6))
		newfile=str(2)+pdf

		# Save new pdf
		outputStream = file(newfile, "wb")
		output.write(outputStream)

# Remove original file
for folder in folders:
	os.chdir(dir+"/"+folder)
	files = os.listdir(".")
	for file in files:
		if not file.startswith('2'):
			os.remove(file)
			print 'Removing original file ', file

# Rename new pdfs 
for folder in folders:
	os.chdir(dir+"/"+folder)
	files = os.listdir(".")
	for file in files:
		os.rename(file, file.replace('2', ''))

# Merge district pdfs in each state
for folder in folders:
	os.chdir(dir+"/"+folder)
	merger = PdfFileMerger()
	pdf_files = os.listdir(".")

	# Loop through district pdfs
	for file in pdf_files:
		# open each file and add to merger object
		fileobj = open(file, 'r')
		merger.append(file)
	os.chdir(dir+"/zState_merge_pdf")
	output = open(folder+'.pdf', 'wb')
	print 'Merging district pdfs in ' + folder
	merger.write(output)

# Merge state pdfs
os.chdir(dir+"/zState_merge_pdf")
state_pdfs = os.listdir(".")
merger = PdfFileMerger()
for file in state_pdfs:
	fileobj = open(file, 'r')
	merger.append(file)
os.chdir(dir+"/zALL_STATES")
output = open('all_states.pdf', 'wb')
merger.write(output)
