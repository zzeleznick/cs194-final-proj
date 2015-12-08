import re
import math
import os
import argparse
from subprocess import check_call, PIPE, Popen
import shlex

from utils import INPUT_FOLDER, OUTPUT_FOLDER, LOG_FILE, zprint

def main():
    filename, split_length = parse_options()
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

    split_count = int(math.ceil(float(video_length) / split_length))

    if split_count == 1:
        print("Video length is less than the target split length.")
        raise SystemExit

    for n in range(split_count):
        split_start = split_length * n
        cmd = "ffmpeg -i {} -vcodec copy  -strict -2 -ss {} -t {} {}{}.{}".\
            format(inputVideoPath, split_start, split_length, path, n, ext)
        print("About to run: {}".format(cmd))
        check_call(shlex.split(cmd), universal_newlines=True)

def listVideoFiles():
    fileNames = [f for f in os.listdir(INPUT_FOLDER) if f.upper().endswith('.MP4')]
    return 'Video Files: ' + ' | '.join(fileNames)

def listOutputVideoFiles():
    folders = [f for f in os.listdir(OUTPUT_FOLDER) if os.path.isdir(OUTPUT_FOLDER+f)]
    fileNames = []
    for folder in folders:
        names = []
        for f in os.listdir(OUTPUT_FOLDER+folder):
            if f.endswith('.mp4'):
                names.append(f[:f.index('.mp4')])
        fileNames.append(str(folder) + ': ' + ", ".join(names))
    return str(fileNames)

def parse_options():
    parser = argparse.ArgumentParser(
        description="Splits a video into chunks of length L as specified by the user and saves them to output/name",
        usage = "%(prog)s [-h] [-v] [Filename] [L]\n*Logs generated to log.txt * ",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= listVideoFiles() )

    parser.add_argument("filename",  metavar= 'v', nargs='?', default = None,
                        help='the video to split')
    parser.add_argument("length",  metavar= 'l', nargs='?', default = 10,
                        help='the length for each chunk')
    parser.add_argument("-v", "--verbose", action="store_true",
                        required = False, default = False,
                        help='Displays all the output videos and exits if True')

    args = parser.parse_args()
    print args
    video  = args.filename
    length = int(args.length)
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

    return video, length

if __name__ == '__main__':
    main()