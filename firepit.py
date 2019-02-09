"""An interpreter for a firepit in the woods."""

import os
import sys

from lark import Tree

import parse


class Person:
    """Stores the state of a person."""
    def __init__(self, number):
        self.number = number
        self.twigs = 0
    def __repr__(self):
        return "Person("+str(self.number)+", "+str(self.twigs)+")"


class Notepad:
    """Stores the state of a notepad."""
    ACTIONS = ("next_page", "last_page", "inc_page", "dec_page")
    def __init__(self):
        self.pages = [0]
        self.page_num = 0

    def next_page(self):
        """Turn to next page."""
        self.page_num += 1
        if self.page_num == len(self.pages):
            self.pages.append(0)

    def last_page(self):
        """Turn to last page."""
        self.page_num = max(self.page_num-1, 0)

    def inc_page(self):
        """Add to page."""
        self.pages[self.page_num] += 1

    def dec_page(self):
        """Remove from page."""
        self.pages[self.page_num] = max(self.pages[self.page_num]-1, 0)

    def get_lines(self):
        """Get how many lines are on the current page."""
        return self.pages[self.page_num]

class Interpreter:
    """Can run a parsed tree. Also stores state of the program."""
    def __init__(self):
        self.people = {}
        self.firewood = 0

        self.is_fire = False
        self.fuel = 0

        self.talk_reactions = {}

        self.notepad = None

    def execute(self, node):
        """
        Execute a node in the parse tree.
        Recursively execute which node to execute next.
        """
        if node.data in Notepad.ACTIONS:
            self._notepad_action(node.data)
        else:
            getattr(self, node.data)(node)

    def _firepit_out(self, is_fire, is_not_fire):
        """
        A helper function for outputting different things depending
        on whether there is a fire or not.
        """
        if self.is_fire:
            print(is_fire, end="")
        else:
            print(is_not_fire, end="")

    def _pass_time(self, time):
        """Pass a certain amount of time. The fire will consume fuel."""
        if self.is_fire:
            self.fuel = max(self.fuel - time, 0)
            if self.fuel == 0:
                self.is_fire = False

    def _notepad_action(self, action):
        """
        Carry out a notepad action, raising an error if the notepad has not been
        intialised.
        """
        if self.notepad is None:
            raise SyntaxError("Suzie's can't use her notepad if it is still in her backpack.")
        return getattr(self.notepad, action)()

    def _is_true(self, condition):
        """Check if a condition is true."""
        if condition.children:
            return getattr(self, condition.data)(*condition.children)
        else:
            return getattr(self, condition.data)()

    def start(self, node):
        """Start of the execution of the program."""
        for node in node.children:
            self.execute(node)

    def header(self, node):
        """Initialise the variables."""
        for i, person in enumerate(node.children):
            name = person.value
            if name is self.people:
                raise SyntaxError("More than one person called {0} are around the firepit.".format(name))
            self.people[name] = Person(2**i)

    def footer(self, _):
        """Finish executing the program."""
        print()

    def when_talks_about(self, node):
        """Execute a codeblock when someone talks about something."""
        talk_key = (node.children[0].value, node.children[1].value)
        self.talk_reactions[talk_key] = node.children[2]

    def codeblock(self, node):
        """Execute the nodes one at a time."""
        for node in node.children:
            self.execute(node)

    def get_firewood(self, node):
        """Get firewood."""
        person = self.people[node.children[0].value]
        self.firewood += person.number
        self._pass_time(1)

    def use_firewood(self, node):
        """Use firewood."""
        person = self.people[node.children[0].value]
        used = min(person.number, self.firewood)
        self.fuel += used
        self.firewood -= used

    def get_twigs(self, node):
        """Get twigs."""
        person = self.people[node.children[0].value]
        person.twigs += person.number
        self._pass_time(1)

    def use_twigs(self, node):
        """Use twigs."""
        person = self.people[node.children[0].value]
        self.fuel += person.twigs
        person.twigs = 0

    def light_fire(self, _):
        """Light a fire if there is enough fuel."""
        if self.fuel > 0:
            self.is_fire = True

    def firepit_lowercase(self, _):
        """Print a lowercase letter corresponding to the current fuel level. a=1, z=26.

        If there is no fire, print a space.
        """
        self._firepit_out(chr(97 + (self.fuel-1)%26), " ")

    def firepit_uppercase(self, _):
        """Print an uppercase letter corresponding to the current fuel level. a=1, z=26.

        If there is no fire, print a space.
        """
        self._firepit_out(chr(65 + (self.fuel-1)%26), " ")

    def firepit_number(self, _):
        """Print a number corresponding to the current fuel level."""
        self._firepit_out(self.fuel, 0)

    def firepit_newline(self, _):
        """Print a newline."""
        print()

    def talk(self, node):
        """Talk about something. Can trigger reactions."""
        talk_key = (node.children[0].value, node.children[1].value)
        if talk_key in self.talk_reactions:
            self.execute(self.talk_reactions[talk_key])

    def wait(self, node):
        """Wait for an amount of time depending on the person."""
        name = node.children[0].value
        self._pass_time(self.people[name].number)

    def ask_twigs(self, node):
        """Recieve a number and give a person that many twigs."""
        amount = int(input())
        name = node.children[0].value
        self.people[name].twigs += amount

    def init_notepad(self, _):
        """Initialise the notepad."""
        self.notepad = Notepad()

    def repeat(self, node):
        """Repeat until a condition is met."""
        condition = node.children[1]
        statement = node.children[0]
        while not self._is_true(condition):
            self.execute(statement)

    def if_true(self, node):
        """Do something only if a condition is true."""
        condition, statement = node.children
        if self._is_true(condition):
            self.execute(statement)

    def say(self, node):
        """Print a string."""
        print(node.children[1], end="")

    def no_fire(self):
        """No fire."""
        return not self.is_fire
    def yes_fire(self):
        """Yes fire."""
        return self.is_fire
    def no_firewood(self):
        """No firewood."""
        return self.firewood == 0
    def yes_firewood(self):
        """Yes firewood."""
        return self.firewood > 0
    def no_twigs(self, node):
        """No twigs."""
        person = node.value
        return self.people[person].twigs == 0
    def yes_twigs(self, node):
        """Yes twigs."""
        person = node.value
        return self.people[person].twigs > 0
    def no_lines(self):
        """No lines on notepad page."""
        return self._notepad_action("get_lines") == 0
    def yes_lines(self):
        """Lines on notepad page."""
        return self._notepad_action("get_lines") > 0


def interpret(source_file_path):
    """Interpret a source file."""

    with open(source_file_path, "r") as code_file:
        code = code_file.read()
    tree: Tree = parse.parse(code)
    #print(tree.pretty(), "\n")
    Interpreter().execute(tree)
    print()
    input("Done.")

def main():
    """Run the interpreter."""
    if len(sys.argv) == 1:
        source_file_path = input("Input the source file path to interpret: ")
    else:
        source_file_path = sys.argv[1]
    if os.path.exists(source_file_path):
        if source_file_path.split(".")[1] == "fire":
            interpret(source_file_path)
        else:
            print("'"+source_file_path+"' does not have a .fire extension.")
    else:
        print("'"+source_file_path+"' is not a valid path.")

def test():
    """Test the interpreter."""
    interpret("test.txt")

if __name__ == "__main__":
    #test()
    main()
