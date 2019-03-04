import datetime
individuals = []
families = []

class Individual:
    def __init__(self, i_id):
        self.i_id = i_id
        self.name = ""
        self.sex = ""
        self.spouse_id = "NA"
        self.child_id = "NA"
        self.birth = ""
        self.death = "NA"
    def set_name(self, name):
        self.name = name
    def set_sex(self, sex):
        self.sex = sex
    def set_spouse(self, family_id):
        self.spouse_id = family_id
    def set_child(self, family_id):
        self.child_id = family_id
    def set_birth(self, birth):
        self.birth = birth
    def set_death(self, death):
        self.death = death
    def get_id(self):
        return self.i_id
    def get_name(self):
        return self.name
    def get_sex(self):
        return self.sex
    def get_spouse(self):
        return self.spouse_id
    def get_child(self):
        return self.child_id
    def get_birth(self):
        return self.birth
    def get_death(self):
        return self.death
class Family:
    def __init__(self, f_id):
        self.f_id = f_id
        self.marriage = ""
        self.divorce = "NA"
        self.husband = ""
        self.wife = ""
        self.children = []
    def set_marriage(self, marriage):
        self.marriage = marriage
    def set_divorce(self, divorce):
        self.divorce = divorce
    def set_husband(self, husband):
        self.husband = husband
    def set_wife(self, wife):
        self.wife = wife
    def add_child(self, child):
        self.children.append(child)
    def get_id(self):
        return self.f_id
    def get_marriage(self):
        return self.marriage
    def get_divorce(self):
        return self.divorce
    def get_husband(self):
        return self.husband
    def get_wife(self):
        return self.wife
    def get_children(self):
        return self.children
def read_file():
    with open("test0.ged") as file:
        lines = file.readlines()
    file.close()
    index = 0
    while index < len(lines):
        line = lines[index].split(" ", 2)
        if len(line) == 3:
            if line[0] == "0" and line[2].rstrip() == "INDI":
                new_individual = Individual(line[1].rstrip())
                index = index + 1
                details = lines[index].split(" ", 2)
                while details[0] != "0" and index < len(lines):
                    if details[0] == "1":
                        if details[1] == "NAME":
                            new_individual.set_name(details[2].rstrip())
                        if details[1] == "SEX":
                            new_individual.set_sex(details[2].rstrip())
                        if details[1] == "FAMS":
                            new_individual.set_spouse(details[2].rstrip())
                        if details[1] == "FAMC":
                            new_individual.set_child(details[2].rstrip())
                        if details[1].rstrip() == "BIRT":
                            index = index + 1
                            details = lines[index].split(" ", 2)
                            if details[0] == "2" and details[1] == "DATE":
                                new_individual.set_birth(details[2].rstrip())
                        if details[1].rstrip() == "DEAT":
                            index = index + 1
                            details = lines[index].split(" ", 2)
                            if details[0] == "2" and details[1] == "DATE":
                                new_individual.set_death(details[2].rstrip())
                    index = index + 1
                    details = lines[index].split(" ", 2)
                individuals.append(new_individual)
                index = index - 1
            if line[0] == "0" and line[2].rstrip() == "FAM":
                new_family = Family(line[1].rstrip())
                index = index + 1
                details = lines[index].split(" ", 2)
                while details[0] != "0" and index < len(lines):
                    if details[0] == "1":
                        if details[1] == "HUSB":
                            new_family.set_husband(details[2].rstrip())
                        if details[1] == "WIFE":
                            new_family.set_wife(details[2].rstrip())
                        if details[1] == "CHIL":
                            new_family.add_child(details[2].rstrip())
                        if details[1].rstrip() == "MARR":
                            index = index + 1
                            details = lines[index].split(" ", 2)
                            if details[0] == "2" and details[1] == "DATE":
                                new_family.set_marriage(details[2].rstrip())
                        if details[1].rstrip() == "DIV":
                            index = index + 1
                            details = lines[index].split(" ", 2)
                            if details[0] == "2" and details[1] == "DATE":
                                new_family.set_divorce(details[2].rstrip())
                    index = index + 1
                    details = lines[index].split(" ", 2)
                families.append(new_family)
                index = index - 1
        index = index + 1


temp = []
stringgs = ''
def monthsplit(date):
    for temp in date:
        temp = date.split()
        if(temp[1] == 'JAN'): 
            temp[1] = '01'
        elif(temp[1] == 'FEB'): 
            temp[1] = '02'
        elif(temp[1] == 'MAR'): 
            temp[1] = '03'
        elif(temp[1] == 'APR'): 
            temp[1] = '04'
        elif(temp[1] == 'MAY'): 
            temp[1] = '05'
        elif(temp[1] == 'JUN'): 
            temp[1] = '06'
        elif(temp[1] == 'JUL'): 
            temp[1] = '07'
        elif(temp[1] == 'AUG'): 
            temp[1] = '08'
        elif(temp[1] == 'SEP'): 
            temp[1] = '09'
        elif(temp[1] == 'OCT'): 
            temp[1] = '10'
        elif(temp[1] == 'NOV'): 
            temp[1] = '11'
        elif(temp[1] == 'DEC'): 
            temp[1] = '12'
        if(temp[0] == '1' or temp[2] == '0' or temp[0] == '3' or temp[0] == '4' or temp[0] == '5' or temp[0] == '6' or temp[0] == '7' or temp[0] == '8' or temp[0] == '9'):
          temp[0] = '0' + temp[0]
        stringgs = str(temp[2]) + '-' + str(temp[1]) + '-' + str(temp[0])
        return stringgs
dates = []
validMarriage = True
def birthBeforeMarriage(indList, famData):
    individuals.sort(key=lambda x: int(x.i_id[1:]))
    families.sort(key=lambda x: int(x.f_id[1:]))
    for fam in famData:
        wifename = individuals[int(fam.get_wife()[1:]) - 1].get_name()
        hubbyname = individuals[int(fam.get_husband()[1:]) - 1].get_name()
        m = monthsplit(fam.get_marriage())
        for ind in indList:
            personname = ind.get_name()
            b = monthsplit(ind.get_birth())
            if (m != None):
                if(wifename == personname or hubbyname == personname):
                    if (m < b):
                        print("---HOUSTON WE HAVE A PROBLEM---")
                        print(personname)
                        print("Birth is: " + ind.get_birth() + " and Marriage is: " + fam.get_marriage())
                        validMarriage = False
    if(validMarriage == True): print("All birth dates were correct")
    else: print("One or more birth/marriage dates were incorrect.")
    return validMarriage

        


def print_individuals():
    individuals.sort(key=lambda x: int(x.i_id[1:]))
    print("--- Individuals ---")
    for ind in individuals:
        print("{}:".format(ind.get_id()))
        print("\tName: {}".format(ind.get_name()))
        print("\tSex: {}".format(ind.get_sex()))
        print("\tBirthday: {}".format(ind.get_birth()))
        print("\tAlive: {}".format(True if ind.get_death() == "NA" else False))
        print("\tDeath: {}".format(ind.get_death()))
        print("\tChildren: {}".format(ind.get_child()))
        print("\tSpouse: {}".format(ind.get_spouse()))
def print_families():
    families.sort(key=lambda x: int(x.f_id[1:]))
    print("\n--- Families ---")
    for fam in families:
        print("{}:".format(fam.get_id()))
        print("\tMarried: {}".format(fam.get_marriage()))
        print("\tDivorced: {}".format(fam.get_divorce()))
        print("\tHusband Id: {}".format(fam.get_husband()))
        print("\tHusband Name: {}".format(individuals[int(fam.get_husband()[1:]) - 1].get_name()))
        print("\tWife Id: {}".format(fam.get_wife()))
        print("\tWife Name: {}".format(individuals[int(fam.get_wife()[1:]) - 1].get_name()))
        print("\tChildren: {}".format(", ".join(fam.get_children())))

def main():
    read_file()
    print_individuals()
    #print()
    print_families()
    birthBeforeMarriage(individuals, families)
    
if __name__ == '__main__':
    main()
