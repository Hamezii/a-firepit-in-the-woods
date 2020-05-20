# A Firepit in the Woods
```
dan, suzie, and alex are sat around a firepit in the woods.
dan talks about "the 90's".
alex chops some firewood.
the fire hums a familiar tune.
```


# Overview
*A Firepit in the Woods* is a fantasy language, or esolang. 

Source code in this language documents the actions of some friends sitting around a campfire. 
Each program takes place over the course of an evening.

# Example Code
## Output the letter 'a'.
```
dan and alex are sat around a firepit in the woods.
dan chops some firewood.
dan puts some firewood into the firepit.
dan puts a match into the firepit.
the fire hums a familiar tune.
they wish each other goodnight, and go their seperate ways.
```
## Truth machine

    dan and suzie are sat around a firepit in the woods.

    when dan talks about "repeat",
    dan throws his twigs into the firepit.
    dan throws a match into the firepit.
    the firepit hums an unfamiliar tune.
    the firepit is calmly quiet.
    dan leaves to scavenge for twigs.

    dan finds some twigs in his backpack.
    if dan has twigs, dan talks about "repeat" until there is a fire burning.
    the firepit hums an unfamiliar tune.
    they wish each other goodnight, and go their separate ways.
If the user inputs a 0, the program outputs 0 and terminates.
If the user inputs a 1, the program outputs 1 indefinitely.

# Syntax
All *A Firepit in the Woods* source code is in lower case, for that ***chillll vibe***.

## Start of program (header)
The code section of a program always begins with an establishing sentence stating who is sat around the firepit:

    dan, alex, and suzie are sat around a firepit in the woods.

Any combination of two or more people can be sat around the firepit, as long as they are valid characters i.e. one of the following:
 - Alex
 - Dan
 - Suzie

Certain characters can perform actions which are unique to them:
- Suzie has a notepad which she can flip through, and draw/erase lines on the pages. It acts similar to a tape, where each page can store an integer value (number of lines), and Suzie reads and writes to the page she is currently on.

## End of program (footer)
For redundancy's sake, the code section of a program always ends with the friends heading home for the night.

    they wish each other goodnight, and go their separate ways.

This is in order for the narrative to get proper closure, that is all.

## Comments
Any text on the lines before the header or after the footer are ignored, so can contain any arbitrary text.

Adding a `#` in a program will cause the interpreter to ignore the rest of the line.

    You can describe the program here if you like, no worries!
    Anything above the header is ignored.

    dan and alex are sat around a firepit in the woods.

    dan talks about "girls". # this is a valid comment
    alex leaves to scavenge for twigs.   # Alex is clearly uninterested.

    they wish each other goodnight, and go their separate ways.

    Anything down here, after the footer, is ignored too.

