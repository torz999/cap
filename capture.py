import os
import sys
import fnmatch

import ffmpeg_streaming as stream
import colorama as c

from datetime import date, timedelta


def displayInformation(info):
    data = stream.FFProbe(info[0])
    form = data.format()

    name = c.Fore.WHITE + c.Style.BRIGHT + "Model: " + \
        c.Fore.CYAN + c.Style.BRIGHT + "{}".format(info[1])
    time = c.Fore.WHITE + c.Style.BRIGHT + "Duration: " + c.Fore.CYAN + \
        c.Style.BRIGHT + \
        "{}".format(str(timedelta(seconds=float(form.get('duration', 0)))))
    file = c.Fore.WHITE + c.Style.BRIGHT + "File: " + \
        c.Fore.CYAN + c.Style.BRIGHT + "{}".format(info[2])
    size = c.Fore.WHITE + c.Style.BRIGHT + "Size: " + \
        c.Fore.CYAN + c.Style.BRIGHT + \
        "{} MB".format(form.get('size', 0) / 1024)

    print('{}\n{}\n{}\n{}\n'.format(name, time, file, size), end='\r')


def getFileInstance(filePath, fileName):
    count = 0
    targets = '{}*.mp4'.format(fileName)
    contents = os.listdir(filePath)

    for content in contents:
        if fnmatch.fnmatch(content, targets):
            count += 1

    return count + 1


def main():
    c.init()

    if len(sys.argv) < 2:
        error = c.Fore.RED + c.Style.BRIGHT + ''' Please specify a models name:
                              - Usage: {0} <username> <serverid> <modelid> <appmode>
                              - Examples: {0} Reige 401 34377471 app
                              - Examples: {0} Reige 401 34377471 std'''.format(sys.argv[0])

        print(error)
        sys.exit(0)
    else:
        urlPath = None

        if sys.argv[4] == 'app':
            urlPath = "https://video{}.myfreecams.com/NxServer/ngrp:mfc_a_1{}.f4v_cmaf/playlist_sfm4s.m3u8".format(
                sys.argv[2], sys.argv[3])
        elif sys.argv[4] == 'std':
            urlPath = "https://video{}.myfreecams.com/NxServer/ngrp:mfc_1{}.f4v_cmaf/playlist_sfm4s.m3u8".format(
                sys.argv[2], sys.argv[3])
        else:
            print('Please specify a valid appmode')
            sys.exit(0)

        modelDirectory = "./recordings/{}".format(sys.argv[1])

        if not os.path.exists(modelDirectory):
            os.mkdir(modelDirectory)

        fileBase = '{} - {} - P'.format(sys.argv[1], date.today())
        fileInst = getFileInstance(modelDirectory, fileBase)
        fileName = "{}{}.mp4".format(fileBase, str(fileInst))
        filePath = '{}/{}'.format(modelDirectory, fileName)

        video = stream.input(urlPath)

        hls = video.stream2file(stream.Formats.h264())
        hls.output(filePath)

        print(c.Fore.GREEN + c.Style.BRIGHT + 'Stream Complete!')


if __name__ == "__main__":
    main()
