def list_living_married(people):

    living_married = []

    for person in people:

        if person.get_spouse() != "NA" and person.get_death() == "NA":
            living_married.append(person.get_id())

    return living_married
