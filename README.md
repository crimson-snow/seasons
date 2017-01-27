# rename-TV
Rename many TV show episodes for Plex at once

## Installation
UNIX (Linux, macOS, BSD)
```bash
sudo curl -L https://raw.githubusercontent.com/t-sullivan/rename-TV/master/renametv -o /usr/local/bin/renametv
sudo chmod a+rx /usr/local/bin/renametv
```

## Usage
```bash
renametv [OPTIONS] TITLE [DIR [DIR ...]]
```

### Arguments
```
TITLE                 define a TV show title
DIR                   define a working directory
```
The current working directory is the default input and output location if DIR is not supplied.

### Options
```
-h, --help            show this help message and exit
-c, --copy            copy files to output location
-e EXTENSION, --extension EXTENSION
                      only rename files with specified extension
-E EPISODESTART, --episodestart EPISODESTART
                      specify the starting episode number
-m, --makesfv         create an sfv file for each DIR
-o OUTPUT, --output OUTPUT
                      define an output location
-q, --quiet           surpress prompts and proceed with writing files
-r SFV, --readsfv SFV
                      specify an sfv file to verify files
-s SEASONSTART, --seasonstart SEASONSTART
                      specify the starting season number
--version             show program's version number and exit
```

### Example Input
**Renaming multiple seasons of a series**

Consider the scenario in which we have multiple seasons of a series that we need to rename. To do this in a single command, we need each season in it's own respective directory.

Let's say our file structure looks like this:
```
Game of Thrones (working directory)
│
└───Season 01
│   │   got101.mp4
│   │   got102.mp4
│   │   got103.mp4
		...
│
└───Season 02
    │   got201.mp4
    │   got202.mp4
    ...
```

We run our command:
```bash
renametv -e mp4 'Game of Thrones' 'Season 01' 'Season 02'
```

The resulting file structure will look like this:
```
Game of Thrones (working directory)
│
└───Season 01
│   │   Game of Thrones - S01E01.mp4
│   │   Game of Thrones - S01E02.mp4
│   │   Game of Thrones - S01E03.mp4
		...
│
└───Season 02
    │   Game of Thrones - S02E01.mp4
    │   Game of Thrones - S02E02.mp4
		...
```

**Copying files to a new directory**

Consider the scenario where we have several .mkv files in our current working directory. We want to rename every .mkv file in a format that Plex likes, but also copy the files to ```~/TV Shows/Yu Yu Hakusho/Season 04``` which is an appropriate place in our media library.

1. We define our output location with the 'output' flag (If this location does not exist, it will be created).
2. Since we want the files to be copied to a new location we denote that with the 'copy' flag.
3. We only want .mkv files for this scenario and we indicate so with the 'extension' flag.
4. These episodes happen to be in season 4 of the series, so we can specify that with the 'seasonstart' flag.
5. Finally we have our only required argument, the show title. In this case 'Yu Yu Hakusho'.

```bash
renametv -o '~/TV Shows/Yu Yu Hakusho/Season 04' -c -e mkv -s 4 'Yu Yu Hakusho'
```

### Example Output
Any proposed changes will be displayed with a prompt to proceed with renaming or to exit without saving.

```
Yu Yu Hakusho 095.mkv --> Yu Yu Hakusho - S04E01.mkv
Yu Yu Hakusho 096.mkv --> Yu Yu Hakusho - S04E02.mkv
Yu Yu Hakusho 097.mkv --> Yu Yu Hakusho - S04E03.mkv
Yu Yu Hakusho 098.mkv --> Yu Yu Hakusho - S04E04.mkv
...
Write files? (y/n)
```