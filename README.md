#  CS194-26: Video Supercuts (Final Project)

## Main Files
-  main.py          Generates output video

## Configuration
- config.py         Environmental variables called by our program methods

## Utilities
- utils.py          Contains useful functions called by main.py and others

## Classes
- classes.py        Class File for Subtitle Schema

## Project Contents

| Directories | Subfolders| Description |
| ----------- | --------- | ----------- |
| data/       |           | video and subtitle directory |
| output/     |           | directory for output to be saved  |


## Project Summary:

#### Dynamically creates a supercut from a video and subtitle pairing where the keyword(s) of interest are spoken

```
> usage: main.py [-h] [-v] [-p | -w | -s] [videoName] [keywords]

# positional arguments:
#   videoName   The name of the video to process
#   keywords    The words to find in the video

# optional arguments:
#   -h, --help     show this help message and exit
#   -v, --verbose  Displays the phrases that contain the keyword(s) if True
#   -p, --phrase   Captures the entire phrase
#   -w, --word     Refines the bounds to include just the word
#   -s, --speech   Creates a fake speech from the keywords
```


## External Utilities

#### YouTube MP4 and .SRT Downloader
https://github.com/rg3/youtube-dl/

- e.g. youtube-dl --write-srt --srt-lang en https://www.youtube.com/watch?v=yca-uwxCsWg
- note: for github we need to rescale > ffmpeg -i video.mp4 -s 720x480 -c:a copy output.mp4


## Video Sources
| Name        | Title       | Duration  | Link        |
| ----------- | ----------- | --------- | ----------- |
| 1 | President Obama Delivers An Address To The Nation Dec. 6th 2015  | 13:09 |https://youtu.be/TMDV3VY0tPA|
|2 | Donald Trump: 'We Are Not Loved By Many Muslims' MSNBC  |   21:34       | https://youtu.be/NMYeVasogH4 |
|3 | The President Delivers a Statement on the Shooting in Oregon | 12:44 |https://youtu.be/yca-uwxCsWg|