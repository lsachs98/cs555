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
            elif details[1].rstrip() == "BIRT":
                index = index + 1
                details = lines[index].split(" ", 2)
                if details[0] == "2" and details[1] == "DATE":
                    new_individual.birth = details[2].rstrip()
            elif details[1].rstrip() == "DEAT":
                index = index + 1
                details = lines[index].split(" ", 2)
                if details[0] == "2" and details[1] == "DATE":
                    new_individual.death = details[2].rstrip()
        index = index + 1
        details = lines[index].split(" ", 2)
    individuals.append(new_individual)


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
            elif details[1].rstrip() == "MARR":
                index = index + 1
                details = lines[index].split(" ", 2)
                if details[0] == "2" and details[1] == "DATE":
                    new_family.marriage = details[2].rstrip()
            elif details[1].rstrip() == "DIV":
                index = index + 1
                details = lines[index].split(" ", 2)
                if details[0] == "2" and details[1] == "DATE":
                    new_family.divorce = details[2].rstrip()
        index = index + 1
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

        index = index + 1


def print_individuals():
    individuals.sort(key=lambda x: int(x.i_id[1:]))
    print("--- Individuals ---")
    for ind in individuals:
        print("{}:".format(ind.i_id))
        print("\tName: {}".format(ind.name))
        print("\tSex: {}".format(ind.sex))
        print("\tBirthday: {}".format(ind.birth))
        print("\tAlive: {}".format(True if ind.death is None else False))
        print("\tDeath: {}".format(ind.death))
        print("\tChildren: {}".format(ind.child_id))
        print("\tSpouse: {}".format(ind.spouse_id))
    print()


def print_families():
    families.sort(key=lambda x: int(x.f_id[1:]))
    print("--- Families ---")
    for fam in families:
        print("{}:".format(fam.f_id))
        print("\tMarried: {}".format(fam.marriage))
        print("\tDivorced: {}".format(fam.divorce))
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
