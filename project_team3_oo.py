#Team3
#This program shall read data from a GEDCOM file and store information for
#individuals and families in lists
import datetime, re

from datetime import date


tags0_norm = ['HEAD', 'TRLR', 'NOTE']
tags0_id = ['INDI', 'FAM']
tags1 = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
tags2 = ['DATE']
today = datetime.datetime.now().date()
errors = {}

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
            addError("US11", "ERROR: User story 11 - A husband in family " + self.id + " is married to wife but was not divorced first.")
            self.husband = husb
        #End: US11 - No bigamy
        else:
            self.husband = husb
            Family.members += 1
        
    def addWife(self, wife):
        #BEGIN: US11 - No bigamy
        if Family.members > 1:
            addError("US11", "ERROR: User story 11 - A wife in family " + self.id + " is married to wife but was not divorced first.")
            self.wife = wife
        #End: US11 - No bigamy
        else:
            self.wife = wife
            Family.members += 1
        
    def addChild(self, child):
        self.children.append(child)
        Family.members += 1

        #BEGIN: US13 - Sibling Spacing
        for child in self.children:
            for child1 in self.children:
                if child is child1:
                    pass
                elif child is not child1 and bdayDiff(child.birthday, child1.birthday) is True:
                    addError("US13", "ERROR: User Story 13 - Sibling birthdays are between 2 days and 8 months apart.")
                else:
                    pass
        #END: US13

        #BEGIN: US14 - Multiple births less than 5
        for child in self.children:
            twinCount = 0
            for child1 in self.children:
                if child is child1:
                    pass
                elif child is not child1 and child.birthday == child1.birthday:
                    twinCount += 1
                else:
                    pass
        if twinCount > 4:           
            addError("US14", "ERROR: User Story 14 - More than 5 siblings in famliy " + self.id + " were born on the same day.")
        #END: US14
        
        #BEGIN: US15 - Fewer than 15 siblings
        if len(self.children) >= 15:
            addError("US15", "ERROR: User story 15 - Family should have fewer than 15 siblings. Number of Children: " + str(len(self.children)))
        else:
            pass
        #END: US15

        #BEGIN: US25 - Unique first names in families
        for child1 in self.children:
            for child2 in self.children:
                if child1 is child2:
                    continue
                elif child1.name.partition(' ')[0] == child2.name.partition(' ')[0] and child1.birthday == child2.birthday:
                    addError("US25", "ERROR: User story 25 - child " + child1.id + " and child " + child2.id + " share the same first name and birthday.")
        #END: US25


    def addMarried(self, date):
        marriage_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US05 - Marriage before death
        if(isAfterDate(marriage_date, self.husband.death) or isAfterDate(marriage_date, self.wife.death)):
            addError("US5", "ERROR: User story 5 - Marriage date " + str(marriage_date) + " for family " + self.id + " after death of spouse")
        #END: US05
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(marriage_date, today)):
            addError("US1", "ERROR: User story 1 - Marriage date " + str(marriage_date) + " for family " + self.id + " after today's date")
        #END: US01
        #BEGIN: US10 - Marriage after 14
        if ((marriage_date - self.husband.birthday).days/365.0) <= 14:
            addError("US10","ERROR: User story 10 - " + self.husband.name + " has a marriage date before he turns 14 years old")
        if ((marriage_date - self.wife.birthday).days/365.0) <= 14:
            addError("US10","ERROR: User story 10 - " + self.wife.name + " has a marriage date before she turns 14 years old")
        #END: US10
        self.married = marriage_date
        
    def addDivorced(self, date):
        divorce_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(divorce_date, today)):
            addError("US1", "ERROR: User story 1 - Divorce date " + str(divorce_date) + " for family " + self.id + " after today's date")
        #END: US01
        self.divorced = divorce_date
        
    def numMembers(self):
        return Family.members
        
    def printFamily(self):
        print self.id
        print "Married: " + str(self.married)
        print "Divorced: " + str(self.divorced)
        if self.husband:
            print "Husband: " + self.husband.name
        else:
            print "Husband: None"
        if self.wife:
            print "Wife: " + self.wife.name
        else:
            print "Wife: None"
        print "Children:",
        if self.children == []:
            print "None"
        else:
            for child in self.children:
                if child != self.children[-1]:
                    print child.name + ",",
                else:
                    print child.name

#Function to evaluate if the distance between sibling's birthdays is between 2 days and 8 months
def bdayDiff(bday1, bday2):
    """Function:     bdayDiff
	   Purpose:      Returns whether bday1 is between 2 days and 8 months from bday2
	   Parameters:   bday1 - datetime.date object | bday2 - datetime.date object
	   Return value: Boolean
	"""
    bdaySub = (bday1 - bday2).days
    if (bdaySub > 2) and (bdaySub < 240):
        return True
    else:
        return False

def listChildrenByAge(family, children):
    """Function:     listChildrenByAge
       Purpose:      Lists children of a family in order from oldest to youngest.
       Parameters:   Receives the "children" array within a given family.
       Return value: Void
    """
    ret = "LIST: User Story 28 - Order siblings by age - Family " + family.id + ": " 
    while len(children) > 0:
        oldest = children[0]
        for child in children:
            if age(child.birthday, child.death) > age(oldest.birthday, oldest.death):
                oldest = child
        if len(children) != 1:
            ret += oldest.name + ", "
        else:
            ret += oldest.name
        children.remove(oldest)
    addError("US28", ret)
        
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
            addError("US1", "ERROR: User story 1 - Birthday " + str(birth_date) + " for individual " + self.id + " after today's date")
        #END: US01
        #BEGIN: US03 - Birth before death
        if(isAfterDate(birth_date, self.death)):
            addError("US3", "ERROR: User story 3 - Birthday " + str(birth_date) + " for individual " + self.id + " after individual's death date")
        #END: US03

        self.birthday = birth_date
        
        
    def addDeath(self, date):
        death_date = datetime.datetime.strptime(" ".join(date), '%d %b %Y').date()
        #BEGIN: US01 - Dates before current date
        if(isAfterDate(death_date, today)):
            addError("US1", "ERROR: User story 1 - Death Date " + str(death_date) + " for individual " + self.id + " after today's date")
        #END: US01
        #BEGIN: US03 - Birth before death
        if(isAfterDate(self.birthday, death_date)):
            addError("US3", "ERROR: User story 3 - Death date " + str(death_date) + " for individual " + self.id + " before individual's birth date ")
        #END: US03
        
        #BEGIN: US29 - List all Deseased
        if self.death != "None":
            addError("US29", "LIST: User Story 29 - The following individual is deceased: " + self.name)
        #END: US29
        
        
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

        #BEGIN: US27 - Include individual ages
        print "Age: " + str(age(self.birthday, self.death))
        #END: US27 - Include individual ages

    
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

    
def daysAlive(birthday):
    """Function:     daysFromBirth
       Purpose:      Days since an individual was born
       Parameters:   birth
       Return value: int
    """
    today = date.today()
    daysAlive = today - birthday
    return daysAlive.days


def daysDead(death):
    """Function:     daysFromDeath
       Purpose:      Days since an individual died
       Parameters:   death
       Return value: int
    """
    today = date.today()
    if(death):
        daysDead = today - death
        return daysDead.days



def age(birth, death):
    """Function:     age
       Purpose:      Returns the age of the person with provided birth and death dates.
       Parameters:   birth - the birthday of the individual. death - the death date of the individual.
       Return value: Integer (years)
    """
    if(death):
        return death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))
    else:
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

def addError(userStory, errormessage):
      errors.setdefault(userStory, []).append(errormessage)


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
                        #BEGIN: US22 - Unique IDs
                        if curr_indi in individuals:
                            addError("US22","ERROR: User Story 22 - All individual IDs must be unique. Will not add second individual with ID: " + curr_indi)
                        else:
                            individuals[curr_indi] = Individual(curr_indi)
                        curr_fam = ''
                    else:
                        curr_fam = parts[1].replace("@","")
                        if curr_fam in families:
                            addError("US22", "ERROR: User Story 22 - All family IDs must be unique. Will not add second family with ID: " + curr_fam)
                        else:
                            families[curr_fam] = Family(curr_fam)
                        curr_indi = ''
                        #END: US22
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
			
    #BEGIN: US06 - Divorce before death
    for fam in families:
        if families[fam].divorced != None:
            compare = families[fam].divorced
            if families[fam].husband.death is not None: 
                comph = families[fam].husband.death
                if comph <= compare:
                    addError("US6", "ERROR: User Story 6 - Husband, " + families[fam].husband.name + " was divorced after death.")
                else:
                    continue
            if families[fam].wife.death is not None:
                compw = families[fam].wife.death
                if compw <= compare:
                    addError("US6", "ERROR: User Story 6 - Wife, " + families[fam].wife.name + "  was divorced after death.")
                else:
                    continue
            else:
                continue
        else:
            continue   
    #END: US06

    #BEGIN: US08 - Birth before marriage of parents
    for fam in families:
        for child in families[fam].children: 
            if families[fam].married is not None: 
                if isAfterDate(families[fam].married, child.birthday):
                    addError("US8", "ERROR: User Story 8- Child " + child.name + " born on " + str(child.birthday) + " and parents marriage occured later on" + str(families[fam].married))
                else:
                    continue
            else:
                continue
        else:
            continue
    #END: US08

    #BEGIN: US09 - Death before child brith
    for fam in families: #Finding keys in dictionary.  Go throught the family first... Then go through the child list.
        for child in families[fam].children: #Use key to get family... next look at the family.
            delta = datetime.timedelta(days=(9 * 30)) #9 months times 30 days.
            if families[fam].husband:
                if families[fam].husband.death is not None: #If the husband didn't die, skip.
                    if isAfterDate(families[fam].husband.death - delta, child.birthday):
                        addError("US9", "ERROR: User Story 9 - Child born less than 9 months after father's death.  Dead father: " + families[fam].husband.name + "  Child: " + child.name)
                    else:
                        continue
            if families[fam].wife:
                if families[fam].wife.death is not None:  # If the wife is not dead, skip.
                    if child.birthday is not None: #If the child does not have a birthday, skip.
                        if isAfterDate(families[fam].wife.death, child.birthday): #If the child is not born before mother's death, skip.
                            addError("US9", "ERROR: User Story 9 - Child born after mother's death.  Dead mother: " + families[fam].wife.name + "  Child: " + child.name)
                        else:
                            continue
                    else:
                        continue
                else:
                    continue   
    #END: US09

    #BEGIN: US07 - Less than 150 years old
    for indi in individuals:
        if individuals[indi].death:
            if((individuals[indi].death - datetime.timedelta(days=150*365) >= individuals[indi].birthday)):
                addError("US7", "ERROR: User story 7 - Birthday " + str(individuals[indi].birthday) + " and death date " + str(individuals[indi].death) + " for individual " + individuals[indi].id + " makes them over 150 years old")
        elif individuals[indi].birthday:
            if(individuals[indi].birthday <= (today - datetime.timedelta(days=150*365))):
                addError("US7", "ERROR: User story 7 - Birthday " + str(individuals[indi].birthday) + " and no death date for individual " + individuals[indi].id + " makes them over 150 years old")
    #END: US07

    #Begin: US17 - No marrages to decendants
    for indi in individuals:
        if individuals[indi].famc == individuals[indi].fams:
            addError("US17", "ERROR: User story 17 - The decendant " + individuals[indi].name + " is a spouse in the family " + individuals[indi].fams)
        else:
            continue
    #END: US17

    #BEGIN: US19 - First cousins should not marry
    for indi in individuals:
        childOfFam = individuals[indi].famc
        spouseOfFam = individuals[indi].fams
        spouseParFam = ''
        if childOfFam != '' and spouseOfFam != '':
            indParFam = [families[childOfFam].husband.famc, families[childOfFam].wife.famc]
            if individuals[indi].sex == "F":
                try:
                    spouseParFam = [families[families[spouseOfFam].husband.famc].husband.famc, families[families[spouseOfFam].husband.famc].wife.famc]
                except KeyError:
                    pass
            else:
                try:
                    spouseParFam = [families[families[spouseOfFam].wife.famc].husband.famc, families[families[spouseOfFam].wife.famc].wife.famc]
                except KeyError:
                    pass
            if len(list(set(filter(None,indParFam)).intersection(filter(None,spouseParFam)))) > 0:
                addError("US19", "ERROR: User story 19 - " + individuals[indi].name + " is married to first cousin ")
    #END: US19

    #BEGIN: US21 - Correct gender for role
    for fam in families:
        if families[fam].husband:
            if families[fam].husband.sex != "M":
                addError("US21", "ERROR: User story 21 - " + families[fam].husband.name + " has the wrong gender for role.  Husband is " + families[fam].husband.sex + "emale.")
        if families[fam].wife:
            if families[fam].wife.sex != "F":
                addError("US21", "ERROR: User story 21 - " + families[fam].wife.name + " has the wrong gender for role.  Wife is " + families[fam].wife.sex + "ale.")
        else:
            continue
    #END: US21
    
    
    
    #Begin: US31 - Living Single
    for indi in individuals:
        if individuals[indi].death is None and age(individuals[indi].birthday, individuals[indi].death) > 30 and individuals[indi].fams == '':
            addError("US31", "LIST: User Story 31 - Individual is Living / Single / Over Age 30: " + individuals[indi].name)
        else:
            pass
    #END: US17
    
    

    #BEGIN: US23 - Unique name and birth date
    for indi in individuals:
        for indi2 in individuals:
            if indi2 is indi:
                continue
            elif individuals[indi].name == individuals[indi2].name and individuals[indi].birthday == individuals[indi2].birthday:
                addError("US23", "ERROR: User story 23 - Individual " +  individuals[indi].id +  " and " + individuals[indi2].id + " with birthday " + str(individuals[indi].birthday) + " appear twice")

    #END: US23
    
    #BEGIN: US12 - Parents not too old
    for fam in families:
        wife = families[fam].wife
        husband = families[fam].husband
        children = families[fam].children
        for child in children:
            if (age(wife.birthday, wife.death) - age(child.birthday, child.death)) >= 60:
                    addError("US12", "ERROR: User story 12 - Mother: " + wife.name + " is more than 60 years older than Child: " + child.name)
            elif age(husband.birthday, husband.death) -age(child.birthday, child.death) >= 80:
                    addError("US12", "ERROR: User story 12 - Father: " + husband.name + " is more than 80 years older than Child: " + child.name)
            else:
                continue
    #END: US12

    #Begin: US18 - Siblings should not marry
    for fam in families:
        if families[fam].wife.famc != '' and (families[fam].wife.famc == families[fam].husband.famc):
            addError("US18", "ERROR: User story 18 - Siblings " + families[fam].wife.name + " and " + families[fam].husband.name + " are married")
        else:
            continue
    #END: US18

    #BEGIN: US02 - Birth before marriage
    for indi in individuals:
        if individuals[indi].fams != '' and individuals[indi].fams in families:
            if isAfterDate(individuals[indi].birthday, families[individuals[indi].fams].married):
                addError("US2", "ERROR: User story 2 - Individual " + individuals[indi].id + " birthday " + str(individuals[indi].birthday) + " after marriage date " + str(families[individuals[indi].fams].married))
    #END: US02

    #BEGIN: US04 - Marriage before divorce
    for fam in families:
        if isAfterDate(families[fam].married, families[fam].divorced):
            addError("US4", "ERROR: User story 4 - Family " + families[fam].id + " divorce date " + str(families[fam].divorced) + " is before marriage date " + str(families[fam].married))
        if families[fam].divorced and not families[fam].married:
            addError("US4", "ERROR: User story 4 - Family " + families[fam].id + " has divorce date " + str(families[fam].divorced) + " without marriage.")
    #END: US04
    


    #BEGIN: US16 - Male Last Names
    for fam in families:        
        husband = families[fam].husband        
        children = families[fam].children    
        for child1 in children:  
            if child1.name.split(' ')[-1] != husband.name.split(' ')[-1]:
                addError("US16", "ERROR: User story 16 - " + child1.name + " has a different last name than " + husband.name)       
            for child2 in children:
                if child1 is child2:
                    pass
                elif child1.sex != "M" or child2.sex != "M":
                    pass
                elif child1.name.split(' ')[-1] != child2.name.split(' ')[-1]:
                    addError("US16", "ERROR: User story 16 - " + child1.name + " has a different last name than " + child2.name)
    #END: US16

    #BEGIN: US20 - Aunts and uncles
    for fam in families:
        for childs1 in families[fam].children:
            if childs1.fams != '':
                if families[fam].wife.famc != families[fam].husband.famc:
                    addError("US20", "ERROR: User story 20 - " + childs1.name + " is married to an aunt or uncle.")
    #END: US20    

    #BEGIN: US24 - Unique familes by spouses
    for fam in families:
        husbn = families[fam].husband.name
        wifen = families[fam].wife.name
        if husbn == wifen:
            print addError("US24", "ERROR: User story 24 - Family " + families[fam].husband.fams + " and " + families[fam].wife.fams + " have spouses with the same name. Husband name: "+ husbn + " and wife name: " + wifen)
    #END: US24  

    #BEGIN: US28 - Order siblings by age
    for fam in families:
        listChildrenByAge(families[fam], families[fam].children)
    #END: US28

    #BEGIN: US30 - List living married
    for indi in individuals:
        if not individuals[indi].death and individuals[indi].fams in families and families[individuals[indi].fams].married and not families[individuals[indi].fams].divorced:
            addError("US30", "LIST: User Story 30 - List living married: " + individuals[indi].name + " is living and married.")
    #END: US30
    
    
    
    #Begin: US35 - List Recent Births
    for indi in individuals:
        if daysAlive(individuals[indi].birthday) >= 0 and daysAlive(individuals[indi].birthday) <=30:
            addError("US35", "LIST: User Story 35 - Individual " + individuals[indi].name + " was born in the last 30 days")
        else:
            continue
    #END: US35
    
    
    #Begin: US36 - List Recent Deaths
    for indi in individuals:
        if individuals[indi].death is 'none':
            pass
        elif daysDead(individuals[indi].death) >= 0 and daysDead(individuals[indi].death) <=30:
            addError("US36", "LIST: User Story 36 - Individual " + individuals[indi].name + " died in the last 30 days")
        else:
            continue
    #END: US36
    

    
    
    
    

    #Print out all errors in order
    sorted_errors = natural_sort(errors)
    for i in sorted_errors:
        for error in errors[i]:
            print error     
    print        

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
    

readGEDCOM('gedcom_test_files/all_us_sprint4.ged')

        
#readGEDCOM('GEDCOMFile.ged')
#readGEDCOM('gedcom_test_files/us01.ged')
#readGEDCOM('gedcom_test_files/us02.ged')
#readGEDCOM('gedcom_test_files/us03.ged')
#readGEDCOM('gedcom_test_files/us04.ged')
#readGEDCOM('gedcom_test_files/us05.ged')
#readGEDCOM('gedcom_test_files/us06.ged')
#readGEDCOM('gedcom_test_files/us07.ged')
#readGEDCOM('gedcom_test_files/us08.ged')
#readGEDCOM('gedcom_test_files/us09.ged')
#readGEDCOM('gedcom_test_files/us10.ged')
#readGEDCOM('gedcom_test_files/us11.ged')
#readGEDCOM('gedcom_test_files/us13.ged')
#readGEDCOM('gedcom_test_files/us14.ged')
#readGEDCOM('gedcom_test_files/us15.ged')
#readGEDCOM('gedcom_test_files/us17.ged')
#readGEDCOM('gedcom_test_files/us18.ged')
##readGEDCOM('gedcom_test_files/us21.ged')
#readGEDCOM('gedcom_test_files/us22.ged')
#readGEDCOM('gedcom_test_files/us24.ged')
#readGEDCOM('gedcom_test_files/us25.ged')
#readGEDCOM('gedcom_test_files/us28.ged')
#readGEDCOM('gedcom_test_files/us31.ged')

