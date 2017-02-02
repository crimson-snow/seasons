#!/usr/bin/env python3

import os
import re
import sys
import shutil
import argparse
import zlib

# ANSI color escape codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m' # No Color

episodes = {}
ignoredtypes = {'.sfv', '.DS_Store', '.Spotlight-V100', '.Trashes',
                '.DocumentRevisions-V100', '.fseventsd',
                '.VolumeIcon.icns', '.localized'}


def main():
    parser = argparse.ArgumentParser(description='Rename many TV show \
                                                episodes for Plex at once',
                                     epilog='The current working \
                                                directory is the default \
                                                input and output location')

    parser.add_argument('title', metavar='TITLE',
                        help='define a TV show title')
    parser.add_argument('dir', metavar='DIR',  nargs='*', default='.',
                        help='define a working directory')
    parser.add_argument('-c', '--copy', action='store_true',
                        help='copy files to output location')
    parser.add_argument('-e', '--extension',
                        help='only rename files with specified extension')
    parser.add_argument('-E', '--episodestart', type=int, default=1,
                        help='specify the starting episode number')
    parser.add_argument('-m', '--makesfv', action='store_true',
                        help='create an sfv file for each DIR')
    parser.add_argument('-o', '--output',
                        help='define an output location')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='surpress prompts and proceed with writing files')
    parser.add_argument('-r', '--readsfv', action='store_true',
                        help='read sfv file in DIR to verify files')
    parser.add_argument('-s', '--seasonstart', type=int, default=1,
                        help='specify the starting season number')
    parser.add_argument('--version', action='version',
                        version='%(prog)s v1.1')

    args = parser.parse_args()

    title = args.title
    directories = args.dir
    output = args.output or directories[0]
    seasonnum = args.seasonstart
    episodenum = args.episodestart
    extension = args.extension

    for directory in directories:
        print(directory)
        if args.readsfv:
            sfv = findsfv(directory)
            if sfv:
                sfvparsed = sfvparse(sfv)
            else:
                sfvparsed = False
        else:
            sfvparsed = False

        createepisodenames(title, directory, output,
                           seasonnum, episodenum, extension, sfvparsed)
        seasonnum += 1
        domakesfv = verifychanges(args.quiet, args.copy)

        if args.makesfv and domakesfv:
            makesfv(directory)

        episodes.clear()


def findsfv(src):
    sfvfiles = []
    for file in [x for x in os.listdir(src)
                 if os.path.splitext(x)[1] == ".sfv"]:
        sfvfiles.append(src + '/' + file)

    if sfvfiles:
        return sfvfiles[0]
    else:
        return False


def makecrc(filepath):
    f = open(filepath, 'rb')
    signedcrc = zlib.crc32(f.read()) % (1 << 32)
    f.close()
    return format(signedcrc, 'x')


def sfvparse(sfv):
    filelist = []
    f = open(sfv)
    for line in f:
        # parse for comments
        nocom = re.sub(r'\;.*', '', line)
        filelist.append(tuple(nocom.strip().rsplit(' ', 1)))

    f.close()
    return filelist


def makesfv(directory):
    f = open(directory + '/' + os.path.basename(directory) + '.sfv', 'w')

    for e in episodes:
        file = episodes[e]['new']['file']
        path = episodes[e]['new']['path']
        f.write(file + ' ' + makecrc(path + file) + '\n')

    f.close()


def crcvalidate(crc1, crc2):
    return (crc1.lower() == crc2.lower())


def makechanges(copy):
    for e in episodes:
        oldpath = episodes[e]['old']['path'] + episodes[e]['old']['file']
        newpath = episodes[e]['new']['path'] + episodes[e]['new']['file']

        if copy:
            print('Copying ' + episodes[e]['new']['file'])
            if not os.path.exists(episodes[e]['new']['path']):
                os.makedirs(episodes[e]['new']['path'])
            shutil.copy(oldpath, newpath)
        else:
            os.rename(oldpath, newpath)


def verifychanges(quiet, copy):
    while True:
        userinput = quiet or input('Write files? ((y)es, (n)o, (q)uit) ').lower()

        if userinput == 'y' or userinput is True:
            makechanges(copy)
            print('Done!')
            return True
        elif userinput == 'n':
            print('No changes made.\n')
            return False
        elif userinput == 'q':
            print('Exiting...')
            sys.exit()
        else:
            print('Please enter a valid option.')


def createepisodenames(title, src, dst, season,
                       episode, extension, sfv):
    for file in [x for x in os.listdir(src)
                 if not os.path.splitext(x)[0] in ignoredtypes
                 if not os.path.splitext(x)[1] in ignoredtypes
                 if not os.path.isdir(os.path.join(src, x))]:
        if extension:
            if extension[0] != '.':
                ext = '.' + extension
            else:
                ext = extension
        else:
            _, ext = os.path.splitext(file)

        newname = (title + ' - S{:02d}'.format(season) +
                   'E{:02d}'.format(episode) + ext)
        print(file + ' --> ' + newname)

        if sfv:
            for t in sfv:
                if file in t:
                    if crcvalidate(makecrc(src + '/' + file),
                                   t[1].strip('\n')):
                        print(GREEN + '[CRC Match]' + NC)
                    else:
                        print(RED + '[CRC Mismatch]' + NC)

        episodes[episode] = {'old': {'path': src + '/', 'file': file},
                             'new': {'path': dst + '/', 'file': newname}}
        episode += 1


if __name__ == '__main__':
    main()
