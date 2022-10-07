import sys
import individual
import family
import datetime
from prettytable import PrettyTable

validTags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "MARR", "HUSB", 
             "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE", "FAMS", 
             "FAM"]
individuals = {}
families = {}

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

# takes in a list of Gedcom rows pertaining to an individual and returns an indvidual object
def readIndividual(rowList):
    newIndiv = individual.individual()
    
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
    
# takes in a list of Gedcom rows pertaining to an family and returns an family object
def readFamily(rowList):
    newFam = family.family()
    
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
            
    return newFam

# Print out the individuals and families from the Gedcom file using prettytable
def printOutput():
    indPT = PrettyTable()
    famPT = PrettyTable()

    indPT.field_names = ["ID", "NAME", "GENDER", "BIRTHDAY", "AGE", "ALIVE", "DEATH", "CHILD", "SPOUSE"]
    famPT.field_names = ["ID", "MARRIED", "DIVORCED", "HUSBAND ID", "HUSBAND NAME", "WIFE ID", "WIFE NAME", "CHILDREN"]

    for individual in sorted(individuals.keys()):
        ind = individuals[individual]
        indPT.add_row([ind.identifier, ind.name, ind.gender, ind.birthday, ind.age, ind.alive, ind.getDeathday(), ind.getChildFam(), ind.getSpouseFam()])
    for family in sorted(families.keys()):
        fam = families[family]
        famPT.add_row([fam.identifier, fam.married, fam.getIsDivorced(), fam.husbandId, fam.husbandName, fam.wifeId, fam.wifeName, fam.getChildren()])
        
    print("Individuals")
    print(indPT)
    print("Families")
    print(famPT)

# Process teh Gedcom file and store it
def processGedcomFile(file):

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
        for family in families.keys():
            families[family].husbandName = individuals[families[family].husbandId].name
            families[family].wifeName = individuals[families[family].wifeId].name

#code for less than 150 years by Rakesh Balaji.
def less_than_150_years_old():  # US07: Less Than 150 Years Old
    correct_age = True
    notes = []
    for ind in individuals:
        if ind.alive is True:
            
            diff = datetime.now().date() - ind.birth
            if (diff.days / 365.24) > 150:
                notes.append(
                    "{} is over 150 years old! Birthday is {}.".format(ind.name, ind.birth))
                correct_age = False
        else:
            diff = ind.death - ind.birth
            if (diff.days / 365.24) > 150:
                notes.append(
                    "{} was over 150 years old! Birthday is {} and Death is {}.".format(ind.name, (
                        ind.birth, ind.getDeathday())))
                correct_age = False

    if correct_age:
        result = "Every person is within the right age range."
    else:
        result = "One or more individuals are not within the right age range."

    print(
        ["US08", "Less Than 150 Years Old", "\n".join(notes), correct_age, result])

print(less_than_150_years_old())

#code for birth before marriage of parents
def birth_before_marriage(table):  # US02: Birth Before Marriage
    valid_marriage = True
    notes = []

    for fam in families:
        wife_name = families[family].wifeName
        hubby_name =families[family].husbandName
        for ind in individuals:
            if fam.marriage is not None:
                if wife_name == ind.name or hubby_name == ind.name and fam.marriage < ind.birth:
                    notes.append("{} has an incorrect birth and/or marriage date.".format(ind.name))
                    notes.append(
                        "Birth is: {} and Marriage is: {}".format((ind.birth),(fam.marriage)))
                    valid_marriage = False

    if valid_marriage:
        result = "All birth dates were correct"
    else:
        result = "One or more birth/marriage dates were incorrect."

    print(
        ["US08", "Birth Before Marriage", "\n".join(notes), valid_marriage, result])


def main():
    if len(sys.argv) == 2:
        try:
            file = open(sys.argv[1], "r")
            processGedcomFile(file)
            printOutput()
        except OSError:
            print("Error opening GEDCOM FILE.")
    else:
        print("Error in number of arguments. Please provide the name of one GEDCOM file.")
    
    
if __name__ == "__main__":
    main()