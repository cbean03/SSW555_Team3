#Team3
#This program shall read date from a GEDCOM file and store information for
#individuals and families in lists
import datetime, re

tags0_norm = ['HEAD', 'TRLR', 'NOTE']
tags0_id = ['INDI', 'FAM']
tags1 = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
tags2 = ['DATE']
today = datetime.datetime.now().date()

#Natural sorting function just to meet sorted requirements of project 3 submission
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#Class for holding family information
class Family:
    members = 0
    
    def __init__(self, id):
        self.id = id
        self.married = None
        self.divorced = None
        self.husband = None
        self.wife = None
        self.children = []
    
    def addHusband(self, husb):
        #BEGIN: US11 - No bigamy
        if Family.members > 1:
            print "ERROR: User story 11 - A husband in family " + self.id + " is married to wife but was not divorced first."
            self.husband = husb
        #End: US11 - No bigamy
        else:
            self.husband = husb
            Family.members += 1
        
    def addWife(self, wife):
        #BEGIN: US11 - No bigamy
        if Family.members > 1:
            print "ERROR: User story 11 - A wife in family " + self.id + " is married to wife but was not divorced first."
            self.wife = wife
        #End: US11 - No bigamy
        else:
            self.wife = wife
            Family.members += 1
        
    def addChild(self, child):
        self.children.append(child)
        Family.members += 1

    def addMarried(self, date):
        marriage_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US05 - Marriage before death
        if(isAfterDate(marriage_date, self.husband.death) or isAfterDate(marriage_date, self.wife.death)):
            print "ERROR: User story 5 - Marriage date " + str(marriage_date) + " for family " + self.id + " after death of spouse"
        #END: US05
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(marriage_date, today)):
            print "ERROR: User story 1 - Marriage date " + str(marriage_date) + " for family " + self.id + " after today's date"
        #END: US01
        else:
            self.married = marriage_date
        
    def addDivorced(self, date):
        divorce_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(divorce_date, today)):
            print "ERROR: User story 1 - Divorce date " + str(divorce_date) + " for family " + self.id + " after today's date"
        #END: US01
        else:
            self.divorced = divorce_date
        
    def numMembers(self):
        return Family.members
        
    def printFamily(self):
        print self.id
        print "Married: " + str(self.married)
        print "Divorced: " + str(self.divorced)
        print "Husband: " + self.husband.name
        print "Wife: " + self.wife.name
        print "Children:",
        if self.children == []:
            print "None"
        else:
            for child in self.children:
                if child != self.children[-1]:
                    print child.name + ",",
                else:
                    print child.name
        
#Class for holding individual information
class Individual:
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.sex = ''
        self.birthday = None
        self.death = None
        self.famc = ''
        self.fams = ''
    
    def addName(self, name):
        self.name = name
        
    def addSex(self, sex):
        self.sex = sex
        
    def addBirthday(self, date):
        birth_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(birth_date, today)):
            print "ERROR: User story 1 - Birthday " + str(birth_date) + " for individual " + self.id + " after today's date"
        #END: US01
        #BEGIN: US03 - Birth before death
        if(isAfterDate(birth_date, self.death)):
            print "ERROR: User story 3 - Birthday " + str(birth_date) + " for individual " + self.id + " after individual's death date"
        #END: US03
        else:
            self.birthday = birth_date
        
    def addDeath(self, date):
        death_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(death_date, today)):
            print "ERROR: User story 1 - Death Date " + str(death_date) + " for individual " + self.id + " after today's date"
        #END: US01
        #BEGIN: US03 - Birth before death
        if(isAfterDate(self.birthday, death_date)):
            print "ERROR: User story 3 - Death date " + str(death_date) + " for individual " + self.id + " before individual's birth date "
        #END: US03
        else:
            self.death = death_date
        
    def addFamc(self, famc):
        self.famc = famc
        
    def addFams(self, fams):
        self.fams = fams
        
    def printIndividual(self):
        print self.id + ": " + self.name
        print "Gender: " + self.sex
        print "Birthday: " + str(self.birthday)
        print "Death: " + str(self.death)
        print "Child of family: " + self.famc
        print "Spouse of family: " + self.fams
    
def isAfterDate(date1, date2):
    """Function:     isAfterDate
       Purpose:      Returns whether date1 is after date2. If date1 or date2 is of type None then return False.
       Parameters:   date1 - datetime.date object | date2 - datetime.date object
       Return value: Boolean
    """
    if(date1 != None and date2 != None):
        return date1 > date2
    else:
        return False

def readGEDCOM(filename):
    curr_indi = ''
    curr_fam = ''
    bday_flag = 0
    deat_flag = 0
    marr_flag = 0
    div_flag = 0
    individuals = {}
    families = {}

    print "BEGIN: " + filename
    with open(filename) as f:
        for line in f:
            parts = line.split()
            
            #For first level, check for individual/family tag and create new instance
            if parts[0] == '0':
                if parts[1] in tags0_norm:
                    pass
                elif parts[2] in tags0_id:
                    if parts[2] == 'INDI':
                        curr_indi = parts[1].replace("@","")
                        individuals[curr_indi] = Individual(curr_indi)
                        curr_fam = ''
                    else:
                        curr_fam = parts[1].replace("@","")
                        families[curr_fam] = Family(curr_fam)
                        curr_indi = ''
                else:
                    print("Invalid tag")
                    
            #Add appropriate information to current individual or current family
            elif parts[0] == '1':
                if parts[1] in tags1 and curr_indi != '':
                    if parts[1] == 'NAME':
                        individuals[curr_indi].addName(" ".join(parts[2:]).replace('/',''))
                    elif parts[1] == 'SEX':
                        individuals[curr_indi].addSex(parts[2])
                    elif parts[1] == 'BIRT':
                        bday_flag = 1
                    elif parts[1] == 'DEAT':
                        deat_flag = 1
                    elif parts[1] == 'FAMC':
                        individuals[curr_indi].addFamc(parts[2].replace("@",""))
                    elif parts[1] == 'FAMS':
                        individuals[curr_indi].addFams(parts[2].replace("@",""))
                elif parts[1] in tags1 and curr_fam != '':
                    if parts[1] == 'HUSB':
                        families[curr_fam].addHusband(individuals[parts[2].replace("@","")])
                    elif parts[1] == 'WIFE':
                        families[curr_fam].addWife(individuals[parts[2].replace("@","")])
                    elif parts[1] == 'CHIL':
                        families[curr_fam].addChild(individuals[parts[2].replace("@","")])
                    elif parts[1] == 'MARR':
                        marr_flag = 1
                    elif parts[1] == 'DIV':
                        div_flag = 1
                    
            #Add appropriate date to current individual or current family
            elif parts[0] == '2':
                if parts[1] in tags2 and curr_indi != '':
                    if bday_flag == 1:
                        individuals[curr_indi].addBirthday(parts[2:])
                        bday_flag = 0
                    elif deat_flag == 1:
                        individuals[curr_indi].addDeath(parts[2:])
                        deat_flag = 0
                elif parts[1] in tags2 and curr_fam != '':
                    if marr_flag == 1:
                        families[curr_fam].addMarried(parts[2:])
                        marr_flag = 0
                    elif div_flag == 1:
                        families[curr_fam].addDivorced(parts[2:])
                        div_flag = 0

    #BEGIN: US09 - Death before child brith
    for fam in families: #Finding keys in dictionary.  Go throught the family first... Then go through the child list.
        for child in families[fam].children: #Use key to get family... next look at the family.
            delta = datetime.timedelta(days=(9 * 30)) #9 months times 30 days.
            if families[fam].husband.death is not None: #If the husband didn't die, skip.
                if child.birthday > families[fam].husband.death - delta:
                    print "ERROR: User Story 9: Child born less than 9 months after father's death.  Dead father:",families[fam].husband.name,"  Child:",child.name
                else:
                    continue
            if families[fam].wife.death is not None:  # If the wife is not dead, skip.
                if child.birthday is not None: #If the child does not have a birthday, skip.
                    if child.birthday > families[fam].wife.death: #If the child is not born before mother's death, skip.
                        print "ERROR: User Story 9: Child born before mother's death.  Dead mother:",families[fam].wife.name,"  Child:",child.name
                    else:
                        continue
                else:
                    continue
            else:
                continue   
    #END: US09

    #Print out all loaded information for troubleshooting
    sorted_keys = natural_sort(individuals)
    for i in sorted_keys:
        individuals[i].printIndividual()
        print
    print

    sorted_keys = natural_sort(families)
    for i in sorted_keys:
        families[i].printFamily()
        print
    print "END: " + filename
    print
    

        
readGEDCOM('GEDCOMFile.ged')
readGEDCOM('gedcom_test_files/us01.ged')
readGEDCOM('gedcom_test_files/us03.ged')
readGEDCOM('gedcom_test_files/us05.ged')
readGEDCOM('gedcom_test_files/us09.ged')
readGEDCOM('gedcom_test_files/us11.ged')
