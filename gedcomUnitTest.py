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

    def testUserStory1(self):
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
    
    def testUserStory2(self):
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

    def testUserStory3(self):
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

    def testUserStory4(self):
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
        
    def testUserStory5(self):
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




if __name__ == '__main__':
    unittest.main()