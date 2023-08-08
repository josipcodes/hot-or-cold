# used to delay print
import sys
import time
# used to clear terminal
import os
# importing art to print game name and goodbye messages
from art import tprint


# Original code borrowed from:
# https://python-programs.com/python-how-to-find-an-element-in-tuple-by-value/
def search_element(given_tuple, element):
    """
    Function returns True if given element is found in a tuple
    """
    # using for loop to traverse the tuple
    for value in given_tuple:
        # if the given element is equal to the value then return True
        if value == element:
            return True
    # if the element is not found in tuple then return False
    return False


# Original code borrowed from gnuton (GitHub),
# however, adapted for suitability and learning purposes.
def slow_print(line):
    """
    Prints each string/line with a delay of .3 sec.
    Link to the source code is within the Credits section of the README file.
    """
    # prints a line and goes to the next row
    sys.stdout.write(line + "\n")
    # sets delay to 0.3s
    time.sleep(0.3)


# obtained from: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    """
    Function clears the terminal to prevent clutter.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def hello():
    tprint("Hot or cold", font="graffiti")


def bye():
    tprint("Bye", font="graffiti")
