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
        self.clidernbdate = datetime.datetime(1,1,1).date()
        self.Marriagebefore14 = False
        self.childbdate = False
    
    def getIsDivorced(self):
        if self.isDivorced:
            return self.divorced
        else:
            return "N/A"
    
    def getChildren(self):
        if self.children == []:
            return "N/A"
        else:
            childStr = "{"
            for child in self.children:
                childStr = childStr + child + ", "
            childStr = childStr[:-2]
            return childStr + "}"