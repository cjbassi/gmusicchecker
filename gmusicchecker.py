import os
import argparse
import json
from gmusicapi import Mobileclient


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
    return [{'artist': song['artist'], 'title': song['title'], 'album': song['album']} for song in library]


def write_removed_songs(removed_songs):
    removed_songs = sorted(removed_songs, key=lambda song: song['album'])
    with open('removed_songs.txt', 'w', encoding='utf-8') as file:
        for song in removed_songs:
            title, artist, album = song['title'], song['artist'], song['album']
            file.write(f'{artist} - {title} | {album}\n')


def main():
    args = parse_args()
    username, password = args.username, args.password

    api = authenticate(username, password)
    library = api.get_all_songs()

    existed = touch_file('library.json')

    new_songs = get_songs(library)
    if existed:
        old_songs = file_read_json('library.json')
        removed_songs = [song for song in old_songs if song not in new_songs]

        print(str(len(removed_songs)) + ' ' + ('songs' if len(removed_songs) != 1 else 'song') + ' removed.')

        if len(removed_songs) > 0:
            touch_file('removed_songs.txt')
            write_removed_songs(removed_songs)

    file_write_json('library.json', new_songs)
    print('Updated library')


if __name__ == '__main__':
    main()
