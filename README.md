# rename-TV
Rename many TV show episodes for Plex at once

## Installation
UNIX (Linux, macOS, BSD)
'''
sudo curl -L https://raw.githubusercontent.com/t-sullivan/rename-TV/master/renametv -o /usr/local/bin/renametv
sudo chmod a+rx /usr/local/bin/renametv
'''

## Usage
```
renametv [OPTIONS] TITLE [DIR [DIR ...]]
```

### Arguments
'''
TITLE                 define a TV show title
DIR                   define a working directory
'''

### Options
'''
-h, --help            show this help message and exit
-c, --copy            copy files to output location
-e EXTENSION, --extension EXTENSION
                      only rename files with specified extension
-E EPISODESTART, --episodestart EPISODESTART
                      specify the starting episode number
-o OUTPUT, --output OUTPUT
                      define an output location
-q, --quiet           surpress prompts and proceed with writing files
-s SEASONSTART, --seasonstart SEASONSTART
                      specify the starting season number
--version             show program's version number and exit
'''

### Example Input
Copying files to a new directory
```
renametv -o "~/TV Shows/Yu Yu Hakusho/Season 04" -c -e mkv -s 4 'Yu Yu Hakusho'
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