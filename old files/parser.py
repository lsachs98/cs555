def main(file):
    #main function -- opens file -- prints original
    with open(file) as ged:
        for line in ged:
            print("--> " + line.rstrip())
            strparser(line.rstrip())
            
            
def strparser(line):
    #parses through lines, extracting relevant info and printing edited info
    tagList = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR",
               "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
    irregulars = ["INDI", "FAM"]
    
    lineOld = line.split()
    lineNew = ""
    wordCount = 0
    if lineOld[-1] not in irregulars:
        #deal with regular line format
        for x in lineOld:
            # splits up and adds pipes, only to certain places
            if wordCount == 0:
                #adds in level
                x = x + "|"
                lineNew += x
            elif wordCount == 1:
                #adds in tag and valid/invalid (Y/N)
                if x in tagList:
                    #marks 1 DATE and 2 NAME invald
                    if lineOld[0] == "1" and lineOld[1] == "DATE":
                        x = x + "|N|"
                    elif lineOld[0] == "2" and lineOld[1] == "NAME":
                        x = x + "|N|"
                    #marks 1 DATE and 2 NAME invald
                    else:
                        x = x + "|Y|"
                else:
                    x = x + "|N|"
                lineNew += x
            else:
                #just adds the data in as it was
                x += " "
                lineNew += x
            #keep track of where we are
            wordCount += 1
    else:
        #deal with INDI and FAM line formats
        lineNew += lineOld[0] + "|" + lineOld[2] + "|Y|" + lineOld[1]
    print("<-- " + lineNew)



