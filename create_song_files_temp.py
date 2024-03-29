#!/usr/bin/env python3

import os

song_delim = '---'
inputdir = "lyrics_text/"
outputdir = "output/"
lyricsfiles = os.listdir("lyrics_text")
songmap = {}
dups = 0


def song_already_exists(song, title):
    global dups
    # check for duplicate song
    if title not in songmap:
        return False

    n = songmap[title]

    for i in range(1, n + 1):
        suffix = f"_{n}" if n > 1 else ""
        filename = f"{outputdir}{title}{suffix}.txt"
        with open(filename, 'r', encoding='utf-8') as songfile:
            songtext = songfile.readlines()
            if songtext == song:
                dups = dups + 1
                return True

    return False


def save_songs_to_file(songs):
    for song in songs:
        title = song[1].strip()

        # check for duplicate song
        if song_already_exists(song, title):
            continue

        songmap[title] = songmap.get(title, 0) + 1

        suffix = f"_{songmap[title]}" if songmap[title] > 1 else ""
        with open(f"{outputdir}{title}{suffix}.txt", 'w', encoding='utf-8') as song_file:
            song_file.writelines(song)


def main():
    # list file names
    for file in lyricsfiles:
        if not file.endswith('.txt'):
            continue

        # open txt file
        with open(inputdir + file, 'r', encoding='utf-8') as lyricfile:
            print(f"Reading {file}...")

            songs = []
            song = None
            for line in lyricfile.readlines():
                if line.startswith(song_delim):
                    if song:
                        songs.append(song)
                    song = []
                song.append(line)

            save_songs_to_file(songs)

    print('Done')
    print(f'Total Duplicates: {dups}')


if __name__ == "__main__":
    main()
