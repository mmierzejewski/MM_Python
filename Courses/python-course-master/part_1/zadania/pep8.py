import os, sys, json

__author__ = "Andrzej Krawczyk - Pep8 test"

from sys import path, path_hooks

class Point(object):

    def __init__(self, x, z, SomeData):
        self.x = x
        self.z = z
        self.someData = SomeData

    def title(self):
        return "%s" % self.someData


def SomeDataProcessor(a, b, y = 10, c=20, e=[1,2,3,4]):
    result = 0
    for x in range(15):
        result = (a**2 + (c / y * e) + b**b +10-20+33**2)
        if result % 2 == 0:
                    print("oh!")

def fOo(m, y, d="Ann has a cat", h='7 dwarfs'):
    return (
        d + h
        )

def bar(a, b):
    return sum(a) / float(b)

some_results = fOo(1, 2,
               "zxc",
        h="askdj"
                   )

list_of_people = [
 "Rama",
 "John",
 "Shiva",
    "Janusz"
    ]

test_sentence = "This is a very long line of code containing just some text of a certain length and I think it's quite a bit too long"
second_sentence = 'this is another long line of text for testing'

with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())

income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)


result1 = "{} {} {}".format(test_sentence, 2, 3)