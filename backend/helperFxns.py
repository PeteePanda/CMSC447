from email import header
import json
import random
import sqlite3
import re
import os
import requests
from dotenv import load_dotenv
import lyricsgenius



load_dotenv()

class SavePoint:
    def __init__(self, wordsUsed, id, currentLevel):
        self.wordsUsed = wordsUsed
        self.songID = id
        self.currentLevel = currentLevel
    
    def json(self):
        return ({
            "wordsUsed": self.wordsUsed,
            "songID": self.songID,
            "currentLevel": self.currentLevel
        })

class User:
    def __init__(self, cookie, name, lvlsUnlocked, save):
        self.id = cookie
        self.name = name
        self.unlocked = lvlsUnlocked
        self.savePoint = save
    def json(self):
        return ({
            "id": self.id,
            "name": self.name,
            "levelsUnlocked": self.unlocked,
            "savePoint": self.savePoint
        })

        
class Song:
    def __init__(self, songID, artist, lyrics, name, obfEasy, obfMedium, obfHard):
        self.id = songID
        self.artist = artist
        self.lyrics = lyrics
        self.name = name
        self.obfPatterns = {"easy": obfEasy, "medium": obfMedium, "hard": obfHard}

    def json(self):
        return ({
            "id": self.id,
            "artist": self.artist,
            "name": self.name,
            "lyrics": self.lyrics,
            "obfPatterns": self.obfPatterns
        })


class Lyridact_DB:
    def __init__(self, PATH_TO_DB):
        self.DBpath = PATH_TO_DB

    def connect(self):
        try:
            return sqlite3.connect(self.DBpath)
        except:
            print("Something went wrong connecting to DB.")

    def reset(self):
        try:
            delete_file = open(self.DBpath, "w")
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
                user VARCHAR(255),
                points INT NOT NULL
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

##### obfuscateLyrics(string, string, string, number between 0 and 1)
#####
##### Takes input song lyrics, artist name, and song name as strings as
##### well as a number 0 - 1 indicating the percentage of words to be
##### obfuscated. 
#####
##### Returns: Dictionary with songName, songArtist, songLyrics,
##### percentage obfuscated, and the resulting obfuscatedLyrics.
#####
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
        if (re.search("\[[\w]*\]", lyric) != None):
            obfuscation_indexes.append(counter)
            counter += 1
            obfuscated_lyrics.append("~")
        elif lyric in words_not_allowed:
            obfuscation_indexes.append(counter)
            counter += 1
            size = len(lyric)
            obfuscated_lyrics.append(("_"*size))
        else:
            obfuscated_lyrics.append(lyric)
            counter += 1
    
    plain_text_lyrics = set(range(song_length)) - set(obfuscation_indexes)
    remove = (percentage * song_length) - len(obfuscation_indexes)

    for x in range(round(remove)):
        plain_lyrics = list(plain_text_lyrics)
        random_index = random.choice(plain_lyrics)     
        size = len(lyric_array[random_index])
        obfuscated_lyrics[random_index] = ("_"*size)
        plain_text_lyrics.remove(random_index)

    return obfuscated_lyrics



def create_song(songLyrics, songName, songArtist, songID):
    easy = obfuscateLyrics(songLyrics, songName, songArtist, .2)
    medium = obfuscateLyrics(songLyrics, songName, songArtist, .5)
    hard = obfuscateLyrics(songLyrics, songName, songArtist, .7)
    return(Song(songID, songArtist, songLyrics, songName, easy, medium, hard))

def getSpotifyAccessToken():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get('SPOTIFY_CLIENT_ID'),
        "client_secret": os.environ.get('SPOTIFY_SECRET'),
    }
    res = requests.post(url, headers=headers, data=data)    

    if res.status_code == 200:
        
        return res.json()["access_token"]
    else:
        return None

def getTop50():
    topFifty = []
    playlist_id = "37i9dQZEVXbLp5XoPON0wI"
    url = "https://api.spotify.com/v1/playlists/" + playlist_id
    access_token = getSpotifyAccessToken()
    if access_token == None:
        return None
    headers = {
        'Authorization': "Bearer " + access_token, 
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()["tracks"]["items"]
        for item in data:
            singers = []
            artists = item["track"]["artists"]
            for artist in artists:
                singerName = artist["name"]
                singers.append(singerName)
            name = item["track"]["name"]
            topFifty.append((name, singers))

        
        return topFifty
    else:
        return None


def getLyrics(songName, songArtists):
    regex = r'[^a-zA-Z0-9\s]'
    name = re.sub(regex, '', songName.lower())
    artist = re.sub(regex, '', songArtists[0].lower())
    query = f'{name} {artist}'
    url = f"https://api.genius.com/search?q=" + re.sub(" ", "%20", query)
   
    access_token = os.environ.get("GENIUS_API_KEY")
    headers = {
        'Authorization': "Bearer " + access_token 
    }
    res = requests.get(url, headers=headers)
    data = json.loads(res.text)
    song_id = data["response"]["hits"][0]["result"]["id"]
    genius = lyricsgenius.Genius(access_token)
    lyrics = genius.lyrics(int(song_id))
    start = lyrics.find('[')
    clean_lyrics = lyrics[start:-7]


    return clean_lyrics
    

