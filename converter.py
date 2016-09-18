# -*- coding: utf-8 -*- #
"""
    Created on 18.09.16 by fashust
"""
import os
import shlex
from time import sleep
from subprocess import call
from threading import Thread


__author__ = 'fashust'
__email__ = 'fashust.nefor@gmail.com'


EXTENTION = '.cue'


def get_file(source_dir, ext=EXTENTION):
    """
    find cue file in source dir
    :param source_dir:
    :raise Exception
    :return:
    """
    for _file in os.listdir(source_dir):
        if _file.endswith(ext):
            return os.path.abspath(os.path.join(source_dir, _file))
    msg = '*.cue file not found in directory "{}"'.format(source_dir)
    raise Exception(msg)


def generate_commands(cue_file, ffmpeg_bin):
    """
    generate convert commands from cue file
    based on gist forked from
    https://gist.github.com/bancek/b37b780292540ed2d17d
    :param cue_file:
    :return:
    """
    general = {}
    tracks = []
    commands = []
    with open(cue_file) as _cue_file:
        file_data = _cue_file.read().splitlines()
        current_file = None
        for line in file_data:
            if line.startswith('REM GENRE '):
                general['genre'] = ' '.join(line.split(' ')[2:])
            if line.startswith('REM DATE '):
                general['date'] = ' '.join(line.split(' ')[2:])
            if line.startswith('PERFORMER '):
                general['artist'] = ' '.join(
                    line.split(' ')[1:]
                ).replace('"', '')
            if line.startswith('TITLE '):
                general['album'] = ' '.join(
                    line.split(' ')[1:]
                ).replace('"', '')
            if line.startswith('FILE '):
                current_file = ' '.join(line.split(' ')[1:-1]).replace('"', '')
            if line.startswith('  TRACK '):
                track = general.copy()
                track['track'] = int(line.strip().split(' ')[1], 10)
                tracks.append(track)
            if line.startswith('    TITLE '):
                tracks[-1]['title'] = ' '.join(
                    line.strip().split(' ')[1:]).replace('"', '')
            if line.startswith('    PERFORMER '):
                tracks[-1]['artist'] = ' '.join(
                    line.strip().split(' ')[1:]).replace('"', '')
            if line.startswith('    INDEX 01 '):
                t = list(map(
                    int,
                    ' '.join(
                        line.strip().split(' ')[2:]
                    ).replace('"', '').split(':')
                ))
                tracks[-1]['start'] = 60 * t[0] + t[1] + t[2] / 100.0
        for i in range(len(tracks)):
            if i != len(tracks) - 1:
                tracks[i]['duration'] = (
                    tracks[i + 1]['start'] - tracks[i]['start']
                )
        for track in tracks:
            metadata = {
                'artist': track['artist'],
                'title': track['title'],
                'album': track['album'],
                'track': str(track['track']) + '/' + str(len(tracks))
            }

            if 'genre' in track:
                metadata['genre'] = track['genre']
            if 'date' in track:
                metadata['date'] = track['date']

            cmd = ffmpeg_bin
            cmd += ' -b:a 320k'
            cmd += ' -i "%s"' % current_file
            cmd += ' -ss %.2d:%.2d:%.2d' % (
                track['start'] / 60 / 60, track['start'] / 60 % 60,
                int(track['start'] % 60)
            )

            if 'duration' in track:
                cmd += ' -t %.2d:%.2d:%.2d' % (
                    track['duration'] / 60 / 60, track['duration'] / 60 % 60,
                    int(track['duration'] % 60)
                )

            cmd += ' ' + ' '.join(
                '-metadata %s="%s"' % (k, v) for (k, v) in metadata.items()
            )
            cmd += ' "%.2d - %s - %s.mp3"' % (
                track['track'], track['artist'], track['title']
            )
            commands.append(cmd)
    return commands


def run_command(command, source_dir):
    """
    excute convert command
    :param source_dir:
    :param command:
    :return:
    """
    command = command.replace('""', '"')
    os.chdir(os.path.abspath(source_dir))
    call(shlex.split(command))


def convert(source_dir, ffmpeg_bin):
    """
    converter
    """
    cue_file = get_file(source_dir)
    commands = generate_commands(cue_file, ffmpeg_bin)
    running_commands = []
    for command in commands:
        job = Thread(target=run_command, args=(command, source_dir))
        job.start()
        running_commands.append(job)
    return running_commands


def delete_original(source_dir, running_commands, is_deleted=False):
    """
    delete original files
    :param source_dir:
    :return:
    """
    def is_all_finished():
        return not all(map(lambda _: _.isAlive(), running_commands))

    if not is_all_finished():
        sleep(5)
        delete_original(source_dir, running_commands, is_deleted)
    elif is_deleted:
        return
    else:
        for ext in [EXTENTION, '.flac']:
            os.remove(get_file(source_dir, ext))
        return
