#Carly Bean
#This program shall read and print data from a GEDCOM file

file = "Project02GEDCOMFIle_CBean.ged"
validTags = ['INDI','NAME','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE']

with open(file) as f:
	for line in f.readlines():
		print line.strip()
		items = line.split()
		print "Level:", items[0]
		#DATE must be level 2
		if int(items[0]) == 1 and items[1] == 'DATE':
			print "INVALID TAG:", items[1]
		#check that tag is valid
		elif items[1] in validTags:
			print "Tag:", items[1]
		#FAM and INDI tags are at the end of the entry
		elif items[-1] == 'FAM' or items[-1] == 'INDI':
			print "Tag:", items[-1]
		else: 
			print "INVALID TAG:", items[1]