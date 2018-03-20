#!/usr/bin/env python3

import os
import argparse
import json
from gmusicapi import Mobileclient

LIBRARY = 'gpm_library.json'
REMOVED = 'gpm_removed_songs.txt'


def touch_file(name):
    """
    Creates a file if it doesn't exist and returns a bool telling if the file
    existed.
    """
    if not os.path.exists(name):
        print(f'File \'{name}\' not found. Creating it.')
        with open(name, 'w'):
            pass
        return False
    return True


def file_read_json(filename):
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


def file_write_json(filename, container):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(container, file)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', action='store',
                        help='Stores username')
    parser.add_argument('password', action='store',
                        help='Stores password')
    return parser.parse_args()


def authenticate(username, password):
    api = Mobileclient()
    api.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
    return api


def get_songs(library):
    """Returns a new library of songs that only include artist, song, and album"""
    songs = []
    for song in library:
        title, artist, album = song['title'], song['artist'], song['album']
        seconds = int(song['durationMillis']) // 1000
        songs.append({'artist': artist, 'title': title, 'album': album, 'seconds': seconds})
    return songs


def write_removed_songs(removed_songs):
    removed_songs = sorted(removed_songs, key=lambda song: song['album'])
    with open(REMOVED, 'w', encoding='utf-8') as file:
        for song in removed_songs:
            title, artist, album, seconds = song['title'], song['artist'], song['album'], song['seconds']
            min, sec = seconds // 60, seconds % 60
            file.write(f'{artist} - {title} | {album} | {min}:{sec:02}\n')


def main():
    args = parse_args()
    username, password = args.username, args.password

    api = authenticate(username, password)
    library = api.get_all_songs()

    existed = touch_file(LIBRARY)

    new_songs = get_songs(library)
    if existed:
        old_songs = file_read_json(LIBRARY)
        removed_songs = [song for song in old_songs if song not in new_songs]

        print(str(len(removed_songs)) + ' ' + ('songs' if len(removed_songs) != 1 else 'song') + ' removed.')

        if len(removed_songs) > 0:
            touch_file(REMOVED)
            write_removed_songs(removed_songs)

    file_write_json(LIBRARY, new_songs)
    print('Updated library')


if __name__ == '__main__':
    main()
