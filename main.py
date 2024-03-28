# Joshua Taylor
# March 2024

# This file has a menu that allows the user to choose between parsing and drawing

import parse
import draw

import os
import argparse


# Get arguments from command line input
ap = argparse.ArgumentParser(description="Parse and draw Agilent Vee files")
ap.add_argument("filename", nargs="?", help="The filename to parse")
args = ap.parse_args()

# Get the file from user input
def inputFile():
    # Check if there's a command line argument
    if args.filename is not None:
        try:
            with open(args.filename) as file:
                return args.filename
        except FileNotFoundError:
            print("Argument file not found")

    # Get filename from user input
    while True:
        try:
            filename = input("Enter filename: ")
            with open(filename) as file:
                return filename
        except FileNotFoundError:
            print("File not found")

def main():
    # Print header
    print()
    print('=' * 50)
    print('VPARSER'.center(50))
    print('=' * 50)
    print('Joshua Taylor'.ljust(25) + 'Mar 2024'.rjust(25))
    print()

    # Get file
    file = inputFile()

    # Get size of file
    size = os.path.getsize(file)

    # If file is large, show progress
    doProgress = size > 1000000

    print()
    print(f"Reading {os.path.basename(file)}... ", end="", flush=True)

    # Parse file
    objects = parse.parse(file, doProgress)

    print("done")

    # Get total number of objects
    # print(f"Found {parse.count(objects)} objects")
    print()
    
    # Menu
    while True:
        print("1. Draw")
        print("2. Export as JSON")
        print("3. Quit")
        choice = input("> ")
        
        if choice == "1":
            draw.draw(objects)
        elif choice == "2":
            jsonFile = parse.export(objects)
            print(f"Exported to {jsonFile}")
        elif choice == "3":
            break
        else:
            print("Invalid choice")
        print()

if __name__ == "__main__":
    main()