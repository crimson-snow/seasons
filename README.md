# seasons

<img src="assets/img/readme/seasons_logo.png" width="100%" />
A lightweight organization tool for your media library

## Installation
```bash
sudo curl -L https://raw.githubusercontent.com/t-sullivan/seasons/master/seasons.py
```

## Usage
```bash
python3 seasons.py [OPTIONS] TITLE [DIR [DIR ...]]
```

### Arguments
```
TITLE                 specify a TV show title
DIR                   specify source directories
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
-q, --quiet           surpress prompts and proceed with writing files
-s SEASONSTART, --seasonstart SEASONSTART
                      specify the starting season number
-S SCHEME, --scheme SCHEME
                      define a custom episode naming scheme
-v, --verbose         display file paths in full
--version             show program's version number and exit
```

## Examples of Use
### Renaming multiple seasons of a series

Consider the scenario in which we have multiple seasons of a series that we need to rename.

Let's say our file structure looks like this:
```
Game of Thrones (working directory)
│
└───S01
│   │   got101.mp4
│   │   got102.mp4
│   │   got103.mp4
|       ...
│
└───S02
    │   got201.mp4
    │   got202.mp4
    |   got203.mp4
        ...
```

We run our command:
```bash
python3 seasons.py 'Game of Thrones' S01 S02
```

The resulting file structure will look like this:
```
Game of Thrones (working directory)
│
└───Season 01
│   │   Game of Thrones - S01E01.mp4
│   │   Game of Thrones - S01E02.mp4
│   │   Game of Thrones - S01E03.mp4
|       ...
│
└───Season 02
    │   Game of Thrones - S02E01.mp4
    │   Game of Thrones - S02E02.mp4
    |   Game of Thrones - S02E03.mp4
        ...
```

### Copying files to a new directory

Consider the scenario where we have several .mkv files in our current working directory. We want to copy the files to ```B``` where Plex will be able to find the content and add it to our media library.

1. We define our output location with the `--output` option. If this location does not exist, it will be created.
2. Since we want the files to be copied to a new location and not moved, we denote that with the `--copy` option.
4. The episodes used in this example start at 105 and we can specify that with the `--episodestart` option.
5. Next we input our desired show title. In this case `'Dragon Ball Super'`.
6. Finally we have our source directory `A`.

```bash
python3 seasons.py -o B/ -c -e 105 'Dragon Ball Super' A/
```

Any proposed changes will be displayed with a prompt to proceed with renaming or to exit without saving.

```
[COPY] from [A/Dragon Ball Super - 105 [1080p].mkv] to [B/Season 01/Dragon Ball Super - S01E105.mkv]
[COPY] from [A/Dragon Ball Super - 106 [1080p].mkv] to [B/Season 01/Dragon Ball Super - S01E106.mkv]
[COPY] from [A/Dragon Ball Super - 107 [1080p].mkv] to [B/Season 01/Dragon Ball Super - S01E107.mkv]
[COPY] from [A/Dragon Ball Super - 108 [1080p].mkv] to [B/Season 01/Dragon Ball Super - S01E108.mkv]
...
Write files? [(y)es, (n)o, (q)uit]
```

### Custom Naming Scheme

You have the option to define an episode naming scheme to your liking using variables for series title, season number, and episode number.

|Variable   	|Description   	        |Result   	        |
|---	        |---	                |---	            |
|`{t}`   	    |Series title   	    |"Example Title"    |
|`{t.dot}`   	|Series title with dots |"Example.Title"    |
|`{s}`  	    |Season #   	        |"1"   	            |
|`{e}`   	    |Episode #   	        |"03"  	            |

```bash
python3 seasons.py -S '{t.dot}.{s}{e}' -o B/ -c 'Dragon Ball Super' A/
```

```
[COPY] from [A/Dragon Ball Super - 01 [1080p].mkv] to [B/Season 01/Dragon.Ball.Super.101.mkv]
[COPY] from [A/Dragon Ball Super - 02 [1080p].mkv] to [B/Season 01/Dragon.Ball.Super.102.mkv]
[COPY] from [A/Dragon Ball Super - 03 [1080p].mkv] to [B/Season 01/Dragon.Ball.Super.103.mkv]
[COPY] from [A/Dragon Ball Super - 04 [1080p].mkv] to [B/Season 01/Dragon.Ball.Super.104.mkv]
...
Write files? [(y)es, (n)o, (q)uit]
```