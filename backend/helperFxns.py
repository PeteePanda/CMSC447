import random
import sqlite3


##### obfuscateLyrics(string, string, string, number between 0 and 1)

##### Takes input song lyrics, artist name, and song name as strings as
##### well as a number 0 - 1 indicating the percentage of words to be
##### obfuscated. 

##### Returns: Dictionary with songName, songArtist, songLyrics,
##### and the resulting obfuscatedLyrics. 

##### obfuscatedLyrics is an array of lyrics,
##### obfuscated ones replaced with an underscore '_'

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
            obfuscated_lyrics.append("_")
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


class Lyridactle_DB:
    def connect(self):
        try:
            return sqlite3.connect("data.db")
        except:
            print("Something went wrong connecting to DB.")

    def reset(self):
        try:
            delete_file = open("data.db", "w")
            delete_file.close()
            db = self.connect()
            create_song_table = """CREATE TABLE songs (
                songID INT NOT NULL,
                artist VARCHAR(255) NOT NULL,
                lyrics VARCHAR(255) NOT NULL,
                songName VARCHAR(255) NOT NULL,
                obfPattern VARCHAR(255) NOT NULL
            );"""
            create_leaderboard_table = """CREATE TABLE leaderboard (
                topFive VARCHAR(255)
            );"""
            create_user_table = """CREATE TABLE users (
                cookie VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                levelsUnlocked INT NOT NULL,
                savePoint VARCHAR(255) NOT NULL
            );"""

            db.execute(create_song_table)
            db.execute(create_leaderboard_table)
            db.execute(create_user_table)
            db.commit()
            print("Table reset.")
            return True
        except:
            print("Something went wrong with table reset.")
            return False
        
        finally:
            db.close()
    
    def addUser(self):
        return None

    def updateUser(self):
        return None
    
    def getUser(self):
        return None
    
    def getLeaderboard(self):
        return None
    
    def addSong(self):
        return None
    
    def updateSong(self):
        return None
    
    def getSong(self):
        return None
    
    def deleteUser(self):
        return None
        
    def getPoints(self):
        return None