from datetime import datetime

def reject_invalid_dates(person):

    return (person.birth == None or date_validity_helper(person.birth)) and (person.death == None or date_validity_helper(person.death))


def date_validity_helper(this_date):

    feb = 28

    if (this_date.year % 4) == 0:
        march = 29

    month_lengths = [31,feb,31,30,31,30,31,31,30,31,30,31]    

    return this_date.day < month_lengths[this_date.month-1]
