from datetime import datetime, timedelta
from tabulate import tabulate

individuals = []
families = []
FILE_NAME = "test.ged"


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
                new_individual.name = details[2].strip().replace("/", "")
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


def print_individuals():
    headers = ["Id", "Name", "Sex", "Birthday", "Alive", "Death", "Child Id", "Spouse Id"]
    table = []
    for ind in individuals:
        table.append([ind.i_id, ind.name, ind.sex, format_date(ind.birth), True if ind.death is None else False,
                      format_date(ind.death) if ind.death is not None else "NA", ind.child_id, ind.spouse_id])
    return tabulate(table, headers, tablefmt="fancy_grid")


def print_families():
    headers = ["Id", "Married", "Divorced", "Husband Id", "Husband Name", "Wife Id", "Wife Name", "Children Ids"]
    table = []
    for fam in families:
        table.append([fam.f_id, format_date(fam.marriage) if fam.marriage is not None else "NA",
                      format_date(fam.divorce) if fam.divorce is not None else "NA", fam.husband,
                      get_individual(fam.husband).name, fam.wife, get_individual(fam.wife).name,
                      ", ".join(fam.children)])
    return tabulate(table, headers, tablefmt="fancy_grid")


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


def print_bigamy(ind, marriage_a, marriage_b, notes):
    if ind.sex == "M":
        notes.append("{} committed bigamy with {} and {}".format(ind.name, get_individual(marriage_a.wife).name,
                                                                 get_individual(marriage_b.wife).name))
    else:
        notes.append("{} committed bigamy with {} and {}".format(ind.name, get_individual(marriage_a.husband).name,
                                                                 get_individual(marriage_b.husband).name))


def check_bigamy_spouse_death(ind, marriage_a, marriage_b, bigamy, notes):
    if ind.sex == "M":  # check if either wife died
        if get_individual(marriage_a.wife).death is not None and get_individual(
                marriage_a.wife).death >= marriage_b.marriage:
            print_bigamy(ind, marriage_a, marriage_a, notes)
            bigamy = True
        elif get_individual(marriage_b.wife).death is not None and get_individual(
                marriage_b.wife).death >= marriage_a.marriage:
            print_bigamy(ind, marriage_a, marriage_b, notes)
            bigamy = True
    else:  # check if either husband died
        if get_individual(marriage_a.husband).death is not None and get_individual(
                marriage_a.husband).death >= marriage_b.marriage:
            print_bigamy(ind, marriage_a, marriage_b, notes)
            bigamy = True
        elif get_individual(marriage_b.husband).death is not None and get_individual(
                marriage_b.husband).death >= marriage_a.marriage:
            print_bigamy(ind, marriage_a, marriage_b, notes)
            bigamy = True

    return bigamy


def check_bigamy_divorce_spouse_death(ind, marriage_a, marriage_b, bigamy, notes):
    if ind.sex == "M":  # check if either wife died
        if get_individual(marriage_a.wife).death is None:
            if marriage_b.divorce >= marriage_a.marriage:
                print_bigamy(ind, marriage_a, marriage_a, notes)
                bigamy = True
        else:
            if marriage_b.divorce >= marriage_a.marriage or get_individual(
                    marriage_a.wife).death >= marriage_b.marriage:
                print_bigamy(ind, marriage_a, marriage_b, notes)
                bigamy = True
    else:  # check if either husband died
        if get_individual(marriage_a.husband).death is None:
            if marriage_b.divorce >= marriage_a.marriage:
                print_bigamy(ind, marriage_a, marriage_a, notes)
                bigamy = True
        else:
            if marriage_b.divorce >= marriage_a.marriage or get_individual(
                    marriage_a.husband).death >= marriage_b.marriage:
                print_bigamy(ind, marriage_a, marriage_b, notes)
                bigamy = True

    return bigamy


def check_bigamy_divorce(ind, marriage_a, marriage_b, bigamy, notes):
    if marriage_a.marriage > marriage_b.divorce or marriage_b.marriage <= marriage_a.divorce:
        print_bigamy(ind, marriage_a, marriage_b, notes)
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


def dates_before_today(table):  # US01: Dates (Birth, Death, Marriage, Divorce) Before Today
    valid_dates = True
    notes = []
    for ind in individuals:
        if ind.birth is not None and ind.birth > datetime.now().date():
            notes.append("{} born before current date, {}.".format(ind.name, format_date(ind.birth)))
            valid_dates = False
        if ind.death is not None and ind.death > datetime.now().date():
            notes.append("{} died before current date, {}.".format(ind.name, format_date(ind.death)))
            valid_dates = False

    for fam in families:
        wife_name = get_individual(fam.wife).name
        hubby_name = get_individual(fam.husband).name

        if fam.marriage is not None and fam.marriage > datetime.now().date():
            notes.append(
                "{} {} married before current date, {}.".format(hubby_name, wife_name, format_date(fam.marriage)))
            valid_dates = False

        if fam.divorce is not None and fam.divorce > datetime.now().date():
            notes.append(
                "{} {} divorced before current date, {}.".format(hubby_name, wife_name, format_date(fam.divorce)))
            valid_dates = False

    if valid_dates:
        result = "All dates are valid in this GEDCOM file."
    else:
        result = "Not all dates are valid in this GEDCOM file."

    table.append(
        ["US01", "Dates (Birth, Death, Marriage, Divorce) Before Today", "\n".join(notes), valid_dates, result])


def birth_before_marriage(table):  # US02: Birth Before Marriage
    valid_marriage = True
    notes = []

    for fam in families:
        wife_name = get_individual(fam.wife).name
        hubby_name = get_individual(fam.husband).name

        for ind in individuals:
            if fam.marriage is not None:
                if wife_name == ind.name or hubby_name == ind.name and fam.marriage < ind.birth:
                    notes.append("{} has an incorrect birth and/or marriage date.".format(ind.name))
                    notes.append(
                        "Birth is: {} and Marriage is: {}".format(format_date(ind.birth), format_date(fam.marriage)))
                    valid_marriage = False

    if valid_marriage:
        result = "All birth dates were correct"
    else:
        result = "One or more birth/marriage dates were incorrect."

    table.append(
        ["US02", "Birth Before Marriage", "\n".join(notes), valid_marriage, result])


def birth_before_death(table):  # US03: Birth Before Death
    born_before_death = True
    notes = []
    for ind in individuals:
        if ind.death is not None and ind.death < ind.birth:
            notes.append("{} has a birth date after their death.".format(ind.name))
            notes.append("Birth is: {} and Death is: {}".format(format_date(ind.birth), format_date(ind.death)))
            born_before_death = False

    if born_before_death:
        result = "All birth and death dates are valid."
    else:
        result = "One or more people has a birth date before their death."

    table.append(
        ["US03", "Birth Before Death", "\n".join(notes), born_before_death, result])


def marriage_before_divorce(table):  # US04: Marriage Before Divorce
    marry_before_divorce = True
    notes = []
    for fam in families:
        if fam.divorce is not None and fam.marriage is not None:
            if fam.divorce < fam.marriage:
                notes.append("{} and {} have a marriage before their divorce".format(get_individual(fam.husband),
                                                                                     get_individual(fam.wife)))
                notes.append(
                    "Marriage is: {} and divorce is: {}".format(format_date(fam.marriage), format_date(fam.divorce)))
                marry_before_divorce = False

    if marry_before_divorce:
        result = "All marriage and divorce dates are correct."
    else:
        result = "One or more marriage/divorce dates are incorrect."

    table.append(
        ["US04", "Marriage Before Divorce", "\n".join(notes), marry_before_divorce, result])


def marriage_before_death(table):  # US05: Marriage Before Death
    marry_before_dead = True
    notes = []
    for fam in families:
        for ind in individuals:
            if fam.marriage is not None:
                if ind.name == get_individual(fam.wife).name or ind.name == get_individual(fam.husband).name:
                    if ind.death is not None:
                        if ind.death < fam.marriage:
                            notes.append("{} has an incorrect marriage and/or death date.".format(ind.name))
                            notes.append("Marriage is: {} and Death is: {}".format(format_date(fam.marriage),
                                                                                   format_date(ind.death)))
                            marry_before_dead = False

    if marry_before_dead:
        result = "All marriages are before death dates."
    else:
        result = "One or more marriages are not before death dates"

    table.append(
        ["US05", "Marriage Before Death", "\n".join(notes), marry_before_dead, result])


def divorce_before_death(table):  # US06: Divorce Before Death
    divorce_before_dead = True
    notes = []
    for fam in families:
        wife_name = get_individual(fam.wife).name
        hubby_name = get_individual(fam.husband).name

        for ind in individuals:
            if fam.divorce is not None:
                if ind.name == wife_name or ind.name == hubby_name:
                    if ind.death is not None and ind.death < fam.divorce:
                        notes.append("{} has an incorrect divorce and/or death date.".format(ind.name))
                        notes.append(
                            "Divorce is: {} and Death is: {}".format(format_date(fam.divorce), format_date(ind.death)))
                        divorce_before_dead = False
    if divorce_before_dead:
        result = "All divorces are before death dates."
    else:
        result = "One or more divorces are not before death dates"

    table.append(
        ["US06", "Divorce Before Death", "\n".join(notes), divorce_before_dead, result])


def less_than_150_years_old(table):  # US07: Less Than 150 Years Old
    right_age = True
    notes = []
    for ind in individuals:
        if ind.death is None:
            diff = datetime.now().date() - ind.birth
            if (diff.days / 365.24) > 150:
                notes.append(
                    "{} is over 150 years old! Whaat?! Birthday is {}.".format(ind.name, format_date(ind.birth)))
                right_age = False
        else:
            diff = ind.death - ind.birth
            if (diff.days / 365.24) > 150:
                notes.append(
                    "{} was over 150 years old! Whaat?! Birthday is {} and Death is {}.".format(ind.name, format_date(
                        ind.birth), format_date(ind.death)))
                right_age = False

    if right_age:
        result = "Every person is within the right age range."
    else:
        result = "One or more individuals are not within the right age range."

    table.append(
        ["US07", "Less Than 150 Years Old", "\n".join(notes), right_age, result])


def birth_before_parents_death(table):  # US09: Birth Before Death of Parents
    valid_birth = True
    notes = []
    for ind in individuals:
        if ind.child_id is None:
            continue

        husband = get_individual(get_husband_id(ind))  # get husband
        wife = get_individual(get_wife_id(ind))  # get wife

        if husband.death is None and wife.death is None:  # if husband and wife are alive
            continue
        elif husband.death is not None and wife.death is not None:  # if husband and wife are both dead
            if ind.birth < husband.death and ind.birth < wife.death:
                continue
            else:
                valid_birth = False
                notes.append("{} was born after death of parent(s).".format(ind.name))
        elif husband.death is not None and ind.birth < husband.death:  # if husband is dead
            continue
        elif wife.death is not None and ind.birth < wife.death:  # if wife is dead
            continue
        else:
            valid_birth = False
            notes.append("{} was born after death of parent(s).".format(ind.name))

    if valid_birth:
        result = "All birth dates were before parents' deaths."
    else:
        result = "One or more birth dates were incorrect."

    table.append(
        ["US09", "Birth Before Death of Parents", "\n".join(notes), valid_birth, result])


def marriage_after_fourteen(table):  # US10: Marriage After 14
    proper_marriage = True
    notes = []
    for fam in families:
        if fam.marriage is None:
            continue

        wife = get_individual(fam.wife)
        hubby = get_individual(fam.husband)

        wife_marriage_age = (fam.marriage - wife.birth).days / 365.24
        husband_marriage_age = (fam.marriage - hubby.birth).days / 365.24

        if wife_marriage_age < 14 and husband_marriage_age < 14:
            notes.append("{} and {} both got married before the age of 14!".format(wife.name, hubby.name))
            notes.append("They got married on: {} and {}'s birth date is: {} and {}'s birth date is: {}".format(
                format_date(fam.marriage),
                wife.name, format_date(wife.birth), hubby.name, format_date(hubby.birth)))
            proper_marriage = False
        elif wife_marriage_age < 14:
            notes.append("{} got married before the age of 14!".format(wife.name))
            notes.append(
                "{} got married on: {} and their birth date is: {}".format(wife.name, format_date(fam.marriage),
                                                                           format_date(wife.birth)))
            proper_marriage = False
        elif husband_marriage_age < 14:
            notes.append("{} got married before the age of 14!".format(hubby.name))
            notes.append(
                "{} got married on: {} and their birth date is: {}".format(hubby.name, format_date(fam.marriage),
                                                                           format_date(hubby.birth)))
            proper_marriage = False

    if proper_marriage:
        result = "Every person here got married at the right age."
    else:
        result = "Someone got married waaay too early."

    table.append(
        ["US10", "Marriage After 14", "\n".join(notes), proper_marriage, result])


def no_bigamy(table):  # US11: No Bigamy
    bigamy = False
    notes = []
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
                    bigamy = check_bigamy_spouse_death(ind, marriages[i], marriages[j], bigamy, notes)
                elif marriages[i].divorce is None:  # Was Family A created before Family B divorce/death?
                    bigamy = check_bigamy_divorce_spouse_death(ind, marriages[i], marriages[j], bigamy, notes)
                elif marriages[j].divorce is None:  # Was Family B created before Family A divorce/death?
                    bigamy = check_bigamy_divorce_spouse_death(ind, marriages[j], marriages[i], bigamy, notes)
                else:  # Both families are divorced
                    bigamy = check_bigamy_divorce(ind, marriages[i], marriages[j], bigamy, notes)

    if bigamy:
        result = "There are bigamy cases in this GEDCOM file."
    else:
        result = "There are no bigamy cases in this GEDCOM file."

    table.append(
        ["US11", "No Bigamy", "\n".join(notes), not bigamy, result])


def parents_not_too_old(table):  # US12: Parents Not Too Old
    too_old = False
    notes = []
    for fam in families:
        if fam.children:
            mom = get_individual(fam.wife)
            dad = get_individual(fam.husband)
            for child_id in fam.children:
                child = get_individual(child_id)
                if abs(get_age(mom) - get_age(child)) > 60 and abs(get_age(dad) - get_age(child)) > 80:
                    notes.append("{}'s parents, {} and {}, are too old.".format(child.name, mom.name, dad.name))
                    too_old = True
                elif abs(get_age(mom) - get_age(child)) > 60:
                    notes.append("{}'s mother, {}, is too old.".format(child.name, mom.name))
                    too_old = True
                elif abs(get_age(dad) - get_age(child)) > 80:
                    notes.append("{}'s father, {}, is too old.".format(child.name, dad.name))
                    too_old = True

    if too_old:
        result = "Some parents are too old in this GEDCOM file."
    else:
        result = "All parents are not too old in this GEDCOM file."

    table.append(
        ["US12", "Parents Not Too Old", "\n".join(notes), not too_old, result])


def sibling_age_space(table):  # US13: Sibling Age Spacing
    sibling_space = True
    notes = []
    for fam in families:
        if fam.children and len(fam.children) > 1:
            for i in range(len(fam.children)):
                for j in range(i + 1, len(fam.children)):
                    if 2 < abs((get_individual(fam.children[i]).birth - get_individual(fam.children[j]).birth).days) < \
                            243.3:
                        notes.append("{} and {} are not spaced properly.".format(get_individual(fam.children[i]).name,
                                                                                 get_individual(fam.children[j]).name))
                        sibling_space = False

    if sibling_space:
        result = "All sibling ages are spaced properly."
    else:
        result = "Some sibling ages are not spaced properly."

    table.append(
        ["US13", "Sibling Age Spacing", "\n".join(notes), sibling_space, result])


def fewer_than_fifteen_siblings(table):  # US15: Fewer Than 15 Siblings
    too_many_kids = False
    notes = []
    for fam in families:
        if fam.children and len(fam.children) >= 15:
            notes.append("Family {} has greater than 15 children.".format(fam.f_id))
            too_many_kids = True

    if too_many_kids:
        result = "Some families have too many children."
    else:
        result = "All families have less than 15 children."

    table.append(
        ["US15", "Fewer Than 15 Siblings", "\n".join(notes), not too_many_kids, result])


def male_last_names(table):  # US16: Male Last Names
    fathers_last_name = True
    notes = []
    for fam in families:
        if fam.children:
            last_name = get_individual(fam.husband).name[get_individual(fam.husband).name.rfind(" "):]

            for kid in fam.children:
                if get_individual(kid).sex == "M" and last_name not in get_individual(kid).name:
                    notes.append(
                        "{} does not have his father's last name, {}".format(get_individual(kid).name, last_name))
                    fathers_last_name = False

    if fathers_last_name:
        result = "All male children have their father's last name."
    else:
        result = "Some male children don't have their father's last name."

    table.append(
        ["US16", "Male Last Names", "\n".join(notes), fathers_last_name, result])


def no_marriage_to_descendants(table):  # US17: No Marriage to Descendants
    descendant_marriage = False
    notes = []

    for ind in individuals:
        descendants = get_descendants(ind.i_id)
        if descendants:
            for fam_id in get_individuals_families(ind.i_id):
                if any(s_id in descendants for s_id in [get_family(fam_id).husband, get_family(fam_id).wife]):
                    if ind.i_id == get_family(fam_id).husband:
                        notes.append(
                            "{} is married to descendant, {}.".format(ind.name,
                                                                      get_individual(get_family(fam_id).wife).name))
                    else:
                        notes.append("{} is married to descendant, {}.".format(ind.name,
                                                                               get_individual(
                                                                                   get_family(fam_id).husband).name))
                    descendant_marriage = True

    if descendant_marriage:
        result = "Some ancestors are married to descendants."
    else:
        result = "No ancestors are married to descendants."

    table.append(
        ["US17", "No Marriage to Descendants", "\n".join(notes), not descendant_marriage, result])


def siblings_should_not_marry(table):  # US18: Siblings Should Not Marry
    sibling_marriage = False
    notes = []
    for fam in families:
        if fam.children and len(fam.children) > 1:
            for i in range(len(fam.children)):
                for j in range(i + 1, len(fam.children)):
                    if any(fam.children[i] in [f.husband, f.wife] and fam.children[j] in [f.husband, f.wife] for f in
                           families):
                        sibling_marriage = True
                        notes.append("{} and {} are married siblings.".format(get_individual(fam.children[i]).name,
                                                                              get_individual(fam.children[j]).name))

    if sibling_marriage:
        result = "Some siblings are married."
    else:
        result = "All siblings are not married."

    table.append(
        ["US18", "Siblings Should Not Marry", "\n".join(notes), not sibling_marriage, result])


def order_children_by_age(table):  # US28: Order Siblings By Age
    for fam in families:
        if fam.children:
            fam.children.sort(key=lambda child: get_individual(child).birth)

    table.append(
        ["US28", "Order Siblings By Age", "", True, "---Reordered Children---\n{}\n".format(print_families())])


def list_deceased(table):  # US29: List Deceased
    results = "\n".join([ind.name for ind in individuals if ind.death is not None])

    table.append(
        ["US29", "List Deceased", "", True, results])


def list_living_married(table):  # US30: List Living Married
    living_married = []

    for person in individuals:
        if person.spouse_id is not None and person.death is None:
            living_married.append(person.name)

    table.append(
        ["US30", "List Living Married", "", True, "\n".join(living_married)])


def list_living_single(table):  # US31: List Living Single
    living_single = []

    for person in individuals:
        if person.spouse_id is None and person.death is None:
            living_single.append(person.name)

    table.append(
        ["US31", "List Living Single", "", True, "\n".join(living_single)])


def list_recent_births(table):  # US35: List Recent Births
    recent_births = []

    for person in individuals:
        if person.birth is not None and datetime.now().date() - timedelta(
                days=365) <= person.birth <= datetime.now().date():
            recent_births.append(person.name)

    table.append(
        ["US35", "List Recent Births", "", True, "\n".join(recent_births)])


def list_recent_deaths(table):  # US36: List Recent Deaths
    recent_deaths = []

    for person in individuals:
        if person.death is not None and datetime.now().date() - timedelta(
                days=365) <= person.death <= datetime.now().date():
            recent_deaths.append(person.name)

    table.append(
        ["US36", "List Recent Deaths", "", True, "\n".join(recent_deaths)])


def run_stories():
    headers = ["User Story", "Description", "Notes", "Pass", "Result"]
    table = []
    dates_before_today(table)  # US01
    birth_before_marriage(table)  # US02
    birth_before_death(table)  # US03
    marriage_before_divorce(table)  # US04
    marriage_before_death(table)  # US05
    divorce_before_death(table)  # US06
    less_than_150_years_old(table)  # US07
    birth_before_parents_death(table)  # US09
    marriage_after_fourteen(table)  # US10
    no_bigamy(table)  # US11
    parents_not_too_old(table)  # US12
    sibling_age_space(table)  # US13
    fewer_than_fifteen_siblings(table)  # US15
    male_last_names(table)  # US16
    no_marriage_to_descendants(table)  # US17
    siblings_should_not_marry(table)  # US18
    order_children_by_age(table)  # US28
    list_deceased(table)  # US29
    list_living_married(table)  # US30
    list_living_single(table)  # US31
    list_recent_births(table)  # US35
    list_recent_deaths(table)  # US36

    return tabulate(table, headers, tablefmt="fancy_grid")


def main():
    process_file(read_file())
    print("--- Individuals ---\n{}\n".format(print_individuals()))
    print("--- Families ---\n{}\n".format(print_families()))
    print("--- User Stories ---\n{}".format(run_stories()))


if __name__ == '__main__':
    main()
