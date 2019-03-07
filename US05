#US05 Marriage before death
def user_story_05():
    marbeforedeat = True
    print("-------- Testing USER STORY 05. MARRIAGE BEFORE DEATH -------")
    for fam in families:
        wifename = individuals[int(fam.wife[1:]) - 1].name
        hubbyname = individuals[int(fam.husband[1:]) - 1].name
        for ind in individuals:
            personname = ind.name
            if(fam.marriage != None):
                if (personname == wifename or personname == hubbyname):
                    if (ind.death != None):
                        if (ind.death < fam.marriage):
                            print(personname + " has an incorrect marriage and/or death date.")
                            print("Marriage is: " + datetime.strftime(fam.marriage, '%d %b %Y') + " and Death is: " + datetime.strftime(ind.death, '%d %b %Y'))
                            marbeforedeat = False
    if(marbeforedeat == True):
        print("All marriages are before death dates.")
    else:
        print("One or more marriages are not before death dates")
