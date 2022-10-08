import unittest
import Team_1_Gedcom_Project
import individual
import family
import datetime
import io
import sys

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



if __name__ == '__main__':
    unittest.main()