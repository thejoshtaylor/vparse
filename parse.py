# Joshua Taylor
# March 2024

# This file reads in an Agilent Vee file and builds objects in memory

import os
import json
import math

# Check the file
def check(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Not a file: {filename}")
    
    if not os.path.getsize(filename):
        raise ValueError(f"Empty file: {filename}")

# Parse the file
def parse(filename, progress=False):
    # Check the file
    check(filename)

    objects = []

    if progress:
        size = os.path.getsize(filename)
        read = 0
        lastSize = -1
        print(' ' * 4, end="")

    with open(filename) as file:
        # Go character by character
        # Open parantheses indicate a new object
        # While space indicates a new property
        # Close parantheses indicate the end of an object
        # Objects can be nested

        obj = {}

        objStack = []

        gettingType = True
        inQuote = False
        escaped = False
        value = ""

        debug = False
        
        # Parse one character at a time from the file
        for char in file.read():
            if char == "\"":
                if inQuote:
                    if not escaped:
                        inQuote = not inQuote
                else:
                    inQuote = not inQuote
            
            # In a quote
            if inQuote:
                value += char

                if char == "\\" and not escaped:
                    escaped = True
                    continue
                
                escaped = False

            # Not in a quote
            else:
                if char == "(":
                    if obj:
                        objStack.append(obj)
                    obj = {
                        "type": "",
                        "objects": []
                    }
                    gettingType = True
                    value = ""

                elif char.isspace():
                    if gettingType:
                        obj["type"] = value
                        gettingType = False
                    else:
                        if value:
                            obj["objects"].append(value)
                        value = ""

                    value = ""

                elif char == ")":
                    if gettingType:
                        obj["type"] = value
                    else:
                        if value:
                            obj["objects"].append(value)
                    value = ""
                    
                    if debug:
                        print(f"ObjStack: {len(objStack)} elements")
                        print(obj)
                        input("[Press Enter]")

                    if len(objStack) > 0:
                        currObject = objStack.pop()
                        currObject["objects"].append(obj.copy())
                        obj = currObject
                    else:
                        if obj["type"] == "ShowOnExecPanel":
                            debug = True
                        objects.append(obj.copy())
                        obj = {}

                else:
                    value += char

            if progress:
                read += 1
                thisSize = math.floor(read / size * 100)
                if thisSize != lastSize:
                    lastSize = thisSize
                    print("\b" * 4 + f"{thisSize}%".rjust(4), end="", flush=True)

    if progress:
        print("\b" * 4 + " " * 4 + "\b" * 4, end="")

    print()
    print(f"ObjStack at end: {len(objStack)} elements")
    # printTypes(objStack)

    return objects

# Count objects
def count(objects):
    total = 0

    for obj in objects:
        total += 1
        if type(obj) == dict and "objects" in obj:
            total += count(obj["objects"])

    return total

# Print tree of all the types of objects, then return the nested tree
def printTypes(objects, level=0):
    tree = {}

    for obj in objects:
        if type(obj) == dict and "objects" in obj:
            print("-" * level + obj["type"])
            tree[obj["type"]] = printTypes(obj["objects"], level + 1)

    return tree

# Export the objects as JSON
def export(objects):
    # Create a new file
    filename = "output.json"
    with open(filename, "w") as file:
        json.dump(objects, file, indent=4)

    return filename