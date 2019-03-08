import unittest
from pprint import pprint
from project03 import *
from US_28 import *


class Test(unittest.TestCase):

	def test_same_age(self):
		child_one = Individual("@I1@")
		child_one.set_name("Lauren Sachs")
		child_one.set_birth("25 AUG 1998")
		fam = Family("F1")
		fam.add_child(child_one)
		child_two = Individual("@I2@")
		child_two.set_name("Lauren Sachs")
		child_two.set_birth("25 AUG 1998")
		fam.add_child(child_two)
		sorted_kids = order_children_by_age([fam])
		assert("@I1@" == sorted_kids[0][0])
		assert("@I2@" == sorted_kids[0][1])

	def test_one_family_many_children_one_family_none(self):
		family_a = Family("@F1@")
		child_a_one = Individual("@I1@")
		child_a_one.set_name("Lauren Sachs")
		child_a_one.set_birth("25 AUG 1998")
		family_a.add_child(child_a_one)
		child_a_two = Individual("@I2@")
		child_a_two.set_name("Lauren Sachs")
		child_a_two.set_birth("26 AUG 1998")
		family_a.add_child(child_a_two)
		family_b = Family("@F2@")
		sorted_kids = order_children_by_age([family_a, family_b])
		assert("@I1@" == sorted_kids[0][0])
		assert("@I2@" == sorted_kids[0][1])
		assert([] == sorted_kids[1])

	def test_no_children(self):
		fam = Family("@F1@")
		sorted_kids = order_children_by_age([fam])
		assert([] == sorted_kids[0])

	def test_one_child(self):
		fam = Family("@F1@")
		child_one = Individual("@I1@")
		child_one.set_name("Lauren Sachs")
		child_one.set_birth("25 AUG 1998")
		fam.add_child(child_one)
		sorted_kids = order_children_by_age([fam])
		assert("@I1@" == sorted_kids[0][0])


	def test_multiple_family(self):
		family_a = Family("@F1@")
		child_a_one = Individual("@I1@")
		child_a_one.set_name("Lauren Sachs")
		child_a_one.set_birth("25 AUG 1998")
		family_a.add_child(child_a_one)
		child_a_two = Individual("@I2@")
		child_a_two.set_name("Lauren Sachs")
		child_a_two.set_birth("26 AUG 1998")
		family_a.add_child(child_a_two)
		family_b = Family("@F2@")
		child_b_one = Individual("@I3@")
		child_b_one.set_name("Lauren Sachs")
		child_b_one.set_birth("27 AUG 1998")
		family_b.add_child(child_b_one)
		child_b_two = Individual("@I4@")
		child_b_two.set_name("Lauren Sachs")
		child_b_two.set_birth("28 AUG 1998")
		family_b.add_child(child_b_two)
		sorted_kids = order_children_by_age([family_a, family_b])
		assert("@I1@" == sorted_kids[0][0])
		assert("@I2@" == sorted_kids[0][1])
		assert("@I3@" == sorted_kids[1][0])
		assert("@I4@" == sorted_kids[1][1])

if __name__ == '__main__':
        unittest.main()