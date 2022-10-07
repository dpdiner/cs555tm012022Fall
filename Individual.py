#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime

class individual:

    def __init__(self):
        self.identifier = "N/A"
        self.name = "N/A"
        self.gender = "N/A"
        self.birthday = datetime.datetime(1776, 7, 4).date()
        self.age = 0
        self.alive = True
        self.deathday = datetime.datetime(1776, 7, 4).date()
        self.childFam = []
        self.spouseFam = []
    
    def calculateAge(self):
        
        if self.alive:
            deathday = datetime.date.today()
        else:
            deathday = self.deathday
        self.age = deathday.year - self.birthday.year
        if deathday.month < self.birthday.month:
            self.age -= 1
        elif deathday.month == self.birthday.month:
            if deathday.day < self.birthday.day:
                self.age -= 1
    
    def getDeathday(self):
        if self.alive:
            return "N/A"
        else:
            return str(self.deathday)
            
    def getChildFam(self):
        if self.childFam == []:
            return "N/A"
        else:
            childStr = "{"
            for child in self.childFam:
                childStr = childStr + child + ", "
            childStr = childStr[:-2]
            return childStr + "}"
            
    def getSpouseFam(self):
        if self.spouseFam == []:
            return "N/A"
        else:
            spouseStr = "{"
            for spouse in self.spouseFam:
                spouseStr = spouseStr + spouse + ", "
            spouseStr = spouseStr[:-2]
            return spouseStr + "}"
 


# In[ ]:




