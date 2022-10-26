#!/usr/bin/env python3

import os

song_delim = '---'
inputdir = "/Users/davidogirala/git-repos/openlp_formatter/lyrics_text/"
outputdir = "/Users/davidogirala/git-repos/openlp_formatter/output/"
lyricsfiles = os.listdir("/Users/davidogirala/git-repos/openlp_formatter/lyrics_text")
songmap = {}


def song_text_is_same(song1, song2):
    return song1 == song2


def save_songs_to_file(songs):
    for song in songs:
        title = song[1].strip()

        # check for duplicate song

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


if __name__ == "__main__":
    main()
