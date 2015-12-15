##############
##  HEADER  ##
##############
# AUTHOR: Ollie O'Donnel & Zach Zeleznick
# DATE: December 2015
# COURSE: CS 194-26
# PROJECT: Video Supercuts
# FUNCTION: Testing Videocutting (Unused)

import re
import math
import os
import argparse
from subprocess import check_call, PIPE, Popen
import shlex

from utils import INPUT_FOLDER, OUTPUT_FOLDER, LOG_FILE
from utils import zprint, listVideoFiles, listOutputVideoFiles

def main():
    filename, split_length, offset, limit = parse_options()
    name, ext = filename.rsplit(".", 1)

    path = OUTPUT_FOLDER + name + '-' + str(split_length) + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    inputVideoPath = INPUT_FOLDER + filename

    if split_length <= 0:
        print("Split length can't be 0")
        raise SystemExit

    print("Reading file '%s' and splitting length of %d  " % (filename, split_length))

    p1 = Popen(["ffmpeg", "-i", inputVideoPath], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # get p1.stderr as input
    output = Popen(["grep", 'Duration'], stdin=p1.stderr, stdout=PIPE, universal_newlines=True)
    p1.stdout.close()
    info = output.stdout.read()
    # will be something like
    # Duration: 00:00:43.89, start: 0.000000, bitrate: 1148 kb/s
    re_length = re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,')
    matches = re_length.search(info)

    if matches:
        video_length = int(matches.group(1)) * 3600 + \
                       int(matches.group(2)) * 60 + \
                       int(matches.group(3))
        print("Video length in seconds: %d" % video_length )
    else:
        print("Can't determine video length.")
        raise SystemExit

    split_count = int(math.ceil(float(video_length - offset) / split_length))

    if limit:
        print('Trimming %d potential clips to %d' % (split_count, limit))
        split_count = min(split_count, limit)

    for n in range(split_count):
        split_start = split_length * n + offset
        timing = '%d-%d' % (split_start, min(split_start + split_length, video_length ))
        cmd = "ffmpeg -i {} -vcodec copy  -strict -2 -ss {} -t {} {}{}.{}".\
            format(inputVideoPath, split_start, split_length, path, timing, ext)
        print("About to run: {}".format(cmd))
        check_call(shlex.split(cmd), universal_newlines=True)

def parse_options():
    parser = argparse.ArgumentParser(
        description="Splits a video into chunks of length L as specified by the user and saves them to output/name",
        usage = "%(prog)s [-h] [-v] [Filename] [length] [-o offset] [-l limit]\n*Logs generated to log.txt * ",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= listVideoFiles() )

    parser.add_argument("filename",  metavar= 'v', nargs='?', default = None,
                        help='the video to split')
    parser.add_argument("length",  metavar= 'length', nargs='?', default = 10,
                        help='the length for each chunk')
    parser.add_argument("-o", "--offset", type = int, required = False, default = 0,
                        help='the seconds to offset the clip trimming')
    parser.add_argument("-l", "--limit",  dest='limit', type = int, required = False,
                        help='the max number of clips')
    parser.add_argument("-v", "--verbose", action="store_true",
                        required = False, default = False,
                        help='Displays all the output videos and exits if True')

    args = parser.parse_args()
    print args
    video  = args.filename
    length = int(args.length)
    offset = int(args.offset)
    limit = args.limit
    if not video:
        print("ERROR: Did not input value for video name")
        print listVideoFiles()
        exit()
    else:
        videoPath = INPUT_FOLDER + video

    if not os.path.isfile(videoPath):
        print("ERROR: File '%s' is not on path '%s'" % (video, INPUT_FOLDER) )
        print listVideoFiles()
        exit()

    if args.verbose:
        print listOutputVideoFiles()
        exit()

    if limit:
        limit = int(limit)

    return video, length, offset, limit

if __name__ == '__main__':
    main()