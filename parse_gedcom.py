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


def get_husband_id(indi):
    return families[int(indi.child_id[1:]) - 1].husband


def get_wife_id(indi):
    return families[int(indi.child_id[1:]) - 1].wife


def get_husband(husband_id):
    return individuals[int(husband_id[1:]) - 1]


def get_wife(wife_id):
    return individuals[int(wife_id[1:]) - 1]


def user_story_09(indi):
    husband_id = get_husband_id(indi)  # get family's husband id
    wife_id = get_wife_id(indi)  # get family's wife id
    husband = get_husband(husband_id)  # get husband
    wife = get_wife(wife_id)  # get wife

    if husband.death is None and wife.death is None:  # if husband and wife are alive
        return True
    elif husband.death is not None and indi.birth < husband.death:  # if husband is dead
        return True
    elif wife.death is not None and indi.birth < wife.death:  # if wife is dead
        return True
    return False


def user_story_11(indi):
    # Find all marriages for an individual
    marriages = []
    for fam in families:
        if indi.i_id == fam.husband or indi.i_id == fam.wife:
            marriages.append(fam)

    # If they are in less than 2 families, there can be no bigotry
    if len(marriages) < 2:
        return False

    for i in range(len(marriages) - 1):
        if marriages[i].divorce is None and marriages[i + 1].divorce is None:  # Neither family is divorced so bigotry
            # TODO account for deaths?
            return True
        elif marriages[i].divorce is None:  # Was Family A created before Family B divorce?
            return datetime.now().date() <= marriages[i + 1].marriage or marriages[i].marriage < marriages[
                i + 1].divorce
        elif marriages[i + 1].divorce is None:  # Was Family B created before Family A divorce?
            return marriages[i + 1].marriage < marriages[i].divorce or datetime.now().date() <= marriages[i].marriage
        else:  # Did both marriages happen after divorces?
            return marriages[i].divorce <= marriages[i + 1].marriage or marriages[i + 1].divorce <= marriages[
                i].marriage


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
        print(
            "\tBirth before either Parent's Death: {}".format(user_story_09(ind) if ind.child_id is not None else "NA"))
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


if __name__ == '__main__':
    main()
