from datetime import datetime, timedelta

def list_recent_deaths(people):

    months = "JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC"

    recent_deaths = []

    for person in people:

        deathdatestring = person.get_death()

        if deathdatestring != "NA":
            deathdate = datetime(int(deathdatestring[7:]),int(months.index(deathdatestring[3:5])/3)+1,int(deathdatestring[0:2]))

            if deathdate > (datetime.now() - timedelta(days = 365)):
                recent_deaths.append((person.get_id(), person.get_death()))

    return recent_deaths
