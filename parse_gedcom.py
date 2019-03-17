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


def get_husband_id(ind):
    return families[int(ind.child_id[1:]) - 1].husband


def get_wife_id(ind):
    return families[int(ind.child_id[1:]) - 1].wife


def get_husband(husband_id):
    return individuals[int(husband_id[1:]) - 1]


def get_wife(wife_id):
    return individuals[int(wife_id[1:]) - 1]


def dates_before_today():  # US01: Dates (Birth, Death, Marriage, Divorce) Before Today
    valid_dates = True

    for ind in individuals:
        if ind.birth is not None and ind.birth > datetime.now().date():
            print(ind.name + " born before current date. " + datetime.strftime(ind.birth, '%d %b %Y'))
            valid_dates = False
        if ind.death is not None and ind.death > datetime.now().date():
            print(ind.get_name() + " died before current date." + datetime.strftime(ind.death, '%d %b %Y'))
            valid_dates = False

    for fam in families:
        wife_name = get_wife(fam.wife).name
        hubby_name = get_husband(fam.husband).name

        if fam.marriage is not None and fam.marriage > datetime.now().date():
            print("%s %s married before current date, %s." % hubby_name, wife_name, datetime.strftime(fam.marriage,
                                                                                                      '%d %b %Y'))
            valid_dates = False

        if fam.divorce is not None and fam.divorce > datetime.now().date():
            print("%s %s divorced before current date." % hubby_name, wife_name, datetime.strftime(fam.divorce,
                                                                                                   '%d %b %Y'))
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
                    print("%s has an incorrect birth and/or marriage date." % ind.name)
                    print("Birth is: %s and Marriage is: %s" % (
                        datetime.strftime(ind.birth, '%d %b %Y'), datetime.strftime(fam.marriage, '%d %b %Y')))
                    valid_marriage = False

    if valid_marriage:
        print("All birth dates were correct")
    else:
        print("One or more birth/marriage dates were incorrect.")


def birth_before_parents_death():  # US09: Birth Before Death of Parents
    valid_birth = True

    for ind in individuals:
        husband_id = get_husband_id(ind)  # get family's husband id
        wife_id = get_wife_id(ind)  # get family's wife id
        husband = get_husband(husband_id)  # get husband
        wife = get_wife(wife_id)  # get wife

        if husband.death is None and wife.death is None:  # if husband and wife are alive
            continue
        elif husband.death is not None and wife.death is not None:  # if husband and wife are both dead
            if ind.birth < husband.death and ind.birth < wife.death:
                continue
        elif husband.death is not None and ind.birth < husband.death:  # if husband is dead
            continue
        elif wife.death is not None and ind.birth < wife.death:  # if wife is dead
            continue
        else:
            valid_birth = False
            print("%s was born after death of parent(s)." % ind.name)

    if valid_birth:
        print("All birth dates were before parents' deaths")
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

        for i in range(len(marriages) - 1):
            for j in range(i + 1, len(marriages)):
                if marriages[i].divorce is None and marriages[j].divorce is None:  # Neither family is divorced
                    if ind.sex == "M":  # check if either wife died
                        if get_wife(marriages[i].wife).death is not None and get_wife(marriages[i].wife).death >= \
                                marriages[j].marriage:
                            print("%s committed bigamy with %s and %s" % (
                                ind.name, get_wife(marriages[i].wife).name, get_wife(marriages[j].wife).name))
                            bigamy = True
                        elif get_wife(marriages[j].wife).death is not None and get_wife(marriages[j].wife).death >= \
                                marriages[i].marriage:
                            print("%s committed bigamy with %s and %s" % (
                                ind.name, get_wife(marriages[i].wife).name, get_wife(marriages[j].wife).name))
                            bigamy = True
                    else:  # check if either husband died
                        if get_husband(marriages[i].husband).death is not None and get_husband(
                                marriages[i].husband).death >= marriages[j].marriage:
                            print("%s committed bigamy with %s and %s" % (
                                ind.name, get_husband(marriages[i].husband).name,
                                get_husband(marriages[j].husband).name))
                            bigamy = True
                        elif get_husband(marriages[j].husband).death is not None and get_husband(
                                marriages[j].husband).death >= marriages[i].marriage:
                            print("%s committed bigamy with %s and %s" % (
                                ind.name, get_husband(marriages[i].husband).name,
                                get_husband(marriages[j].husband).name))
                            bigamy = True
                elif marriages[i].divorce is not None and marriages[j].divorce is not None:  # Both families are divorced

                elif marriages[i].divorce is None:  # Was Family A created before Family B divorce/death?
                    if ind.sex == "M":
                        if get_wife(marriages[i].wife).death is not None:
                            if get_wife(marriages[i].wife).death >= marriages[j].marriage or marriages[i].marriage < \
                               marriages[j].divorce:
                                print("%s committed bigamy with %s and %s" % (
                                ind.name, get_wife(marriages[i].wife).name, get_wife(marriages[j].wife).name))
                            bigamy = True
                    else:
                        if get_husband(marriages[i].husband).death is not None:
                            if get_husband(marriages[i].husband).death <= marriages[j].marriage or marriages[
                            i].marriage < \
                               marriages[j].divorce
                    else:
                        return datetime.now().date() <= marriages[j].marriage or marriages[i].marriage < marriages[
                            j].divorce
                elif marriages[j].divorce is None:  # Was Family B created before Family A divorce?
                    if ind.sex == "M" and get_wife(marriages[j].wife).death is not None:
                        return get_wife(marriages[j].wife).death <= marriages[i].marriage or marriages[j].marriage < \
                               marriages[i].divorce
                    elif ind.sex == "F" and get_husband(marriages[j].husband).death is not None:
                        return get_husband(marriages[j].husband).death <= marriages[i].marriage or marriages[
                            j].marriage < marriages[i].divorce
                    else:
                        return marriages[j].marriage < marriages[i].divorce or datetime.now().date() <= marriages[
                            i].marriage
                else:  # Did both marriages happen after divorces?
                    return marriages[i].divorce <= marriages[j].marriage or marriages[j].divorce <= marriages[
                        i].marriage

    if bigamy:
        print("There are bigamy cases in this GEDCOM file.")
    else:
        print("There are no bigamy cases in this GEDCOM file.")


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
        print("\tBirthday: {}".format(datetime.strftime(ind.birth, '%d %b %Y')))
        print("\tAlive: {}".format(True if ind.death is None else False))
        print("\tDeath: {}".format(datetime.strftime(ind.death, '%d %b %Y') if ind.death is not None else "NA"))
        print("\tChildren: {}".format(ind.child_id))
        print("\tSpouse: {}".format(ind.spouse_id))
    print()


def print_families():
    print("--- Families ---")
    for fam in families:
        print("{}:".format(fam.f_id))
        print("\tMarried: {}".format(datetime.strftime(fam.marriage, '%d %b %Y') if fam.marriage is not None else "NA"))
        print("\tDivorced: {}".format(datetime.strftime(fam.divorce, '%d %b %Y') if fam.divorce is not None else "NA"))
        print("\tHusband Id: {}".format(fam.husband))
        print("\tHusband Name: {}".format(individuals[int(fam.husband[1:]) - 1].name))
        print("\tWife Id: {}".format(fam.wife))
        print("\tWife Name: {}".format(individuals[int(fam.wife[1:]) - 1].name))
        print("\tChildren: {}".format(", ".join(fam.children)))
    print()


def main():
    process_file(read_file())
    print_individuals()
    print_families()
    dates_before_today()
    birth_before_marriage()
    birth_before_parents_death()
    no_bigamy()


if __name__ == '__main__':
    main()
