#  CS194-26: Video Scripting (Final Project)

## Main Files

1. main.py          Generates output video

## Helper Files

1. utils.py         Contains useful functions called by main.py and others


## Project Contents

| Directories | Subfolders| Description |
| ----------- | --------- | ----------- |
| data/       |           | video directory |
|             | base      | mvp video       |
|             | test      | test videos     |
| output/     |           | directory for output to be saved  |


## Utilities

#### YouTube MP4 and .SRT Downloader
https://github.com/rg3/youtube-dl/

- e.g. youtube-dl --write-srt --srt-lang en https://www.youtube.com/watch?v=yca-uwxCsWg
- note: for github we need to rescale > ffmpeg -i video.mp4 -s 720x480 -c:a copy output.mp4

## Video Sources


| Name        | Title       | Duration  | Link        |
| ----------- | ----------- | --------- | ----------- |
| Obama-African-Union | Obama Speaks To African Union   |   48:24        | https://youtu.be/z9g5-46Lww8 |
|2 | Which Major? - Intro to Descriptive Statistics  |   00:43        | https://youtu.be/mIzPoh_kqw4 |
|3 | The President Delivers a Statement on the Shooting in Oregon | 12:44 |https://youtu.be/yca-uwxCsWg|