
import sys

validTags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "MARR", "HUSB", 
             "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

def isTagValid(tag):
    if tag in validTags:
        return "Y"
    else:
        return "N"

def processGedcomFile(file):
    for line in file:
        print("-->" + line, end = '')
        
        splitLine = line.split()
        level = splitLine.pop(0)
        
        if len(splitLine) == 1:
            tag = splitLine[0]
            arguments = ""
        else:
            if splitLine[1] == "INDI" or splitLine[1] == "FAM":
                tag = splitLine.pop(1)
            else:
                tag = splitLine.pop(0)
                
            valid = isTagValid(tag)
            
            arguments = ""
            for word in splitLine:
                arguments = arguments + word + " "
         
        print("<--" + level + "|" + tag + "|" + valid + "|" + arguments)



def main():
    if len(sys.argv) == 2:
        try:
            file = open(sys.argv[1], "r")
            processGedcomFile(file)
        except OSError:
            print("Error opening GEDCOM FILE.")
    else:
        print("Error in number of arguments. Please provide the name of one GEDCOM file.")
    
    
if __name__ == "__main__":
    main()