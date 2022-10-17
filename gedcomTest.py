import unittest
import Team_1_Gedcom_Project
import individual
import family
import datetime

def makeTestIndividual():
    indiv = individual.individual()
    indiv.identifier = "I1"
    indiv.name = "Christie Lee"
    indiv.gender = "F"
    indiv.birthday = datetime.datetime(1983, 4, 7).date()
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

    def test1(self):
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        # check that the alive individual's information has not changed
        self.assertEqual(str(individuals[individual1.identifier].deathday), str(datetime.date.today()))
    
        
    def test2(self):
        # create an individual who is still alive
        individual1 = makeTestIndividual()
        
        # create an individual whose death is before their birthday
        individual1.alive = False
        individual1.deathday = datetime.datetime(1980, 4, 7).date()
        
        individuals = {individual1.identifier:individual1}
        
        # run the error checker
        individuals = Team_1_Gedcom_Project.errorCheckIndividuals(individuals)
        
        # check that the dead individual's information has been updated
        self.assertEqual(str(individuals[individual1.identifier].birthday), str(datetime.datetime(1, 1, 1).date()))

    def test3(self):
        fam = makeTestFamily()
        families = {fam.identifier:fam}
        
        indiv = makeTestIndividual()
        
        individuals = {indiv.identifier:indiv}
        
        families = Team_1_Gedcom_Project.errorCheckFamilies(families, individuals)
        
        self.assertEqual(str(families[fam.identifier].divorced), str(datetime.datetime(1776, 7, 4).date()))
    
    def test4(self):
        fam = makeTestFamily()
        fam.isDivorced = True
        fam.divorced = datetime.datetime(2010, 7, 4).date()
        families = {fam.identifier:fam}
        
        indiv1 = makeTestIndividual()
        indiv2 = makeTestIndividual()
        indiv2.identifier = "I2"
        
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2}
        
        families = Team_1_Gedcom_Project.errorCheckFamilies(families, individuals)
        
        self.assertEqual(str(families[fam.identifier].divorced), str(datetime.datetime(2010, 7, 4).date()))
        
    def test5(self):
        
        fam = makeTestFamily()
        fam.isDivorced = True
        fam.divorced = datetime.datetime(2010, 7, 4).date()
        families = {fam.identifier:fam}
        
        indiv1 = makeTestIndividual()
        indiv2 = makeTestIndividual()
        indiv2.alive = False
        indiv2.deathday = datetime.datetime(2010, 1, 4).date()
        indiv2.identifier = "I2"
        
        individuals = {indiv1.identifier:indiv1, indiv2.identifier:indiv2}
        
        families = Team_1_Gedcom_Project.errorCheckFamilies(families, individuals)
        
        self.assertEqual(str(families[fam.identifier].divorced), str(datetime.datetime(1776, 7, 4).date()))
        self.assertEqual(families[fam.identifier].isDivorced, False)

if __name__ == '__main__':
    unittest.main()