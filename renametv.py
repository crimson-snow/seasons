#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from natsort import natsorted, ns


class Series:
    def __init__(self, seasonnum, title, episodes=None):
        self.title = title
        self.seasonnum = seasonnum
        self.episodes = []


class Episode:
    ignoredtypes = {'.sfv', '.DS_Store', '.Spotlight-V100', '.Trashes',
                    '.DocumentRevisions-V100', '.fseventsd',
                    '.VolumeIcon.icns', '.localized', '.gitignore'}

    def __init__(self, title, episodenum,
                 origfilename, newfilename=None,
                 source=None, destination=None):
        self.title = title
        self.episodenum = episodenum
        self.origfilename = origfilename
        self.extension = origfilename.split('.')[1]
        self.newfilename = newfilename
        self.source = source
        self.destination = destination

    def makefilename(self, seasonnum):
        self.newfilename = (self.title
                            + ' - S{:02d}'.format(seasonnum)
                            + 'E{:02d}'.format(self.episodenum)
                            + '.' + self.extension)

    def __repr__(self):
        return "Episode('{}', '{}', '{}', '{}')".format(self.title,
                                                        self.episodenum,
                                                        self.origfilename,
                                                        self.newfilename,
                                                        self.source,
                                                        self.destination)


def main():
    parser = argparse.ArgumentParser(description='A lightweight organization \
                                                  tool for your media library',
                                     epilog='The current working \
                                                directory is the default \
                                                input and output location')

    parser.add_argument('title', metavar='TITLE',
                        help='specify a TV show title')
    parser.add_argument('dir', metavar='DIR',  nargs='*', default='.',
                        help='specify a working directory')
    parser.add_argument('-c', '--copy', action='store_true',
                        help='copy files to output location')
    parser.add_argument('-e', '--episodestart', type=int, default=1,
                        help='specify the starting episode number')
    parser.add_argument('-o', '--output',
                        help='specify an output location')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='surpress prompts and proceed with writing files')
    parser.add_argument('-s', '--seasonstart', type=int, default=1,
                        help='specify the starting season number')
    parser.add_argument('--version', action='version',
                        version='%(prog)s v1.1.1')

    args = parser.parse_args()

    options = {
        'title': args.title,
        'directories': args.dir,
        'copy': args.copy,
        'quiet': args.quiet,
        'output': args.output or False,
        'seasonnum': args.seasonstart,
        'episodenum': args.episodestart,
    }

    series = Series(options['seasonnum'], options['title'])

    for directory in options['directories']:
        directory = directory.rstrip('/')
        if not options['output']:
            options['output'] = directory

        for file in [x for x in natsorted(os.listdir(directory),
                     alg=ns.IGNORECASE)
                     if not os.path.splitext(x)[0] in Episode.ignoredtypes
                     if not os.path.splitext(x)[1] in Episode.ignoredtypes
                     if not os.path.isdir(os.path.join(directory, x))]:

            newep = Episode(series.title, options['episodenum'], file)

            newep.makefilename(series.seasonnum)
            newep.source = directory
            newep.destination = '{}/Season {:02d}'.format(options['output'],
                                                          series.seasonnum)

            series.episodes.append(newep)

            print('[{}] from [{}/{}] to [{}/{}]'.format(mode(options['copy']),
                                                        newep.source,
                                                        newep.origfilename,
                                                        newep.destination,
                                                        newep.newfilename))

            options['episodenum'] += 1

        if options['quiet'] or userprompt():
            writefiles(series.episodes, options['copy'])
        else:
            sys.exit()

        # Reset values for next directory
        series.episodes.clear()
        options['episodenum'] = 1
        series.seasonnum += 1


def writefiles(episodes, copy):
    for e in episodes:
        if not os.path.exists(e.destination):
                os.makedirs(e.destination)
        mode = 'COPYING' if copy else 'MOVING'
        try:
            print('[{}] from [{}/{}] to [{}/{}]'.format(mode,
                                                        e.source,
                                                        e.origfilename,
                                                        e.destination,
                                                        e.newfilename))
            if copy:
                shutil.copy(e.source + '/' + e.origfilename,
                            e.destination + '/' + e.newfilename)
            else:
                shutil.move(e.source + '/' + e.origfilename,
                            e.destination + '/' + e.newfilename)

        except shutil.SameFileError:
                print('Cannot {}}. File already exists at the desired \
                      output location.'.format(mode(copy).lower()))


def userprompt():
    while True:
        userinput = input('Write files? [(y)es, (n)o, (q)uit]').lower()

        if userinput == 'y':
            return True
        elif userinput == 'n' or userinput == 'q':
            print('No changes made.')
            return False
        else:
            print('Please enter a valid option.')

        print('\n')


def mode(argument):
    switcher = {
        0: "MOVE",
        1: "COPY"
    }
    return switcher.get(argument, "nothing")


if __name__ == '__main__':
    main()
