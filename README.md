# rename-TV
A lightweight organization tool for your media library

## Installation
UNIX (Linux, macOS, BSD)
```bash
sudo curl -L https://raw.githubusercontent.com/t-sullivan/rename-TV/develop/renametv.py -o ~/Desktop
```

## Usage
```bash
python3 renametv.py [OPTIONS] TITLE [DIR [DIR ...]]
```

### Arguments
```
TITLE                 specify a TV show title
DIR                   specify a source directories
```
The current working directory is the default input and output location if DIR is not supplied.

### Options
```
-h, --help            show this help message and exit
-c, --copy            copy files to output location
-e EPISODESTART, --episodestart EPISODESTART
                      specify the starting episode number
-o OUTPUT, --output OUTPUT
                      specify an output location
-q, --quiet           suppress prompts and proceed with writing files
-s SEASONSTART, --seasonstart SEASONSTART
                      specify the starting season number
--version             show program's version number and exit
```

### Examples of Use
**Renaming multiple seasons of a series**

Consider the scenario in which we have multiple seasons of a series that we need to rename.

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
python3 renametv.py 'Game of Thrones' Season\ 01 Season\ 02 -o .
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
        Game of Thrones - S02E03.mp4
		...
```

**Copying files to a new directory**

Consider the scenario where we have several .mkv files in our current working directory. We want to copy the files to ```Media/TV Shows/Dragon Ball Super``` where Plex will be able to find the content and add it to our media library.

1. We define our output location with the 'output' flag. If this location does not exist, it will be created.
2. Since we want the files to be copied to a new location and not moved, we denote that with the 'copy' flag.
4. The episodes used in this example start at 105 and we can specify that with the 'episodestart' flag.
5. Next we input our desired show title. In this case 'Dragon Ball Super'.
6. Finally we have our source directory 'DBS'.

```bash
python3 renametv.py -o 'Media/TV Shows/Dragon Ball Super' -c -e 105 'Dragon Ball Super' DBS
```

### Example Output
Any proposed changes will be displayed with a prompt to proceed with renaming or to exit without saving.

```
[MOVE] from [DBS/Dragon Ball Super - 105 [1080p].mkv] to [Media/TV Shows/Dragon Ball Super/Season 01/Dragon Ball Super - S01E105.mkv]
[MOVE] from [DBS/Dragon Ball Super - 106 [1080p].mkv] to [Media/TV Shows/Dragon Ball Super/Season 01/Dragon Ball Super - S01E106.mkv]
[MOVE] from [DBS/Dragon Ball Super - 107 [1080p].mkv] to [Media/TV Shows/Dragon Ball Super/Season 01/Dragon Ball Super - S01E107.mkv]
[MOVE] from [DBS/Dragon Ball Super - 108 [1080p].mkv] to [Media/TV Shows/Dragon Ball Super/Season 01/Dragon Ball Super - S01E108.mkv]
...
Write files? [(y)es, (n)o, (q)uit]
```