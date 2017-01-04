#!/usr/bin/env python3

import os
import sys

USAGE = "Usage: " + sys.argv[0] +\
        " directory \"Name of Series\" season [start] [extentison]\n"\
        "Rename video files within specified directory"

episodenames = {}


def main():
    if len(sys.argv) < 3:
        print(USAGE)
    else:
        directory = sys.argv[1]
        title = sys.argv[2]
        season = int(sys.argv[3])

        try:
            increment = int(sys.argv[4])
        except IndexError:
            increment = 1

        try:
            extension = sys.argv[5]
            if extension[0] != ".":
                extension = "." + extension
        except IndexError:
            print("No file extension provided, assuming .mkv")
            extension = ".mkv"

        collectfilenames(directory, title, season, increment, extension)

        usrinput = input("Rename files? (y/n) ").lower()

        if usrinput == "y":
            for key, val in episodenames.items():
                os.rename(key, val)
        else:
            print("Exiting...")
            sys.exit()


def collectfilenames(directory, title, season, inc, ext):
    for filename in [x for x in os.listdir(directory) if ext in x[-5:]]:
            newname = (title + " - S{:02d}".format(season) +
                       "E{:02d}".format(inc) + ext)
            print(filename + " --> " + newname)
            episodenames[directory + '/' + filename] = (directory + '/' +
                                                        newname)
            inc += 1

if __name__ == '__main__':
    main()
