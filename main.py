# -*- coding: utf-8 -*- #
"""
    Created on 17.09.16 by fashust
"""
from options import parse_options, check_options
from converter import delete_original, convert


__author__ = 'fashust'
__email__ = 'fashust.nefor@gmail.com'


def run(source_dir, ffmpeg_bin, delete):
    """
    main entry point for script
    :return:
    """
    running = convert(source_dir, ffmpeg_bin)
    if delete:
        delete_original(source_dir, running)


if __name__ == '__main__':
    parser = parse_options()
    options, args = parser.parse_args()
    options = check_options(options)
    run(**options)
