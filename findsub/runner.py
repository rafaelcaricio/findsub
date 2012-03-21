#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import getpass
import argparse
import logging as log
from xmlrpclib import ServerProxy

from utils import get_file_hash

OPENSUBTITLES_API_URL = 'http://api.opensubtitles.org/xml-rpc'
BAD_SUBTITLE = '1'


class FileFinder(object):

    def __init__(self, path_matcher):
        self.path_matcher = path_matcher

    def all_files(self):
        pass


class OpenSubtitlesClient(object):
    def __init__(self, username, password):
        self.opensubtitles = ServerProxy(OPENSUBTITLES_API_URL)
        response = self.opensubtitles.LogIn(username, password, 'en', 'OS Test User Agent') #'FindSub v1')
        if self.check_response(response):
            self.token = response['key']
            log.info('login success...')
        else:
            log.error('Bad login. Please check your username/password and try again [%s]' % response['status'])
            sys.exit(1)

    def check_response(self, response):
        return response['status'] == '200 OK'

    def search(self, language, file_hash):
        pass

    def find_subtitles(self, language, movie_files):
        pass


def download_file(remote_path):
    pass


def replace_extension_to(new_extension, complete_file_path):
    pass


def unzip_to(gzip_file, target_file, dest_file_path, replace=False):
    pass


def main():
    parser = argparse.ArgumentParser(description='Find the best subtitle from http://opensubtitles.org/ for you movies/series files.')
    parser.add_argument('file_matcher', metavar='FILE', type=str, nargs=1,
                        help='a file path or matcher indication where you files are located (ex: *.avi for all AVI files in current directory)')
    parser.add_argument('-u', dest='username', action='store', type=str, nargs=1,
                        help='indicate your username in opensubtitles site')
    parser.add_argument('-l', dest='language', action='store', type=str, nargs=1, default='all',
                        help='find subtitles for a specific language')
    parser.add_argument('--replace', dest='replace_all', action='store_true',
                        help='replace any subtitles with the same filename (default: not replace any subtitle file)')

    args = parser.parse_args()
    
    ost = OpenSubtitlesClient(args.username, getpass.getpass())
    movie_files = FileFinder(args.file_matcher)
    for movie_file, subtitles in ost.find_subtitles(args.language, movie_files.all_files()):
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
