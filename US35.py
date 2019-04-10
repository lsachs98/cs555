from datetime import datetime, timedelta

def list_recent_births(people):

    months = "JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC"

    recent_births = []

    for person in people:

        birthdatestring = person.get_birth()

        if birthdatestring != "":
            birthdate = datetime(int(birthdatestring[7:]),int(months.index(birthdatestring[3:6])/3) + 1,int(birthdatestring[0:3]))

            if birthdate > (datetime.now() - timedelta(days = 365)):
                recent_births.append((person.get_id(), person.get_birth()))

    return recent_births
