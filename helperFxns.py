import json
import random
import sqlite3
import re
import os
import requests
from dotenv import load_dotenv
import lyricsgenius
from datetime import datetime
import string

load_dotenv()

def generateCookie():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(20))


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

def obfuscateLyrics(songLyrics, songName, songArtists, percentage):
    obfuscated_lyrics = []
    lyric_array = sanitizeLyics(songLyrics,songName)
    
    name_array = songName.lower().split()
    artist_array = []
    for artist in songArtists:
        artist = artist.lower().split()
        artist_array += artist
    
    words_not_allowed = name_array + artist_array
    song_length = len(lyric_array)
    obfuscation_indexes = []

    counter = 0
    for lyric in lyric_array:
        
        if lyric in words_not_allowed:
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

def sanitizeLyics(songLyrics,songName):

    # Split the text using the regular expression pattern
    nospaces = songLyrics.replace("\n"," _ ")
    words = re.findall(r'\[[^\]]+\]|\S+' , nospaces.lower())

    # Merge words inside square brackets into a single element
    clean = []
    line = ""
    for word in words:

        #if the word has an [ wait to find ] before adding ~
        if (word.find('[') != -1 or line.find('[') != -1):
            line += word
            if(word.find(']') != -1):
                clean.append("~")
                line = ""

        # looks for ( and ) to separate into separate elements
        elif(word.find('(') != -1 or word.find(')') != -1):
            line = ""
            for x in word:
                if(x == '('):
                    if (line):
                        clean.append(line)
                    clean.append("(")

                elif(x == ")"):
                    if (line):
                        clean.append(line)
                    clean.append(")")

                else:
                    line += x
            if (line):
                clean.append(line)               
                   
        else:
            clean.append(word)

    if(songName == "Rich Flex"):
        print(songLyrics)
        print(clean)
        print(word)

    return clean


def create_song(songLyrics, songName, songArtists, songID):
    easy = obfuscateLyrics(songLyrics, songName, songArtists, .2)
    medium = obfuscateLyrics(songLyrics, songName, songArtists, .5)
    hard = obfuscateLyrics(songLyrics, songName, songArtists, .7)
    return(Song(songID, songArtists, songLyrics, songName, easy, medium, hard))

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
    return clean_lyrics, int(song_id)



class User:
    def __init__(self, lvlsUnlocked, wordsUsed):
        self.unlocked = lvlsUnlocked
        self.wordsUsed = wordsUsed
    def json(self):
        return ({
            "levelsUnlocked": self.unlocked,
            "wordsUsed": self.wordsUsed
        })

        
class Song:
    def __init__(self, songID, artists, lyrics, name, obfEasy, obfMedium, obfHard):
        self.id = songID
        self.artists = artists
        self.lyrics = lyrics
        self.name = name
        self.obfPatterns = json.dumps({"easy": obfEasy, "medium": obfMedium, "hard": obfHard})

    def json(self):
        return ({
            "id": self.id,
            "artists": self.artists,
            "name": self.name,
            "lyrics": self.lyrics,
            "obfPatterns": self.obfPatterns
        })
    
    def tuple(self):
        return ((self.id, self.artists, self.lyrics, self.name, self.obfPatterns))


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
                id INTEGER,
                artists TEXT,
                lyrics TEXT,
                name TEXT,
                obfPatterns TEXT
            );"""
            create_leaderboard_table = """CREATE TABLE leaderboard (
                user TEXT,
                points INTEGER
            );"""
            create_user_table = """CREATE TABLE users (
                cookie TEXT,
                userData TEXT
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
    
    def downloadSongs(self):
        try:
            db = self.connect()
            cursor = db.cursor()
            songArray = []
            songNames = getTop50()
            for song in songNames:
                name = song[0]
                artists = ' & '.join(song[1])
                lyrics, id = getLyrics(name, artists)
                newSong = create_song(lyrics,name,artists,id)
                if (lyrics):
                    songArray.append(newSong.tuple())
                
            cursor.executemany("INSERT INTO songs VALUES (?,?,?,?,?)", songArray)
            db.commit()
            
            return True
        except:
            print("Something went wrong with downloading songs.")
            return False
        
        finally:
            db.close()

    
    def updateSong(self):
        return None
    
    def getSong(self):
        return None
    
    def deleteUser(self):
        return None
        
    def getPoints(self):
        return None
    
    def getSongFromDB(self, index):
        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"SELECT * FROM songs LIMIT 1 OFFSET {index}"
            cursor.execute(query)
            row = cursor.fetchall()

            return row
        except:
            return False
        finally:
            db.close()

    def sendTodaySongs(self):
        today = datetime.today().strftime('%Y-%m-%d')
        random.seed(today)
        indexes = []
        songs =  []
        for _ in range(3):
            indexes.append(random.randint(1,50))
        for index in indexes:
            song = self.getSongFromDB(index)
            if song == False:
                return False
            else:
                songs.append(self.getSongFromDB(index))
        
        return songs
    
    def getUserFromCookie(self, cookie):
        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"SELECT userData FROM users WHERE cookie = '{cookie}' LIMIT 1"
            cursor.execute(query)
            row = cursor.fetchall()
            return row
            
        except:
            return False

        finally:
            db.close()
    
    def updateUser(self, cookie, wordlist, level):
        user = self.getUserFromCookie(cookie)
        person = json.loads(user[0][0])
        person['wordsUsed'] = wordlist
        person['levelsUnlocked'] = level

        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"UPDATE users SET userData = '{json.dumps(person)}' WHERE cookie = '{cookie}';"
            cursor.execute(query)
            db.commit()
            return True
            
        except:
            return False
        finally:
            db.close()
    
    def addNewUser(self, cookie):
        try:
            db = self.connect()
            cursor = db.cursor()
            newUser = User(1,[])
            query = f"INSERT INTO users VALUES ('{cookie}', '{json.dumps(newUser.json())}')"
            cursor.execute(query)
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()


        





    

