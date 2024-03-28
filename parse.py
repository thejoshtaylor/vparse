# Joshua Taylor
# March 2024

# This file reads in an Agilent Vee file and builds objects in memory

import json

# Parse the file
def parse(filename):
    objects = []

    with open(filename) as file:
        # Go character by character
        # Open parantheses indicate a new object
        # While space indicates a new property
        # Close parantheses indicate the end of an object
        # Objects can be nested

        objTemplate = {
            "type": "",
            "objects": []
        }

        obj = {}

        objStack = []

        gettingType = True
        inQuote = False
        value = ""
        
        # Parse one character at a time from the file
        for char in file.read():
            if char == "(":
                if obj:
                    objStack.append(obj)
                obj = objTemplate.copy()
                gettingType = True
                value = ""

            elif char.isspace():
                if inQuote:
                    value += char

                elif gettingType:
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

                if len(objStack) > 0:
                    currObject = objStack.pop()
                    currObject["objects"].append(obj)
                    obj = currObject
                else:
                    objects.append(obj)
                    obj = objTemplate.copy()

            else:
                value += char

    return objects

# Export the objects as JSON
def export(objects):
    # Create a new file
    filename = "output.json"
    with open(filename, "w") as file:
        json.dump(objects, file, indent=4)

    return filename