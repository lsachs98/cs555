#user story 29, list all deceased
from parse_to_objects import *
def list_deceased(GEDinfo):
	all_individuals = GEDinfo.get_individuals()
	deceased = []
	for i in all_individuals:
		if i.get_death() != "NA":
			deceased.append(i.get_id())

	return deceased
	
