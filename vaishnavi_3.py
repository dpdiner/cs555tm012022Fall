import sys
import individual
import family
import datetime
from prettytable import PrettyTable
from dateutil.relativedelta import relativedelta
import re

validTags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "MARR", "HUSB", 
             "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE", "FAMS", 
             "FAM"]

def printErrorInfo(story, Id, message):
    if "I" in Id:
        itemAffected = "INDVIDUAL"
    else:
        itemAffected = "FAMILY"
        
    print("ERROR: " + itemAffected + ": " + story + ": " + Id + ": " + message)

# takes in the date string used in a Gedcom file and returns a date object of that date
def getDate(dateString):
    monthDict = {"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, 
                 "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
    date = dateString.split()
    day = int(date[0])
    month = monthDict[date[1]]
    year = int(date[2])
    return datetime.datetime(year, month, day).date()

# takes in a Gedcom tag and returns if it is valid
def isTagValid(tag):
    return tag in validTags



def isDateGreaterThanCurrentDate(date):
    currentDate = datetime.date.today()
    return date > currentDate

# Returns is the first date passed to it is smaller than the second. Second date defaults to todays date
#def isDateSmallerThanOtherDate(firstDate, secondDate = datetime.date.today()):
#    return firstDate < secondDate

# takes in a list of Gedcom rows pertaining to an individual and returns an indvidual object
def readIndividual(rowList):
    newIndiv = individual()
    
    # Booleans for tracking if we are reading in birth and death dates
    readingBirth = False
    readingDeath = False
    
    for row in rowList:
        # if the level is 1 then that means we are no longer reading in birth or death dates
        if int(row[0]) == 1:
            readingBirth = False
            readingDeath = False
        
        # Reads each row and sets the corresponding field in the individual object
        if row[1] == "INDI":
            newIndiv.identifier = row[2].strip()
        elif row[1] == "NAME":
            newIndiv.name = row[2].strip()
        elif row[1] == "SEX":
            newIndiv.gender = row[2].strip()
        elif row[1] == "DEAT":
            if "Y" == row[2].strip():
                # Begin reading in the death date
                readingDeath = True
                newIndiv.alive = False
            else:
                newIndiv.alive = True
        elif row[1] == "BIRT":
            # Begin reading in the birth date
            readingBirth = True
        elif int(row[0]) == 2 and row[1] == "DATE":
            if readingBirth:
                newIndiv.birthday = getDate(row[2].strip())
            elif readingDeath:
                newIndiv.deathday = getDate(row[2].strip())
        elif row[1] == "FAMS":
            newIndiv.spouseFam.append(row[2].strip())
        elif row[1] == "FAMC":
            newIndiv.childFam.append(row[2].strip())
    
    newIndiv.calculateAge()
    return newIndiv

# Check for errors in data for the individuals
def errorCheckIndividuals(indivs):
    for individual in indivs.values():
        if ((not individual.alive and individual.deathday < individual.birthday) ):
            printErrorInfo("US03", individual.identifier, "The birthday is before the deathday")
        if individual.age >150:
            printErrorInfo("US07", individual.identifier, "The person is over 150")
        if( isDateGreaterThanCurrentDate(individual.birthday)):
            printErrorInfo("US01", individual.identifier, "The birthday is before the current day")
        if individual.deathday > datetime.date.today():
            printErrorInfo("US01", individual.identifier, "The deathday is before the current day")
    return indivs

# Check for errors for the families
def errorCheckFamilies(fams, indivs):
    for family in fams.values():
        if family.isDivorced:
            if (not indivs[family.husbandId].alive and indivs[family.husbandId].deathday < family.divorced):
                printErrorInfo("US06", family.identifier, "The husband deathday is before the divorce day")
            elif (not indivs[family.wifeId].alive and indivs[family.wifeId].deathday < family.divorced):
                printErrorInfo("US06", family.identifier, "The wife deathday is before the divorce day")
            if isDateGreaterThanCurrentDate(family.divorced): 
                printErrorInfo("US01", family.identifier, "The divorce day is before the current day")
        if isDateGreaterThanCurrentDate(family.married):
            printErrorInfo("US01", family.identifier, "The marriage day is before the current day")
        if indivs[family.husbandId].birthday > family.married:
            printErrorInfo("US02", family.identifier, "The husband birthday is before the marriage day")
        elif indivs[family.wifeId].birthday > family.married :
            printErrorInfo("US02", family.identifier, "The wife birthday is before the marriage day")
    return fams

            
# takes in a list of Gedcom rows pertaining to an family and returns an family object
def readFamily(rowList):
    newFam = family()
    
    # Booleans for tracking if we are reading in marriage and divorce dates
    readingMarriage = False
    readingDivorce = False
    
    for row in rowList:
        # if the level is 1 then that means we are no longer reading in marriage or divorce dates
        if int(row[0]) == 1:
            readingMarriage = False
            readingDivorce = False
        
        # Reads each row and sets the corresponding field in the family object    
        if row[1] == "FAM":
            newFam.identifier = row[2].strip()
        elif row[1] == "HUSB":
            newFam.husbandId = row[2].strip()
        elif row[1] == "WIFE":
            newFam.wifeId = row[2].strip()
        elif row[1] == "CHIL":
            newFam.children.append(row[2].strip())
        elif row[1] == "DIV":
            # Begin reading in the divorce date
            readingDivorce = True
            newFam.isDivorced = True
        elif row[1] == "MARR":
            # Begin reading in the marriage date
            readingMarriage = True
        elif int(row[0]) == 2 and row[1] == "DATE":
            if readingMarriage:
                newFam.married = getDate(row[2].strip())
            elif readingDivorce:
                newFam.isDivorced = True
                newFam.divorced = getDate(row[2].strip())
            if newFam.married > newFam.divorced:
              newFam.Marriagebefordivorce = True
            elif newFam.married < newFam.divorced:
              newFam.Marriagebefordivorce = False
                
    return newFam

# Print out the individuals and families from the Gedcom file using prettytable
def printOutput(individuals, families):
    indPT = PrettyTable()
    famPT = PrettyTable()

    indPT.field_names = ["ID", "NAME", "GENDER", "BIRTHDAY", "AGE", "ALIVE", "DEATH", "CHILD", "SPOUSE","Last Name"]
    famPT.field_names = ["ID", "MARRIED", "DIVORCED", "MARRIED BEFORE DIVORCE","MARRIED BEFORE DEATH","Married before 14","Child's Birth before death","HUSBAND ID", "HUSBAND NAME", "WIFE ID", "WIFE NAME", "CHILDREN","Siblings Less than 15"]

   for individual in sorted(individuals.keys()):
        ind = individ uals[individual]
        if ind.gender == "M":
          name = re.search('/(.*)/', ind.name)
          last_name = name.group(1)
        else:
          last_name = "N/A"

        indPT.add_row([ind.identifier, ind.name, ind.gender, ind.getBirthday(), ind.age, ind.alive, ind.getDeathday(), ind.getChildFam(), ind.getSpouseFam(),last_name])
    for family in sorted(families.keys()):
        fam = families[family]
        if len(fam.getChildren()) < 15:
          siblings_less_than_15 = True
        else :
          siblings_less_than_15 = False
        famPT.add_row([fam.identifier, fam.married, fam.getIsDivorced(), fam.Marriagebefordivorce,fam.Marriagebedoredeath,fam.Marriagebefore14,fam.childbdate,fam.husbandId, fam.husbandName, fam.wifeId, fam.wifeName, fam.getChildren(),siblings_less_than_15])
        
    print("Individuals")
    print(indPT)
    print("Families")
    print(famPT)

# Process the Gedcom file and store it
def processGedcomFile(file):
    
    individuals = {}
    families = {}

    # Booleans to keep track of when we are reading a family in and when we are reading an individual
    readingIndividual = False
    readingFamily = False
    
    # List for the lines that correspond to the family or individual we are reading in
    linesList = []
    
    for line in file:
        
        splitLine = line.split()
        # get the level for the Gedcom line
        level = splitLine.pop(0)
        
        # get the tag and argument for the Gedcom line
        if len(splitLine) == 1:
            tag = splitLine[0]
            arguments = ""
        else:
            if splitLine[1] == "INDI" or splitLine[1] == "FAM":
                tag = splitLine.pop(1)
            else:
                tag = splitLine.pop(0)

            arguments = ""
            for word in splitLine:
                arguments = arguments + word + " "
        
        # Level 0 marks the start of a new family or individual
        if int(level) == 0:
            # stop reading in for the previous family or individual and add them to teh appropriate dictionary
            if readingIndividual:
                newIndividual = readIndividual(linesList)
                individuals[newIndividual.identifier] = newIndividual
            if readingFamily:
                newFamily = readFamily(linesList)
                families[newFamily.identifier] = newFamily
            
            # start reading in for a new individual
            if tag == "INDI":
                readingIndividual = True
                readingFamily = False
                linesList = []
            # start reading in for a new family
            elif tag == "FAM":
                readingIndividual = False
                readingFamily = True
                linesList = []
            # stop reading in at all
            else:
                readingIndividual = False
                readingFamily = False
        
        if isTagValid(tag):
            linesList.append([level, tag, arguments])
        
        # Add the parents names to the families
        if True:
          for family in families.keys():
            #print(families[family].childern)
            families[family].husbandName = individuals[families[family].husbandId].name
            families[family].wifeName = individuals[families[family].wifeId].name
            families[family].wddate = individuals[families[family].wifeId].deathday
            wifedeathdate = individuals[families[family].wifeId].deathday
            families[family].Hddate = individuals[families[family].husbandId].deathday
            husbanddeathdate = individuals[families[family].husbandId].deathday
            families[family].wbdate = individuals[families[family].wifeId].birthday
            families[family].hbdate = individuals[families[family].husbandId].birthday
            if ((families[family].married < families[family].wddate) or (families[family].married < families[family].Hddate)):
              families[family].Marriagebedoredeath = True
            elif ((families[family].wddate == families[family].Hddate)):
                families[family].Marriagebedoredeath = True
            else:
                families[family].Marriagebedoredeath = False
                printErrorInfo("US05", families[family].identifier, "One of the couple died before the marriage")
            if((relativedelta(families[family].married,families[family].hbdate).years)<14 and (relativedelta(families[family].married,families[family].wbdate).years)<14 ):
              families[family].Marriagebefore14 = True
            else:
              families[family].Marriagebefore14 = False
            if True:
              for family in families.values():
                familyID = family.identifier
                husbanddeathday = individuals[family.husbandId].deathday
                #print(husbanddeathdate)
                wifedeathday = individuals[family.wifeId].deathday
                for child in family.children:
                  # print(child)
                  #print(individuals[child].birthday)
                  #print(husbanddeathdate)   
                  if(husbanddeathdate  <= individuals[child].birthday) and (wifedeathdate <= individuals[child].birthday):
                    # print(True)
                    family.childbdate = True
                  elif(husbanddeathdate  < wifedeathdate ):
                    # print(True)
                    family.childbdate = True
    # Run checks
    individuals = errorCheckIndividuals(individuals)
    families = errorCheckFamilies(families, individuals)
    famliyFunc(families,individuals)

        
    return [individuals, families]

def famliyFunc(families,individuals):
    for i in families.values():
        childKeys = i.children
        birthday_dates = []
        for j in childKeys:
            birthday_dates.append(individuals[j].birthday)
        for birthdays in birthday_dates:
            if i.married > birthdays :
                printErrorInfo("US08", j, "Birthday of child is before the marriage of their parents")

            new_div_date = datetime.date(i.divorced.year + int(i.divorced.month / 12), (i.divorced.month + 9) %12, i.divorced.day)
            if new_div_date < birthdays and i.isDivorced:
                printErrorInfo("US08", j, "Birthday of child is after the divorce of their parents")

def main():
  if len(sys.argv) == 2:
    try:
      file = open("/content/Team_1_Gedcom_Project_Input.ged")
      output = processGedcomFile(file)
      printOutput(output[0], output[1])
      except OSError:
        print("Error opening GEDCOM FILE.")
  else:
    print("Error in number of arguments. Please provide the name of one GEDCOM file.")
    
    
if __name__ == "__main__":
    main()
