# rename-tv-plex
Rename TV shows seasons at a time in a Plex suitable naming convention

## Usage
```
./renametv.py directory "Name of Series" seasonNumber [EpisodeStart] [FileExtentison]
```

### Example Input
```
./renametv.py "~/Media/TV Shows/Yu Yu Hakusho/Season 04" "Yu Yu Hakusho" 4 mkv
```

### Example Output
Any proposed changes will be displayed with a prompt to proceed with renaming or to exit without saving.

```
Yu Yu Hakusho 095.mkv --> Yu Yu Hakusho - S04E01.mkv
Yu Yu Hakusho 096.mkv --> Yu Yu Hakusho - S04E02.mkv
Yu Yu Hakusho 097.mkv --> Yu Yu Hakusho - S04E03.mkv
Yu Yu Hakusho 098.mkv --> Yu Yu Hakusho - S04E04.mkv
...
Rename files? (y/n)
```