#Team3
#This program shall read date from a GEDCOM file and store information for
#individuals and families in lists
import datetime
file = "GEDCOMFile.ged"

with open(file) as f:
	#temporary list to hold current record being examined
	L1 = []
	#list of individuals
	#this will be a list of lists where each individual has their own list
	people = []
	#list of families
	#this will be a list of lists where each family has its own list
	families = []
	#flag to tell that we're looking at an individual
	found_ind = False
	#flag to tell that we're looking at a family
	found_fam = False
	#flag to tell that we're looking at a date
	found_date = False
	#variable to store the type of date currently found
	date_type = ''

	for line in f:
		items = line.split()
		#following segment stores data for an individual
		if int(items[0]) == 0 and items[-1] == 'INDI':
			#if flag for family is set, previous record was family, so store temp list in familes
			if found_fam:
				families = families + [L1]
				found_fam = False
			#set found individual flag
			found_ind = True
			#if there is already an individual in the temp list, store it in the people list
			if len(L1) > 0 and L1[0][0] == 'I':
				people = people + [L1]
			#store ID for new individual in temp list
			L1 = [items[1].replace('@','')]
		#store name of individual in temp list, stripping out backslashes
		if found_ind and items[1] == 'NAME':
			L1 = L1 + [line[2:].strip().replace('/','')]
		#we found a date item so set date flag and store type of date
		if found_ind and items[1] in ['BIRT', 'DEAT']:
			found_date = True
			date_type = items[1]
		#store type of date and actual date in temp list (works for both ind and fam records)
		if found_date and items[1] == 'DATE':
			#convert date to datetime.date object for easy date calculations
			L1 = L1 + [date_type +' '+ str(datetime.datetime.strptime(line[7:].strip(), '%d %b %Y').date())]	
			found_date = False
		#store gender in temp list
		if found_ind and items[1] == 'SEX':
			L1 = L1 + [line[2:].strip()]
		#store pointer to family in temp list
		if found_ind and items[1] in ['FAMC','FAMS']:
			L1 = L1 + [line[2:].strip().replace('@','')]

		#following segment stores data for a family
		if int(items[0]) == 0 and items[-1] == 'FAM':
			if found_ind:
				people = people + [L1]
				found_ind = False
			found_fam = True
			if len(L1) > 0 and L1[0][0] == 'F':
				families = families + [L1]
			L1 = [items[1].replace('@','')]
		if found_fam and items[1] in ['HUSB','WIFE','CHIL']:
			L1 = L1 + [line[2:].strip().replace('@','')]
		if found_fam and items[1] in ['DIV', 'MARR']:
			found_date = True
			date_type = items[1]

#make sure last entry gets added to correct list
if L1[0][0] == 'I':
	people = people + [L1]
elif L1[0][0] == 'F':
	families = families + [L1]

#sort people lists by individual ID (the first element of each individual's list)
people = sorted(people, key = lambda indi:int(indi[0][1:]))

#sort families by family ID (the first element of each faily's list)
families = sorted(families, key = lambda fam:int(fam[0][1:]))

#loop reads people array and then arrays within people arrays and prints
print ('People List:')
for i in people:
        print i[0], ':', i[1][5:]

#loop reads families array and then arrays within families arrays and prints                
print ('')
print ('Families List:')
for i in families:
	record_to_print = i[0] + ':'
        for j in i:
        	fam_item = j.split()
        	if fam_item[0] in ['HUSB','WIFE']:
        		for person in people:
        			if person[0] == fam_item[1]:
        				record_to_print = record_to_print + ' ' + fam_item[1] + ' ' + person[1][5:]
	print record_to_print

	