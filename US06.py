#US06 Divorce before Death
def user_story_06():
    divbeforedeat = True
    print("-------- Testing USER STORY 06. DIVORCE BEFORE DEATH -------")
    for fam in families:
        wifename = individuals[int(fam.wife[1:]) - 1].name
        hubbyname = individuals[int(fam.husband[1:]) - 1].name
        for ind in individuals:
            personname = ind.name
            if(fam.divorce != None):
                if (personname == wifename or personname == hubbyname):
                    if(ind.death != None):
                        if (ind.death < fam.divorce):
                            print(personname + " has an incorrect divorce and/or death date.")
                            print("Divorce is: " + datetime.strftime(fam.divorce, '%d %b %Y') + " and Death is: " + datetime.strftime(ind.death, '%d %b %Y'))
                            divbeforedeat = False
    if(divbeforedeat == True):
        print("All divorces are before death dates.")
    else:
        print("One or more divorces are not before death dates")
    return divbeforedeat
