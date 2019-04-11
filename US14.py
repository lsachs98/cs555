def dateat14(dates):
    year = 14+dates.year
    month = dates.month
    day = dates.day
    if(month < 10):
        month = '0' + str(dates.month)
    if (day < 10):
        day = '0' + str(dates.day)
    age = str(year) + '-' + str(month) + '-' + str(day)
    return age
#US10 Marriage after 14 (In my opinion what on earth this should be illegal, you should be over 18)
def user_story_10():
    propermarriage = True
    print("-------- Testing USER STORY 10. MARRIAGE AFTER THE AGE OF 14? -------")
    for fam in families:
        wifename = individuals[int(fam.wife[1:]) - 1].name
        hubbyname = individuals[int(fam.husband[1:]) - 1].name
        for ind in individuals:
            personname = ind.name
            if(personname == wifename or personname == hubbyname):
                #now gotta check their age
                #print("Here in the right name")
                if(dateat14(ind.birth)>str(fam.marriage)):
                    print(ind.name + " got married before the age of 14!")
                    print(ind.name + " got married on: " + datetime.strftime(fam.marriage, '%d %b %Y') + " and their birth date is: " + datetime.strftime(ind.birth, '%d %b %Y'))
                    propermarriage = False
    if(propermarriage == True):
        print("Every person here got married at the right age.")
    else:
        print("Someone got married waaay too early.")
    return process_date
