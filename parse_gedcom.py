from datetime import datetime

individuals = []
families = []
FILE_NAME = "test0.ged"


class Individual:
    def __init__(self, i_id):
        self.i_id = i_id
        self.name = None
        self.sex = None
        self.spouse_id = None
        self.child_id = None
        self.birth = None
        self.death = None


class Family:
    def __init__(self, f_id):
        self.f_id = f_id
        self.marriage = None
        self.divorce = None
        self.husband = None
        self.wife = None
        self.children = []


def read_file():
    with open(FILE_NAME) as file:
        lines = file.readlines()
    file.close()
    return lines


def process_family(lines, index, new_family):
    details = lines[index].split(" ", 2)
    while details[0] != "0" and index < len(lines):
        if details[0] == "1":
            if details[1] == "HUSB":
                new_family.husband = details[2].rstrip()
            elif details[1] == "WIFE":
                new_family.wife = details[2].rstrip()
            elif details[1] == "CHIL":
                new_family.children.append(details[2].rstrip())
            elif details[1].rstrip() == "MARR" or details[1].rstrip() == "DIV":
                process_date(new_family, lines[index + 1].split(" ", 2), details[1].rstrip())
        index += 1
        details = lines[index].split(" ", 2)
    families.append(new_family)


def process_file(lines):
    index = 0
    while index < len(lines):
        line = lines[index].split(" ", 2)
        if len(line) == 3 and line[0] == "0":
            if line[2].rstrip() == "INDI":
                process_individual(lines, index + 1, Individual(line[1].rstrip()))
            elif line[2].rstrip() == "FAM":
                process_family(lines, index + 1, Family(line[1].rstrip()))
        index += 1
    individuals.sort(key=lambda x: int(x.i_id[1:]))
    families.sort(key=lambda x: int(x.f_id[1:]))


def print_individuals():
    print("--- Individuals ---")
    for ind in individuals:
        print("{}:".format(ind.i_id))
        print("\tName: {}".format(ind.name))
        print("\tSex: {}".format(ind.sex))
        print("\tBirthday: {}".format(format_date(ind.birth)))
        print("\tAlive: {}".format(True if ind.death is None else False))
        print("\tDeath: {}".format(format_date(ind.death) if ind.death is not None else "NA"))
        print("\tChildren: {}".format(ind.child_id))
        print("\tSpouse: {}".format(ind.spouse_id))
    print()


def print_families():
    print("--- Families ---")
    for fam in families:
        print("{}:".format(fam.f_id))
        print("\tMarried: {}".format(format_date(fam.marriage) if fam.marriage is not None else "NA"))
        print("\tDivorced: {}".format(format_date(fam.divorce) if fam.divorce is not None else "NA"))
        print("\tHusband Id: {}".format(fam.husband))
        print("\tHusband Name: {}".format(get_husband(fam.husband).name))
        print("\tWife Id: {}".format(fam.wife))
        print("\tWife Name: {}".format(get_wife(fam.wife).name))
        print("\tChildren: {}".format(", ".join(fam.children)))
    print()


def process_date(obj, line, date_type):
    if line[0] == "2" and line[1] == "DATE":
        if isinstance(obj, Individual):
            if date_type == "BIRT":
                obj.birth = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()
            elif date_type == "DEAT":
                obj.death = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()
        elif isinstance(obj, Family):
            if date_type == "MARR":
                obj.marriage = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()
            elif date_type == "DIV":
                obj.divorce = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()


def process_individual(lines, index, new_individual):
    details = lines[index].split(" ", 2)
    while details[0] != "0" and index < len(lines):
        if details[0] == "1":
            if details[1] == "NAME":
                new_individual.name = details[2].rstrip()
            elif details[1] == "SEX":
                new_individual.sex = details[2].rstrip()
            elif details[1] == "FAMS":
                new_individual.spouse_id = details[2].rstrip()
            elif details[1] == "FAMC":
                new_individual.child_id = details[2].rstrip()
            elif details[1].rstrip() == "BIRT" or details[1].rstrip() == "DEAT":
                process_date(new_individual, lines[index + 1].split(" ", 2), details[1].rstrip())
        index += 1
        details = lines[index].split(" ", 2)
    individuals.append(new_individual)


def format_date(input_date):
    return datetime.strftime(input_date, '%d %b %Y')


def get_husband_id(ind):
    return families[int(ind.child_id[1:]) - 1].husband


def get_wife_id(ind):
    return families[int(ind.child_id[1:]) - 1].wife


def get_individual(ind_id):
    return individuals[int(ind_id[1:]) - 1]


def get_family(fam_id):
    return families[int(fam_id[1:]) - 1]


def get_husband(husband_id):
    return individuals[int(husband_id[1:]) - 1]


def get_wife(wife_id):
    return individuals[int(wife_id[1:]) - 1]


def print_bigamy(ind, marriage_a, marriage_b):
    if ind.sex == "M":
        print("{} committed bigamy with {} and {}".format(ind.name, get_wife(marriage_a.wife).name,
                                                          get_wife(marriage_b.wife).name))
    else:
        print("{} committed bigamy with {} and {}".format(ind.name, get_husband(marriage_a.husband).name,
                                                          get_husband(marriage_b.husband).name))


def check_bigamy_spouse_death(ind, marriage_a, marriage_b, bigamy):
    if ind.sex == "M":  # check if either wife died
        if get_wife(marriage_a.wife).death is not None and get_wife(marriage_a.wife).death >= marriage_b.marriage:
            print_bigamy(ind, marriage_a, marriage_a)
            bigamy = True
        elif get_wife(marriage_b.wife).death is not None and get_wife(marriage_b.wife).death >= marriage_a.marriage:
            print_bigamy(ind, marriage_a, marriage_b)
            bigamy = True
    else:  # check if either husband died
        if get_husband(marriage_a.husband).death is not None and get_husband(
                marriage_a.husband).death >= marriage_b.marriage:
            print_bigamy(ind, marriage_a, marriage_b)
            bigamy = True
        elif get_husband(marriage_b.husband).death is not None and get_husband(
                marriage_b.husband).death >= marriage_a.marriage:
            print_bigamy(ind, marriage_a, marriage_b)
            bigamy = True

    return bigamy


def check_bigamy_divorce_spouse_death(ind, marriage_a, marriage_b, bigamy):
    if ind.sex == "M":  # check if either wife died
        if get_wife(marriage_a.wife).death is None:
            if marriage_b.divorce >= marriage_a.marriage:
                print_bigamy(ind, marriage_a, marriage_a)
                bigamy = True
        else:
            if marriage_b.divorce >= marriage_a.marriage or get_wife(marriage_a.wife).death >= marriage_b.marriage:
                print_bigamy(ind, marriage_a, marriage_b)
                bigamy = True
    else:  # check if either husband died
        if get_husband(marriage_a.husband).death is None:
            if marriage_b.divorce >= marriage_a.marriage:
                print_bigamy(ind, marriage_a, marriage_a)
                bigamy = True
        else:
            if marriage_b.divorce >= marriage_a.marriage or get_husband(
                    marriage_a.husband).death >= marriage_b.marriage:
                print_bigamy(ind, marriage_a, marriage_b)
                bigamy = True

    return bigamy


def check_bigamy_divorce(ind, marriage_a, marriage_b, bigamy):
    if marriage_a.marriage > marriage_b.divorce or marriage_b.marriage <= marriage_a.divorce:
        print_bigamy(ind, marriage_a, marriage_b)
        bigamy = True

    return bigamy


def get_age(ind):
    return datetime.today().date().year - ind.birth.year - ((datetime.today().date().month, datetime.today().date().day)
                                                            < (ind.birth.month, ind.birth.day))


def get_individuals_families(i_id):
    return [fam.f_id for fam in families if i_id in [fam.husband, fam.wife]]


def get_descendants(i_id):
    descendants = []

    for fam_id in get_individuals_families(i_id):
        if get_family(fam_id).children:
            descendants.extend(get_family(fam_id).children)

            for child_id in get_family(fam_id).children:
                descendants.extend(get_descendants(child_id))

    return descendants


def dates_before_today():  # US01: Dates (Birth, Death, Marriage, Divorce) Before Today
    valid_dates = True

    for ind in individuals:
        if ind.birth is not None and ind.birth > datetime.now().date():
            print("{} born before current date, {}.".format(ind.name, format_date(ind.birth)))
            valid_dates = False
        if ind.death is not None and ind.death > datetime.now().date():
            print("{} died before current date, {}.".format(ind.name, format_date(ind.death)))
            valid_dates = False

    for fam in families:
        wife_name = get_wife(fam.wife).name
        hubby_name = get_husband(fam.husband).name

        if fam.marriage is not None and fam.marriage > datetime.now().date():
            print("{} {} married before current date, {}.".format(hubby_name, wife_name, format_date(fam.marriage)))
            valid_dates = False

        if fam.divorce is not None and fam.divorce > datetime.now().date():
            print("{} {} divorced before current date, {}.".format(hubby_name, wife_name, format_date(fam.divorce)))
            valid_dates = False

    if valid_dates:
        print("All dates are valid in this GEDCOM file.")
    else:
        print("Not all dates are valid in this GEDCOM file.")


def birth_before_marriage():  # US02: Birth Before Marriage
    valid_marriage = True

    for fam in families:
        wife_name = get_wife(fam.wife).name
        hubby_name = get_husband(fam.husband).name

        for ind in individuals:
            if fam.marriage is not None:
                if wife_name == ind.name or hubby_name == ind.name and fam.marriage < ind.birth:
                    print("{} has an incorrect birth and/or marriage date.".format(ind.name))
                    print("Birth is: {} and Marriage is: {}".format(format_date(ind.birth), format_date(fam.marriage)))
                    valid_marriage = False

    if valid_marriage:
        print("All birth dates were correct")
    else:
        print("One or more birth/marriage dates were incorrect.")


def marriage_before_divorce():  # US04: Marriage before divorce
    marbeforediv = True
    for fam in families:
        if fam.divorce is not None and fam.marriage is not None:
            if fam.divorce < fam.marriage:
                print("{} and {} have a marriage before their divorce".format(get_individual(fam.husband),
                                                                              get_individual(fam.wife)))
                print("Marriage is: {} and divorce is: {}".format(format_date(fam.marriage), format_date(fam.divorce)))
                marbeforediv = False

    if marbeforediv:
        print("All marriage and divorce dates are true.")
    else:
        print("One or more marriage/divorce dates are incorrect.")


def marriage_before_death():  # US05: Marriage before death
    marbeforedeat = True
    for fam in families:
        for ind in individuals:
            if fam.marriage is not None:
                if ind.name == get_wife(fam.wife).name or ind.name == get_husband(fam.husband).name:
                    if ind.death is not None:
                        if ind.death < fam.marriage:
                            print("{} has an incorrect marriage and/or death date.".format(ind.name))
                            print("Marriage is: {} and Death is: {}".format(format_date(fam.marriage),
                                                                            format_date(ind.death)))
                            marbeforedeat = False

    if marbeforedeat:
        print("All marriages are before death dates.")
    else:
        print("One or more marriages are not before death dates")


def birth_before_parents_death():  # US09: Birth Before Death of Parents
    valid_birth = True

    for ind in individuals:
        if ind.child_id is None:
            continue

        husband = get_husband(get_husband_id(ind))  # get husband
        wife = get_wife(get_wife_id(ind))  # get wife

        if husband.death is None and wife.death is None:  # if husband and wife are alive
            continue
        elif husband.death is not None and wife.death is not None:  # if husband and wife are both dead
            if ind.birth < husband.death and ind.birth < wife.death:
                continue
            else:
                valid_birth = False
                print("{} was born after death of parent(s).".format(ind.name))
        elif husband.death is not None and ind.birth < husband.death:  # if husband is dead
            continue
        elif wife.death is not None and ind.birth < wife.death:  # if wife is dead
            continue
        else:
            valid_birth = False
            print("{} was born after death of parent(s).".format(ind.name))

    if valid_birth:
        print("All birth dates were before parents' deaths.")
    else:
        print("One or more birth dates were incorrect.")


def no_bigamy():  # US11: No Bigamy
    bigamy = False

    for ind in individuals:
        # Find all marriages for an individual
        marriages = []
        for fam in families:
            if ind.i_id == fam.husband or ind.i_id == fam.wife:
                marriages.append(fam)

        # If they are in less than 2 families, there can be no bigotry
        if len(marriages) < 2:
            continue

        for i in range(len(marriages)):
            for j in range(i + 1, len(marriages)):
                if marriages[i].divorce is None and marriages[j].divorce is None:  # Neither family are divorced
                    bigamy = check_bigamy_spouse_death(ind, marriages[i], marriages[j], bigamy)
                elif marriages[i].divorce is None:  # Was Family A created before Family B divorce/death?
                    bigamy = check_bigamy_divorce_spouse_death(ind, marriages[i], marriages[j], bigamy)
                elif marriages[j].divorce is None:  # Was Family B created before Family A divorce/death?
                    bigamy = check_bigamy_divorce_spouse_death(ind, marriages[j], marriages[i], bigamy)
                else:  # Both families are divorced
                    bigamy = check_bigamy_divorce(ind, marriages[i], marriages[j], bigamy)

    if bigamy:
        print("There are bigamy cases in this GEDCOM file.")
    else:
        print("There are no bigamy cases in this GEDCOM file.")


def parents_not_too_old():  # US12: Parents Not Too Old
    too_old = False

    for fam in families:
        if fam.children:
            mom = get_individual(fam.wife)
            dad = get_individual(fam.husband)
            for child_id in fam.children:
                child = get_individual(child_id)
                if abs(get_age(mom) - get_age(child)) > 60 and abs(get_age(dad) - get_age(child)) > 80:
                    print("{}'s parents, {} and {}, are too old.".format(child.name, mom.name, dad.name))
                    too_old = True
                elif abs(get_age(mom) - get_age(child)) > 60:
                    print("{}'s mother, {}, is too old.".format(child.name, mom.name))
                    too_old = True
                elif abs(get_age(dad) - get_age(child)) > 80:
                    print("{}'s father, {}, is too old.".format(child.name, dad.name))
                    too_old = True

    if too_old:
        print("Some parents are too old in this GEDCOM file.")
    else:
        print("All parents are not too old in this GEDCOM file.")


def sibling_age_space():  # US13: Sibling Age Spacing
    sibling_space = True
    for fam in families:
        if fam.children and len(fam.children) > 1:
            for i in range(len(fam.children)):
                for j in range(i + 1, len(fam.children)):
                    if 2 < abs((get_individual(fam.children[i]).birth - get_individual(fam.children[j]).birth).days) < \
                            243.3:
                        print("{} and {} are not spaced properly.".format(get_individual(fam.children[i]).name,
                                                                          get_individual(fam.children[j]).name))
                        sibling_space = False

    if sibling_space:
        print("All sibling ages are spaced properly.")
    else:
        print("Some sibling ages are not spaced properly.")


def no_marriage_to_descendants():  # US17: No Marriage to Descendants
    descendant_marriage = False

    for ind in individuals:
        descendants = get_descendants(ind.i_id)
        if descendants:
            for fam_id in get_individuals_families(ind.i_id):
                if any(s_id in descendants for s_id in [get_family(fam_id).husband, get_family(fam_id).wife]):
                    descendant_marriage = True

    if descendant_marriage:
        print("Some ancestors are married to descendants.")
    else:
        print("No ancestors are married to descendants.")


def siblings_should_not_marry():  # US18: Siblings Should Not Marry
    sibling_marriage = False

    for fam in families:
        if fam.children and len(fam.children) > 1:
            for i in range(len(fam.children)):
                for j in range(i + 1, len(fam.children)):
                    if any(fam.children[i] in [f.husband, f.wife] and fam.children[j] in [f.husband, f.wife] for f in families):
                        sibling_marriage = True
                        print("{} and {} are married siblings.".format(get_individual(fam.children[i]).name,
                                                                          get_individual(fam.children[j]).name))

    if sibling_marriage:
        print("Some siblings are married.")
    else:
        print("All siblings are not married.")


def order_children_by_age():  # US28: Order Siblings By Age
    for fam in families:
        if fam.children:
            fam.children.sort(key=lambda child: get_individual(child).birth)


def list_deceased():  # US29: List Deceased
    return [ind for ind in individuals if ind.death is not None]


def list_living_married():  # US30: List Living Married
    living_married = []

    for person in individuals:
        if person.spouse_id is not None and person.death is None:
            living_married.append(person)

    return living_married


def list_living_single():  # US31: List Living Single
    living_single = []

    for person in individuals:

        if person.spouse_id is not None and person.death is None:
            living_single.append(person)

    return living_single


def main():
    process_file(read_file())
    print_individuals()
    print_families()
    dates_before_today()  # US01
    birth_before_marriage()  # US02
    marriage_before_divorce()  # US04
    marriage_before_death()  # US05
    birth_before_parents_death()  # US09
    no_bigamy()  # US11
    parents_not_too_old()  # US12
    sibling_age_space()  # US13
    no_marriage_to_descendants()  # US17
    siblings_should_not_marry()  # US18
    order_children_by_age()  # US28
    print("Deceased:")  # US29
    for deceased in list_deceased():
        print(deceased.name)
    print("Living Married:")  # US30
    for living in list_living_married():
        print(living.name)
    print("Living Single:")  # US31
    for living in list_living_single():
        print(living.name)


if __name__ == '__main__':
    main()
