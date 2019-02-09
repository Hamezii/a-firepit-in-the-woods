"""Contains everything needed to parse a stream of text."""

from lark import Lark


def parse(code):
    """Parse code and return a Tree."""
    with open("grammar.lark", "r") as grammar_file:
        grammar = grammar_file.read()
    parser = Lark(grammar)
    tree = parser.parse(code)
    return tree
