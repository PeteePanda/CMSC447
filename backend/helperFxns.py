import random

##### obfuscateLyrics(string, string, string, number between 0 and 1)

##### Takes input song lyrics, artist name, and song name as strings as
##### well as a number 0 - 1 indicating the percentage of words to be
##### obfuscated. 

##### Returns: Dictionary with songName, songArtist, songLyrics,
##### and the resulting obfuscatedLyrics. 

##### obfuscatedLyrics is an array of lyrics,
##### obfuscated ones replaced with an underscore (_)

def obfuscateLyrics(songLyrics, songName, songArtist, percentage):
    obfuscated_lyrics = []
    lyric_array = songLyrics.lower().split()
    name_array = songName.lower().split()
    artist_array = songArtist.lower().split()

    words_not_allowed = name_array + artist_array
    song_length = len(lyric_array)

    obfuscation_indexes = []
    counter = 0
    for lyric in lyric_array:
        if lyric in words_not_allowed:
            obfuscation_indexes.append(counter)
            counter += 1
            obfuscated_lyrics.append('_')
        else:
            obfuscated_lyrics.append(lyric)
            counter += 1
    
    plain_text_lyrics = set(range(song_length)) - set(obfuscation_indexes)
    remove = (percentage * song_length) - len(obfuscation_indexes)

    for x in range(round(remove)):
        random_index = random.choice(list(plain_text_lyrics))
        obfuscated_lyrics[random_index] = "_"
        plain_text_lyrics.remove(random_index)

    return {
        "songName": songName,
        "songArtist": songArtist,
        "songLyrics": songLyrics,
        "obfuscatedLyrics": obfuscated_lyrics
    }


