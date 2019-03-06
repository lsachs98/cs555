import datetime
temp = []
stringgs = ''
def monthsplit(date):
    for temp in date:
        temp = date.split()
        if(temp[1] == 'JAN'): 
            temp[1] = '01'
        elif(temp[1] == 'FEB'): 
            temp[1] = '02'
        elif(temp[1] == 'MAR'): 
            temp[1] = '03'
        elif(temp[1] == 'APR'): 
            temp[1] = '04'
        elif(temp[1] == 'MAY'): 
            temp[1] = '05'
        elif(temp[1] == 'JUN'): 
            temp[1] = '06'
        elif(temp[1] == 'JUL'): 
            temp[1] = '07'
        elif(temp[1] == 'AUG'): 
            temp[1] = '08'
        elif(temp[1] == 'SEP'): 
            temp[1] = '09'
        elif(temp[1] == 'OCT'): 
            temp[1] = '10'
        elif(temp[1] == 'NOV'): 
            temp[1] = '11'
        elif(temp[1] == 'DEC'): 
            temp[1] = '12'
        if(temp[0] == '1' or temp[0] == '2' or temp[0] == '3' or temp[0] == '4' or temp[0] == '5' or temp[0] == '6' or temp[0] == '7' or temp[0] == '8' or temp[0] == '9'):
          temp[0] = '0' + temp[0]
        stringgs = str(temp[2]) + str(temp[1]) + str(temp[0])
        return stringgs

#US02, birth before marriage
dates = []
validMarriage = True
def birthBeforeMarriage(indList, famData):
    individuals.sort(key=lambda x: int(x.i_id[1:]))
    families.sort(key=lambda x: int(x.f_id[1:]))
    validMarriage = True
    for fam in famData:
        wifename = individuals[int(fam.get_wife()[1:]) - 1].get_name()
        hubbyname = individuals[int(fam.get_husband()[1:]) - 1].get_name()
        m = monthsplit(fam.get_marriage())
        for ind in indList:
            personname = ind.get_name()
            b = monthsplit(ind.get_birth())
            if (m != None):
                if(wifename == personname or hubbyname == personname):
                    if (m < b):
                        print("---HOUSTON WE HAVE A PROBLEM---")
                        print(personname)
                        print("Birth is: " + ind.get_birth() + " and Marriage is: " + fam.get_marriage())
                        validMarriage = False
    if(validMarriage == True): print("All birth dates were correct")
    else: print("One or more birth/marriage dates were incorrect.")
    return validMarriage
