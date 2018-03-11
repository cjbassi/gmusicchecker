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
        print(f'File \'{name}\' not found. Creating a new one.')
        with open(name, 'w'):
            pass
        return False
    return True


def get_old_songs():
    with open('library.txt', encoding='utf-8') as file:
        return [line.strip() for line in file]


def get_new_songs(library):
    new_songs = []
    for song in library:
        title, artist, album, id = song['title'], song['artist'], song['album'], song['id']
        new_songs.append(f'{artist} - {title} | ALBUM: {album} | ID: {id}')
    return new_songs


def compare(old, new):
    """
    Compares old library with new library and prints the differences.
    Returns a bool telling if the songs are different.
    """
    changed = False

    print('Checking missing songs:')
    for song in old:
        if song not in new:
            changed = True
            print('missing song: ' + song)

    print('-' * 10 + '\nChecking newly added songs:')
    for song in new:
        if song not in old:
            changed = True
            print('new song added: ' + song)

    return changed


def update(new_songs):
    """Overwrites 'library.txt' with new library"""
    with open('library.txt', 'w', encoding='utf-8') as file:
        for song in new_songs:
            file.write(song + '\n')


def main():
    args = parse_args()
    username, password = args.username, args.password

    api = authenticate(username, password)
    library = api.get_all_songs()

    existed = touch_file('library.txt')

    old_songs = get_old_songs()
    new_songs = get_new_songs(library)

    changed = compare(old_songs, new_songs)

    if changed:
        if existed:
            print('-' * 10 + '\nUpdate library? [y/n] ')
            update_library = input()
            if update_library == 'y':
                update(new_songs)
                print('Finished updating library!')
            else:
                print('Done!')
        else:
            update(new_songs)
            print('-' * 10 + '\nFinished updating library!')
    else:
        print('-' * 10 + '\nNothing changed. Done!')


if __name__ == '__main__':
    main()
