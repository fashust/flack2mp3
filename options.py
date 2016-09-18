# -*- coding: utf-8 -*- #
"""
    Created on 17.09.16 by fashust
"""
import sys
from optparse import OptionParser


__author__ = 'fashust'
__email__ = 'fashust.nefor@gmail.com'


OPTIONS = {
    'source_dir': ('-s', '--source'),
    'ffmpeg_bin': ('-f', '--ffmpeg'),
    'delete': ('-d', '--delete')
}


def parse_options():
    """
    converter command line options
    :return:
    """
    parser = OptionParser()
    parser.add_option(
        *OPTIONS['source_dir'],
        action="store",
        type=str,
        dest='source_dir',
        help=(
            'Source directory, which will contain '
            'source *.cue and *.flack files'
        )
    )
    parser.add_option(
        *OPTIONS['ffmpeg_bin'],
        action="store",
        type=str,
        dest='ffmpeg_bin',
        help='full path to ffmpeg binary'
    )
    parser.add_option(
        *OPTIONS['delete'],
        dest='delete',
        action='store_true',
        default=False,
        help='Delete source *.cue and *.flac files, Default = False'
    )
    return parser


def check_options(options):
    """
    check passed options
    :param options:
    :return:
    """
    opts = {}
    for key in OPTIONS.keys():
        val = getattr(options, key, None)
        if key != 'delete':
            if not val:
                msg = (
                    'Value for {} is required\n'
                    'For more detail run "./main.py --help"'
                ).format(key)
                sys.exit(msg)
        opts[key] = val
    return opts
