import os
import argparse
from gmusicapi import Mobileclient


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


def file_read_array(filename):
    """Reads each line of a file into an array."""
    with open(filename, encoding='utf-8') as file:
        return [line.strip() for line in file]


def get_songs(library):
    new_songs = []
    for song in library:
        title, artist, album, id = song['title'], song['artist'], song['album'], song['id']
        new_songs.append(f'{artist} - {title} | ALBUM: {album} | ID: {id}')
    return new_songs


def file_write_array(filename, array):
    """
    Clears a file, then writes each item item of the array as a line in the
    file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for i in array:
            file.write(i + '\n')


def main():
    args = parse_args()
    username, password = args.username, args.password

    api = authenticate(username, password)
    library = api.get_all_songs()

    touch_file('library.txt')

    old_songs = file_read_array('library.txt')
    new_songs = get_songs(library)
    removed_songs = [song for song in old_songs if song not in new_songs]

    print(str(len(removed_songs)) + ' ' + ('songs' if len(removed_songs) != 1 else 'song') + ' removed.')

    if len(removed_songs) > 0:
        touch_file('removed_songs.txt')
        file_write_array('removed_songs.txt', removed_songs)

    file_write_array('library.txt', new_songs)


if __name__ == '__main__':
    main()
