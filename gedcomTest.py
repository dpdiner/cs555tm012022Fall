import unittest
import Team_1_Gedcom_Project
import individual
import family
import datetime
import io
import sys

def makeTestIndividual(ident = "I1"):
    indiv = individual.individual()
    indiv.identifier = ident
    indiv.name = "Christie Lee"
    indiv.gender = "F"
    indiv.birthday = datetime.datetime(1983, 4, 7).date()
    indiv.alive = True
    indiv.spouseFam = ["F1"]
    indiv.calculateAge()
    return indiv

def makeTestFamily(ident = "F1"):
    fam = family.family()
    fam.identifier = ident
    fam.husbandId = "I1"
    fam.wifeId = "I2"
    fam.married = datetime.datetime(2003, 4, 7).date()
    return fam

class TestGedcom(unittest.TestCase):

    def testUserStory3(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        
        fam1 = makeTestFamily()
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        
        # create an individual whose death is before their birthday
        individual1.alive = False
        individual1.deathday = datetime.datetime(1980, 4, 7).date()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals, {fam1.identifier:fam1})
        
        # check that the dead individual's information has been updated
        self.assertEqual(capturedOutput.getvalue() , "ERROR: INDVIDUAL: US03: I1: The birthday is after the deathday\n")
        sys.stdout = sys.__stdout__

    def testUserStory6(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        fam = makeTestFamily()
        
        fam.married = datetime.datetime(2005, 7, 4).date()
        fam.isDivorced = True
        fam.divorced = datetime.datetime(2010, 7, 4).date()
        families = {fam.identifier:fam}
        
        indiv1 = makeTestIndividual()
        indiv1.alive = False
        indiv1.deathday = datetime.datetime(2010, 7, 3).date()
        indiv1.gender = "M"
        indiv2 = makeTestIndividual()
        indiv2.identifier = "I2"
        
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2}
        
        families = Team_1_Gedcom_Project.errorCheckFamilies(families, individuals)
        
        # check that no error output was made
        self.assertEqual(capturedOutput.getvalue() , "ERROR: FAMILY: US06: F1: The husband deathday is before the divorce day\n")
        sys.stdout = sys.__stdout__

    def testUserStory10(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        
        fam = makeTestFamily("F1")
        fam.married = datetime.datetime(1985, 7, 4).date()
        families = {fam.identifier:fam}
        
        indiv1 = makeTestIndividual("I1")
        indiv1.gender = "M"
        indiv2 = makeTestIndividual("I2")
        
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2}
        
        families = Team_1_Gedcom_Project.US10MarriedAfter14(families, individuals)
        
        outputString = "ERROR: FAMILY: US10: F1: The husband was less than 14 years old at their wedding day\nERROR: FAMILY: US10: F1: The wife was less than 14 years old at their wedding day\n"
        
        # check that no error output was made
        self.assertEqual(capturedOutput.getvalue() , outputString)
        sys.stdout = sys.__stdout__

    def testBigmay(self):
        fam1 = makeTestFamily()
        fam2 = makeTestFamily()
        indiv1 = makeTestIndividual()
        indiv2 = makeTestIndividual()
        indiv3 = makeTestIndividual()
        indiv1.married = True
        indiv2.identifier = "I2"
        indiv3.identifier = "I3"
        fam2.wifeId = "I3"
        families = {fam1.identifier:fam1, fam2.identifier: fam2}
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2, indiv3.identifier: indiv3}
        
        families = Team_1_Gedcom_Project.errorCheckFamilies(families, individuals)
        self.assertEqual(indiv1.married, True)
        
    def testParentsOlderThanChild(self):
        fam1 = makeTestFamily()
        indiv1 = makeTestIndividual()
        indiv2 = makeTestIndividual()
        indiv3 = makeTestIndividual()
        indiv1.married = True
        fam1.children = {"I3"}
        indiv2.identifier = "I2"
        indiv3.identifier = "I3"
        families = {fam1.identifier:fam1}
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2, indiv3.identifier: indiv3}
        families = Team_1_Gedcom_Project.errorCheckFamilies(families, individuals)
        self.assertEqual(fam1.children, {"I3"})

    def testUserStory27(self):
    
        # Create an individual
        indiv = individual.individual()
        indiv.identifier = "I1"
        indiv.name = "Christie Lee"
        indiv.gender = "F"
        indiv.birthday = datetime.datetime(1983, 4, 7).date()
        indiv.alive = False
        indiv.deathday = datetime.datetime(2022, 10, 17).date()
        indiv.spouseFam = ["F1"]
        
        # check that the individuals age starts off at 0
        self.assertEqual(indiv.age, 0)
        
        # Calculate the age
        indiv.calculateAge()
        
        # check that the individuals age is now 39
        self.assertEqual(indiv.age, 39)
        
    def testUserStory18(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        fam1 = makeTestFamily()
        
        # Create two families where the children of the first family are the spouses in the second
        individual1 = makeTestIndividual("I1")
        individual1.gender = "M"
        individual2 = makeTestIndividual("I2")
        
        individual3 = makeTestIndividual("I3")
        individual3.spouseFam = ["F2"]
        individual3.childFam = ["F1"]
        individual3.gender = "M"
        
        individual4 = makeTestIndividual("I4")
        individual4.spouseFam = ["F2"]
        individual4.childFam = ["F1"]
        
        fam1 = makeTestFamily("F1")
        fam1.children = ["I3", "I4"]
        fam2 = makeTestFamily("F2")
        fam2.husbandId = "I3"
        fam2.wifeId = "I4"

        # Put the families and individuals into lists
        individuals = {individual1.identifier:individual1, individual2.identifier:individual2, 
                       individual3.identifier:individual3, individual4.identifier:individual4}
        families =    {fam1.identifier:fam1, fam2.identifier:fam2}

        # run the error checker
        individuals = Team_1_Gedcom_Project.US18SiblingsShouldNotMarry(families, individuals)
        
        # check that the correct error output was made
        self.assertEqual(capturedOutput.getvalue() , "ERROR: FAMILY: US18: F1: Two of the children in this family are married to each other\n")
        sys.stdout = sys.__stdout__
        
    def testUserStory9Num1(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        fam1 = makeTestFamily()
        
        # Create a family with 2 children where child is born after the death of the mother
        individual1 = makeTestIndividual("I1")
        individual1.gender = "M"
        individual2 = makeTestIndividual("I2")
        individual2.deathday = datetime.datetime(2019, 1, 1).date()
        individual2.alive = False
        
        individual3 = makeTestIndividual("I3")
        individual3.childFam = ["F1"]
        individual3.birthday = datetime.datetime(2020, 1, 1).date()
        
        fam1 = makeTestFamily("F1")
        fam1.children = ["I3"]

        # Put the families and individuals into lists
        individuals = {individual1.identifier:individual1, individual2.identifier:individual2, 
                       individual3.identifier:individual3}
        families =    {fam1.identifier:fam1}

        # run the error checker
        individuals = Team_1_Gedcom_Project.US09MBirthBeforeDeathOfParents(families, individuals)
        
        # check that the correct error output was made
        self.assertEqual(capturedOutput.getvalue() , "ERROR: FAMILY: US09: F1: One of the children was born before a parent died\n")
        sys.stdout = sys.__stdout__
        
    def testUserStory9Num2(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        fam1 = makeTestFamily()
        
        # Create a family with 2 children where child is born more than 9 months after the death of the father
        individual1 = makeTestIndividual("I1")
        individual1.gender = "M"
        individual2 = makeTestIndividual("I2")
        individual2.deathday = datetime.datetime(2019, 1, 1).date()
        individual2.alive = False
        
        individual3 = makeTestIndividual("I3")
        individual3.childFam = ["F1"]
        individual3.birthday = datetime.datetime(2020, 1, 1).date()
        
        fam1 = makeTestFamily("F1")
        fam1.children = ["I3"]

        # Put the families and individuals into lists
        individuals = {individual1.identifier:individual1, individual2.identifier:individual2, 
                       individual3.identifier:individual3}
        families =    {fam1.identifier:fam1}

        # run the error checker
        individuals = Team_1_Gedcom_Project.US09MBirthBeforeDeathOfParents(families, individuals)
        
        # check that the correct error output was made
        self.assertEqual(capturedOutput.getvalue() , "ERROR: FAMILY: US09: F1: One of the children was born before a parent died\n")
        sys.stdout = sys.__stdout__
        
    def testUserStory25(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        
        # Create one family where the children have the same name and birthday
        individual1 = makeTestIndividual("I1")
        individual1.gender = "M"
        individual2 = makeTestIndividual("I2")
        
        individual3 = makeTestIndividual("I3")
        individual3.childFam = ["F1"]
        individual3.birthday = datetime.datetime(2014, 4, 7).date()
        
        individual4 = makeTestIndividual("I4")
        individual4.childFam = ["F1"]
        individual4.birthday = datetime.datetime(2014, 4, 7).date()
        
        fam1 = makeTestFamily("F1")
        fam1.children = ["I3", "I4"]

        # Put the families and individuals into lists
        individuals = {individual1.identifier:individual1, individual2.identifier:individual2, 
                       individual3.identifier:individual3, individual4.identifier:individual4}
        families =    {fam1.identifier:fam1}

        # run the error checker
        individuals = Team_1_Gedcom_Project.US25UniqueFirstNameInFamily(families, individuals)
        
        # check that the correct error output was made
        self.assertEqual(capturedOutput.getvalue() , "ERROR: FAMILY: US25: F1: Two of the children in this family named Christie have the same name and birthday\n")
        sys.stdout = sys.__stdout__
if __name__ == '__main__':
    unittest.main()