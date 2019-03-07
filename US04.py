
#US04 Marriage before divorce
def user_story_04():
    marbeforediv = True
    print("-------- Testing USER STORY 04. MARRIAGE BEFORE DIVORCE -------")
    for fam in families:
        if (fam.divorce != None and fam.marriage != None):
            if (fam.divorce < fam.marriage):
                print(fam.husband + " and " + fam.wife + " have a marriage before their divorce")
                print("Marriage is: " + datetime.strftime(fam.marriage, '%d %b %Y') + " and divorce is: " + datetime.strftime(fam.divorce, '%d %b %Y'))
                marbeforediv = False
    if(marbeforediv == True):
        print("All marriage and divorce dates are true.")
    else:
        print("One or more marriage/divorce dates are incorrect.")
