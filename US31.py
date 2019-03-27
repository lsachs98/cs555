def list_living_single(people):

    living_single = []

    for person in people:

        if person.get_spouse() == "NA" and person.get_death() == "NA":
            living_single.append(person.get_id())

    return living_single
