#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime

class family:

    def __init__(self):
        self.identifier = "N/A"
        self.married = datetime.datetime(1776, 7, 4).date()
        self.divorced = datetime.datetime(1776, 7, 4).date()
        self.isDivorced = False
        self.husbandId = "N/A"
        self.husbandName = "N/A"
        self.wifeId = "N/A"
        self.wifeName = "N/A"
        self.children = []
        self.Marriagebefordivorce = False
        self.Marriagebedoredeath = False
        self.wdday = datetime.datetime(1776, 7, 4).date()
        self.Hdday = datetime.datetime(1776, 7, 4).date()
    
    def getIsDivorced(self):
        if self.isDivorced:
            return "N/A"
        else:
            return self.divorced
    
    def getChildren(self):
        if self.children == []:
            return "N/A"
        else:
            childStr = "{"
            for child in self.children:
                childStr = childStr + child + ", "
            childStr = childStr[:-2]
            return childStr + "}"
       


# In[ ]:




