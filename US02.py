dates = []
validMarriage = True
def user_story_02():
    print("-------- Testing USER STORY 02. BIRTH BEFORE MARRIAGE -------")
    validMarriage = True
    for fam in families:
        wifename = individuals[int(fam.wife[1:]) - 1].name
        hubbyname = individuals[int(fam.husband[1:]) - 1].name
        for ind in individuals:
            personname = ind.name
            if (fam.marriage != None):
                if (wifename == personname or hubbyname == personname):
                    if (fam.marriage < ind.birth):
                        print(personname + " has an incorrect birth and/or marriage date.")
                        print("Birth is: " + datetime.strftime(ind.birth, '%d %b %Y') + " and Marriage is: " + datetime.strftime(fam.marriage, '%d %b %Y'))
                        validMarriage = False
    if (validMarriage == True):
        print("All birth dates were correct")
    else:
        print("One or more birth/marriage dates were incorrect.")
    return validMarriage
