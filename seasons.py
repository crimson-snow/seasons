#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
import re
import magic
from natsort import natsorted, ns


class Series:
    def __init__(self, seasonnum, title, episodes=None):
        self.title = title
        self.seasonnum = seasonnum
        self.episodes = []

    def __repr__(self):
        repr = "Series('{}', '{}', '{}')"
        return repr.format(self.title,
                           self.seasonnum,
                           self.episodes)


class Episode:
    ignored = {'.nfo',
               '.sfv',
               '.DS_Store',
               '.Spotlight-V100',
               '.Trashes',
               '.DocumentRevisions-V100',
               '.fseventsd',
               '.VolumeIcon.icns',
               '.localized',
               '.gitignore'}

    def __init__(self, title, episodenum,
                 origfilename, newfilename=None,
                 source=None, destination=None, extension=None):
        self.title = title
        self.episodenum = episodenum
        self.origfilename = origfilename
        self.extension = extension
        self.newfilename = newfilename
        self.source = source
        self.destination = destination

    def makefilename(self, seasonnum, scheme=None):
        if scheme is None:
            self.newfilename = (self.title
                                + ' - S{:02d}'.format(seasonnum)
                                + 'E{:02d}'.format(self.episodenum)
                                + '.' + self.extension)
        else:
            rep = {"{t}": self.title,
                   "{s}": str(seasonnum),
                   "{e}": str(self.episodenum).zfill(2)}

            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            scheme = pattern.sub(lambda m: rep[re.escape(m.group(0))], scheme)

            self.newfilename = scheme + '.' + self.extension

    def __repr__(self):
        repr = "Episode('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
        return repr.format(self.title,
                           self.episodenum,
                           self.origfilename,
                           self.newfilename,
                           self.source,
                           self.destination,
                           self.extension)


def main():
    parser = argparse.ArgumentParser(description='A lightweight organization '
                                                 + 'tool for your '
                                                 + 'media library',
                                     epilog='The current working '
                                            + 'directory is the default '
                                            + 'input and output location')

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
    parser.add_argument('-S', '--scheme',
                        help='define a custom episode naming scheme')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='display file paths in full')
    parser.add_argument('--version', action='version',
                        version='%(prog)s v0.0.1')

    args = parser.parse_args()

    options = {
        'title': args.title,
        'directories': args.dir,
        'copy': args.copy,
        'quiet': args.quiet,
        'output': args.output.rstrip('/') or False,
        'seasonnum': args.seasonstart,
        'scheme': args.scheme,
        'episodenum': args.episodestart,
        'verbose': args.verbose
    }

    series = Series(options['seasonnum'], options['title'])

    for directory in options['directories']:
        directory = directory.rstrip('/')
        if not options['output']:
            options['output'] = directory

        for file in [x for x in natsorted(os.listdir(directory),
                     alg=ns.IGNORECASE)
                     if not os.path.isdir(os.path.join(directory, x))]:

            if '.' in file:
                name, ext = file.rsplit('.', 1)
                if name in Episode.ignored or '.' + ext in Episode.ignored:
                    continue
            else:
                name = file
                # If extension does not exist, make one
                ext = os.path.basename(magic.from_file(directory
                                                       + '/'
                                                       + file,
                                                       mime=True))

            newep = Episode(series.title,
                            options['episodenum'],
                            file,
                            extension=ext)

            newep.makefilename(series.seasonnum, options['scheme'])
            newep.source = directory
            newep.destination = '{}/Season {:02d}'.format(options['output'],
                                                          series.seasonnum)

            series.episodes.append(newep)

            src = newep.source + '/' + newep.origfilename
            dest = newep.destination + '/' + newep.newfilename

            # Truncate begining of long paths
            if options['verbose'] is False:
                src = truncpath(src)
                dest = truncpath(dest)

            print('[{}] from [{}] to [{}]'.format(mode(options['copy']),
                                                  src,
                                                  dest))

            options['episodenum'] += 1

        if options['quiet'] or userprompt():
            writefiles(series.episodes, options['copy'])
        else:
            sys.exit()

        # Reset values for next directory
        series.episodes.clear()
        options['episodenum'] = 1
        series.seasonnum += 1
        print('Done!')


def writefiles(episodes, copy):
    for e in episodes:
        if not os.path.exists(e.destination):
                os.makedirs(e.destination)
        mode = 'COPYING' if copy else 'MOVING'
        try:
            epstr = '[{}] [{}] to [{}]'
            print(epstr.format(mode,
                               truncpath(e.origfilename),
                               truncpath(e.destination)))

            if copy:
                shutil.copy(e.source + '/' + e.origfilename,
                            e.destination + '/' + e.newfilename)
            else:
                shutil.move(e.source + '/' + e.origfilename,
                            e.destination + '/' + e.newfilename)

        except shutil.SameFileError:
                print(('Cannot {}! File already exists at the desired '
                       + 'output location.').format(mode(copy).lower()))


def userprompt():
    while True:
        userinput = input('Write files? [(y)es, (n)o, (q)uit] ').lower()

        if userinput == 'y':
            return True
        elif userinput == 'n' or userinput == 'q':
            print('No changes made')
            return False
        else:
            print('Please enter a valid option ')

        print('\n')


def mode(argument):
    switcher = {
        0: "MOVE",
        1: "COPY"
    }
    return switcher.get(argument, "nothing")


def truncpath(path):
    return (path[:8] + '...' + path[-22:]) if len(path) > 33 else path


if __name__ == '__main__':
    main()
