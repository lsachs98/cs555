# US01, dates before today
def user_story_01():  # Dates: birth, death, marriage, divorce
    print("-------- Testing USER STORY 01. DATES BEFORE TODAY -------")
    validDates = True
    for ind in individuals:
        if ind.birth is not None and ind.birth > datetime.now().date():
            print(ind.name + " born before current date. " + datetime.strftime(ind.birth, '%d %b %Y'))
            validDates = False
        if ind.death is not None and ind.death > datetime.now().date():
            print(ind.name() + " died before current date." + datetime.strftime(ind.death, '%d %b %Y'))
            validDates = False
    for fam in families:
        wifename = individuals[int(fam.wife[1:]) - 1].name
        hubbyname = individuals[int(fam.husband[1:]) - 1].name
        if fam.marriage is not None and fam.marriage > datetime.now().date():
            print(hubbyname + " " + wifename + " married before current date." + datetime.strftime(fam.marriage, '%d %b %Y'))
            validDates = False
        if fam.divorce is not None and fam.divorce > datetime.now().date():
            print(hubbyname + " " + wifename + " divorced before current date." + datetime.strftime(fam.divorce, '%d %b %Y'))
            validDates = False
    if validDates:
        print("All dates are valid in this GEDCOM file.")
    else:
        print("Not all dates are valid in this GEDCOM file.")
