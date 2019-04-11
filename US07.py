def aging(dates): #The date if it were 150 years later
    year = 150+dates.year
    month = dates.month
    day = dates.day
    if(month < 10):
        month = '0' + str(dates.month)
    if (day < 10):
        day = '0' + str(dates.day)
    old = str(year) + '-' + str(month) + '-' + str(day)
    return old
#US07 Less than 150 years old(Ok who in the world has even made it past 120 years ok)
def user_story_07():
    rightage = True
    print("-------- Testing USER STORY 07. LESS THAN 150 YEARS OLD? -------")
    for ind in individuals:
        if(ind.death == None):
            if(aging(ind.birth)<str(datetime.now().date())):
                print(ind.name + " is over 150 years old! Whaat")
                print("Birthday is: " + datetime.strftime(ind.birth, '%d %b %Y'))
                rightage = False
    if(rightage == True):
        print("Every person is within the right age.")
    else:
        print("One or more individuals are not the right age here.")
    return rightage
