from datetime import datetime, timedelta

def list_upcoming_birthdays(people):

    upcoming_birthdays = []

    for person in people:

        if person.birth is not None:
            
            birthdate = datetime(datetime.now().year,person.birth.month,person.birth.day)
            days_until_birthday = birthdate - datetime.today()
            
            if birthdate > datetime.today() and days_until_birthday < timedelta(days = 30):
                upcoming_birthdays.append((person.i_id, person.birth))

    return upcoming_birthdays
