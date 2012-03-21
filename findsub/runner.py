#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getpass
import argparse
from pythonopensubtitles.opensubtitles import OpenSubtitles

BAD_SUBTITLE = '1'

class OpenSubtitlesClient(object):
    def __init__(self, username, password):
        pass

    def find_subtitles(self, movie_files):
        pass


def download_file(remote_path):
    pass


def replace_extension_to(new_extension, complete_file_path):
    pass


def unzip_to(gzip_file, target_file, dest_file_path, replace=False):
    pass


def main():
    parser = argparse.ArgumentParser(description='Find the best subtitle from http://opensubtitles.org/ for you movies/series files.')
    parser.add_argument('file_matcher', metavar='M', type=str, nargs=1, required=True,
                        help='a file path or matcher indication where you files are located (ex: *.avi for all AVI files in current directory)')
    parser.add_argument('-u', dest='username', action='store', type=str, nargs=1, required=True,
                        help='indicate your username in opensubtitles site')
    parser.add_argument('-l', dest='language', action='store', type=str, nargs=1, default='all',
                        help='find subtitles for a specific language')
    parser.add_argument('--replace', dest='replace_all', action='store_true',
                        help='replace any subtitles with the same filename (default: not replace any subtitle file)')

    args = parser.parse_args()
    
    ost = OpenSubtitlesClient(args.username, getpass.getpass())
    movie_files = FileFinder(args.file_matcher)
    for movie_file, subtitles in ost.find_subtitles(movie_files.all_files()):
        i = 0
        if subtitles:
            found_a_good_subtitle = False
            while not found_a_good_subtitle:
                if subtitles[i]['SubBad'] != BAD_SUBTITLE:
                    found_a_good_subtitle = True
                    subtitle = download_file(subtitles[i]['SubDownloadLink'])
                    subtitle_file_path = replace_extension_to(subtitles[i]['SubFormat'], movie_file.filename)
                    unzip_to(subtitle, subtitles[i]['SubFileName'], subtitle_file_path, replace=args.replace_all)
                    log.info('subtitle found for [%s]' % movie_file.filename)
                else:
                    i = 1 + i
        else:
            log.warn('can\'t find subtitle for file [%s]' % movie_file.filename)


if __name__ == '__main__':
    main()
