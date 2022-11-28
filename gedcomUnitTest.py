import unittest
import Team_1_Gedcom_Project
import individual
import family
import datetime
import io
import sys
#UnitTests By Rakesh Balaji
def makeTestIndividual():
    indiv = individual.individual()
    indiv.identifier = "I1"
    indiv.name = "Christie Lee"
    indiv.gender = "F"
    indiv.birthday = datetime.datetime(1783, 4, 7).date()
    indiv.alive = True
    indiv.spouseFam = "F1"
    indiv.calculateAge()
    return indiv

def makeTestFamily():
    fam = family.family()
    fam.identifier = "F1"
    fam.husbandId = "I1"
    fam.wifeId = "I2"
    return fam

class TestGedcom(unittest.TestCase):

    def testUserStory7num1(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        # check that the alive individual's information has not changed
        self.assertEqual(capturedOutput.getvalue() , "Age is more than 150\n")
        sys.stdout = sys.__stdout__
    
    def testUserStory7num2(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        individual1.birthday = datetime.datetime(1780,4 ,7).date()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        self.assertEqual(capturedOutput.getvalue() , "Age is more than 150\n")
        sys.stdout = sys.__stdout__

    def testUserStory7num3(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        individual1.birthday = datetime.datetime(1780,4 ,7).date()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        self.assertNotEqual(capturedOutput.getvalue() , "Age is not more than 150\n")
        sys.stdout = sys.__stdout__

    def testUserStory7num4(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        individual1.birthday = datetime.datetime(1780,4 ,7).date()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        self.assertAlmostEqual(capturedOutput.getvalue() , "Age is more than 150\n")
        sys.stdout = sys.__stdout__
        
    def testUserStory7num5(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        individual1.birthday = datetime.datetime(1780,4 ,7).date()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        self.assertIsNotNone(capturedOutput.getvalue() , "Age is more than 150\n")
        sys.stdout = sys.__stdout__
    
    def testUserStory08(self):
        fam1 = makeTestFamily()
        indiv1 = makeTestIndividual()
        indiv1.identifier = "I3"
        indiv1.name ="Jenna"
        indiv1.birthday = datetime.datetime(2000,4 ,7).date()
        fam1.children = {"I3"}
        fam1.husbandId = "I1"
        fam1.wifeId = "I2"
        fam1.isDivorced = True
        fam1.divorced = datetime.datetime(1998,4 ,7).date()

        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        families = {fam1.identifier:fam1}
        individuals = {indiv1.identifier:indiv1}
        families = Team_1_Gedcom_Project.famliyFunc(families, individuals)
        self.assertEqual(capturedOutput.getvalue() ," Birthday is more than 9 months after Divorce\n")
        sys.stdout = sys.__stdout__
        


    def testUserStory29(self):
        def makeTestIndividual():
            indiv = individual.individual()
            indiv.identifier = "I1"
            indiv.name = "Jezebel /Gilbert/"
            indiv.gender = "F"
            indiv.birthday = datetime.datetime(1783, 4, 7).date()
            indiv.alive = False
            indiv.deathday = datetime.datetime(1883, 4, 7).date()
            indiv.spouseFam = "F1"
            indiv.calculateAge()
            return indiv

        def makeTestFamily():
            fam = family.family()
            fam.identifier = "F1"
            fam.husbandId = "I1"
            fam.wifeId = "I2"
            return fam

        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        individual1 = makeTestIndividual() 
        families = makeTestFamily()
        individuals = {individual1.identifier:individual1}
        # run the error checker
        individuals = Team_1_Gedcom_Project.listDeceased(families,individuals)
        self.assertEqual(capturedOutput.getvalue() ,"List of deceased:\nJezebel /Gilbert/\n")
        sys.stdout = sys.__stdout__

    
    def testUserStory30(self):
        def makeTestIndividual():
            indiv = individual.individual()
            indiv.identifier = "I1"
            indiv.name = "Jezebel /Gilbert/"
            indiv.gender = "F"
            indiv.birthday = datetime.datetime(1783, 4, 7).date()
            indiv.alive = True
            indiv.spouseFam = "F1"
            indiv.calculateAge()
            return indiv

        def makeTestFamily():
            fam = family.family()
            fam.identifier = "F1"
            fam.husbandId = "I1"
            fam.wifeId = "I2"
            return fam

        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        individual1 = makeTestIndividual() 
        families = makeTestFamily()
        individuals = {individual1.identifier:individual1}
        # run the error checker
        individuals = Team_1_Gedcom_Project.listLivMarried(families,individuals)
        self.assertEqual(capturedOutput.getvalue() ,"#############User story for list living married#################\nThe members who are living and married are:\nJezebel /Gilbert/\n")
        sys.stdout = sys.__stdout__

    def testUserStory31(self):
        def makeTestIndividual():
            indiv = individual.individual()
            indiv.identifier = "I1"
            indiv.name = "Jezebel /Gilbert/"
            indiv.gender = "F"
            indiv.birthday = datetime.datetime(1993, 4, 7).date()
            indiv.alive = True
            indiv.calculateAge()
            return indiv

        def makeTestFamily():
            fam = family.family()
            fam.identifier = "F1"
            fam.husbandId = "I1"
            fam.wifeId = "I2"
            return fam

        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        individual1 = makeTestIndividual() 
        families = makeTestFamily()
        individuals = {individual1.identifier:individual1}
        families = {families.identifier:families}
        # run the error checker
        individuals = Team_1_Gedcom_Project.listLivingSingle(families,individuals)
        self.assertEqual(capturedOutput.getvalue() ,"###########User story for living single#############\nThe members who are living and single are:\nJezebel /Gilbert/\n")
        sys.stdout = sys.__stdout__

    def testUserStory35(self):
        def makeTestIndividual():
            indiv = individual.individual()
            indiv.identifier = "I1"
            indiv.name = "Jezebel /Gilbert/"
            indiv.gender = "F"
            indiv.birthday = datetime.datetime(2022, 11, 22).date()
            indiv.alive = True
            indiv.calculateAge()
            return indiv

        def makeTestFamily():
            fam = family.family()
            fam.identifier = "F1"
            fam.husbandId = "I1"
            fam.wifeId = "I2"
            return fam

        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        individual1 = makeTestIndividual() 
        families = makeTestFamily()
        individuals = {individual1.identifier:individual1}
        families = {families.identifier:families}
        # run the error checker
        individuals = Team_1_Gedcom_Project.listRecentBirths(families,individuals)
        self.assertEqual(capturedOutput.getvalue() ,"These are the individual(s) were born in the last 30 Days\nJezebel /Gilbert/\n")
        sys.stdout = sys.__stdout__

    def testUserStory32(self):
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        fam = makeTestFamily()
        
        fam.married = datetime.datetime(2005, 7, 4).date()
        fam.isDivorced = True
        fam.divorced = datetime.datetime(2010, 7, 4).date()
        families = {fam.identifier:fam}
        
        indiv1 = makeTestIndividual()
        indiv1.alive = True
        indiv1.birthday = datetime.datetime(2010, 7, 4).date()
        indiv1.gender = "M"
        indiv2 = makeTestIndividual()
        indiv2.identifier = "I2"
        indiv2.alive = True
        indiv2.birthday = datetime.datetime(2010, 7, 4).date()
        indiv2.gender = "M"
        
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2}
        
        families = Team_1_Gedcom_Project.listMultipleBirths(families, individuals)

        self.assertEqual(capturedOutput.getvalue() , "These are the Multiple Births in the GEDCOM file:\n")
        sys.stdout = sys.__stdout__

    def testUserStory33(self):
        fam1 = makeTestFamily()
        indiv1 = makeTestIndividual()
        indiv2 = makeTestIndividual()
        indiv3 = makeTestIndividual()
        indiv1.identifier = "I3"
        indiv1.name ="Jezebel /Gilbert/"
        indiv1.birthday = datetime.datetime(2000,4 ,7).date()
        indiv1.calculateAge()
        indiv2.identifier = "I1"
        indiv2.alive = True
        indiv3.identifier = "I2"
        indiv3.alive = True
        fam1.children = {"I3"}
        fam1.husbandId = "I1"
        fam1.wifeId = "I2"

        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput
        families = {fam1.identifier:fam1}
        individuals = {indiv1.identifier:indiv1}
        families = Team_1_Gedcom_Project.listOrphans(families, individuals)
        self.assertNotEqual(capturedOutput.getvalue() ," These are the orphan children names:\nJezebel /Gilbert/\n")
        sys.stdout = sys.__stdout__





if __name__ == '__main__':
    unittest.main()