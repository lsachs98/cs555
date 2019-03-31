#US03 Birth before death
def user_story_03():
    bbeforedeath = True
    print("-------- Testing USER STORY 03. BIRTH BEFORE DEATH -------")
    for ind in individuals:
        if(ind.death != None):
            if (ind.death < ind.birth):
                print(ind.name + " has a birth date before his death.")
                print("Birth is: " + datetime.strftime(ind.birth, '%d %b %Y') + " and Death is: " + datetime.strftime(ind.death, '%d %b %Y'))
                bbeforedeath = False
    if(bbeforedeath == True):
        print("All birth and death dates are valid")
    else:
        print("One or more people has a birth date before their death.")
    return bbeforedeath
