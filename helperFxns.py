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
import numpy as np
import pandas as pd


load_dotenv()


def generateCookie():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(20))



def obfLyrics(songLyrics, songName, songArtists, percentage):

    def findObfCombo(count_dict, target, do_obf, dont_obf):
        words_to_obf = []
        counter = 0
        # Make sure the given obf words are obfd
        for word in do_obf:
            if word in count_dict.keys():
                counter += count_dict[word]
                count_dict.pop(word)
        # While the number of obfd words is still under target
        while counter <= target:
            # Pick a random word
            choice = random.choice(list(count_dict.keys()))
            if choice in dont_obf:
                continue
            # Check if it doesn't exceed the percentage buffer
            if (count_dict[choice] + counter) <= (target + 2):
                # Add choice to return array and remove it from dict
                words_to_obf.append(choice)
                counter += count_dict[choice]
                count_dict.pop(choice)

       

        return words_to_obf + do_obf

    dont_obf = []
    do_obf = []

    # Scraping weirdness puts this phrase in some lyrics, remove it
    lyrics = re.sub(r"you might also like", "", songLyrics.lower())
    # Split the lyrics by newline, this puts every line into an index
    # as well as giving all [Verse] lines their own index
    lines = re.split(r"\n", lyrics)

    # Look at each word and record how many times they occur
    wordlist = []
    diff_list = []
    for line in lines:
        if line:

            # Check for [] line and skip it
            if line[0] == "[" and line[-1] == "]":

                continue
            # Ensure consistent encoding
            line = line.replace("\u0435", "\u0065")
            line = line.replace('"', "'")

            # remove punctuation
            clean_line = re.sub(r"""[\\'"?().!,]*""", "", line)

            # create word list
            words = clean_line.split(" ")
            diff_list.append((line, words))
            for word in words:
                # handle hyphenated words
                if "-" in word:
                    wordSplit = word.split("-")
                    # check if all words are the same, if so append
                    if (all(x == wordSplit[0] for x in wordSplit)):
                        for w in wordSplit:
                            wordlist.append(w)
                    else:
                        if word not in dont_obf:
                           dont_obf.append(word)
                        wordlist.append(word)
                else:
                    wordlist.append(word)
    # count words in song
    df = pd.value_counts(np.array(wordlist))
    word_count = df.to_dict()
    # Definitely obfuscate words in title + artist names
    do_obf += songName.lower().split()
    for artist in songArtists:
        do_obf += artist.lower().split()

    # Calculate the number of words that need to be obf
    songLength = len(wordlist)
    number_of_words_to_obfuscate = round(percentage * songLength)
    

    # Determine which groups of words should be obf'd
    obf_combo = findObfCombo(
        word_count, number_of_words_to_obfuscate, do_obf, dont_obf)

    # Obf the lyrics
    obfuscated_lines = []
    for verse in lines:
        if verse:
            if verse[0] == "[" and verse[-1] == "]":
                obfuscated_lines.append("~")
                continue

            ######### NEED LOGIC THAT OBFs any word in obf_combo ########
            # This line is supposed to remove any misc. \ characters but it isn't working
            verse = re.sub(r'"', "'", verse)
            for obf_word in obf_combo:

                regex = r"\b" + re.escape(obf_word) + r"\b"
                if re.sub(regex, "_"*len(obf_word), verse) != verse:
                    verse = re.sub(regex, "_"*len(obf_word), verse)

            obfuscated_lines.append(verse)

    # add ~ to the end of each line for franco's spacing, convert to 1d array
    return_array = []
    for line in obfuscated_lines:
        if "~" not in line:
            line = line + "~"
        words = line.split()
        return_array += words
    
    return return_array
    


def create_song(songLyrics, songName, songArtists, songID):
    easy = obfLyrics(songLyrics, songName, songArtists, .2)
    medium = obfLyrics(songLyrics, songName, songArtists, .5)
    hard = obfLyrics(songLyrics, songName, songArtists, .7)
    return (Song(songID, songArtists, songLyrics, songName, easy, medium, hard))


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
    print(repr(clean_lyrics))
    print(repr(songName))
    print(repr(songArtists))
    
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
        self.obfPatterns = json.dumps(
            {"easy": obfEasy, "medium": obfMedium, "hard": obfHard})

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
                cookie TEXT,
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

    def downloadSongs(self):

        try:
            db = self.connect()
            cursor = db.cursor()
            songArray = []
            songNames = getTop50()
            for song in songNames:
                name = song[0]
                artists = song[1]
                lyrics, id = getLyrics(name, artists)
                artist = ' & '.join(artists)
                newSong = create_song(lyrics,name,artist,id)
                songArray.append(newSong.tuple())

            cursor.executemany(
                "INSERT INTO songs VALUES (?,?,?,?,?)", songArray)
            db.commit()

            return True
        except:
            print("Something went wrong with downloading songs.")
            return False

        finally:
            db.close()

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
        songs = []
        for _ in range(3):
            indexes.append(random.randint(1, 50))
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
            user = json.loads(row[0][0])
            return user

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
            newUser = User(1, [])
            query = f"INSERT INTO users VALUES ('{cookie}', '{json.dumps(newUser.json())}')"
            cursor.execute(query)
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()

    def getLeaderboard(self):
        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"SELECT * FROM leaderboard ORDER BY points DESC"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                return data
            else:
                return False
        except:
            return False
        finally:
            db.close()

    def addScoreToLeaderboard(self, points, cookie):
        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"INSERT INTO leaderboard VALUES ('{cookie}', {points})"
            cursor.execute(query)
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()

    def resetLeaderboard(self):
        try:
            db = self.connect()
            cursor = db.cursor()
            query = "DROP TABLE leaderboard"
            cursor.execute(query)
            db.commit()
            query = """CREATE TABLE leaderboard (
                cookie TEXT,
                points INTEGER
            );"""
            cursor.execute(query)
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()
    
    def postTopFive(self, url):
        lb = self.getLeaderboard()[:5]
        if lb:
            # Still need to get correct format for json from prof
            data = {}
            try:
                x = requests.post(url, json=data)
                print(x.text)
                return True
            except:
                return False
        return False



