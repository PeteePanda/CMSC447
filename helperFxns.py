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
import warnings
import threading

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
    lyrics = re.sub(r"\n.*liveget tickets.*\n", "\n", lyrics)
    # Split the lyrics by newline, this puts every line into an index
    # as well as giving all [Verse] lines their own index
    lines = re.split(r"\n", lyrics)

    # Look at each word and record how many times they occur
    wordlist = []
    special_chars = [",", "'", "(", ")","?",".", "!"]
    nonspecial = []

    for line in lines:
        if line:
            # Check for [] line and skip it
            if (line.find("[") != -1 or line.find("]") != -1):
                continue
            # Ensure consistent encoding
            line = line.replace("\u0435", "\u0065")
            line = line.replace('"', "'")
            line = re.sub(r'([()])',r' \1 ', line)

            words = re.split(r'\s+', line)
            
            for word in words:
                
                if word.isalpha() and word not in nonspecial:
                    nonspecial.append(word)

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

                #checks if word starts and ends with speical char
                elif word and word[0] in special_chars and word[-1] in special_chars:
                    temp = ""
                    for chara in word:
                        if chara not in special_chars:
                            temp += chara

                        else:
                            if temp:
                                wordlist.append(temp)
                                temp = ""
                            else:
                                wordlist.append(chara)


                #checks if the word starts with a punctuation
                elif word and word[0] in special_chars:
                    wordlist.append(word[0])
                    wordlist.append(word[1:])

                #checks if the word ends with a punctuation 
                elif word and word[-1] in special_chars:   
                    temp = ""
                    for chara in word:
                        if chara not in special_chars:
                            temp += chara

                        else:
                            if temp:
                                wordlist.append(temp)
                                temp = ""
                            else:
                                wordlist.append(chara)
            
                else:
                    wordlist.append(word)
        wordlist.append("~")

    # count words in song
    df = pd.value_counts(np.array(nonspecial))
    word_count = df.to_dict()
    # Definitely obfuscate words in title + artist names
    do_obf += songName.lower().split()
    for artist in songArtists:
        do_obf += artist.lower().split()

    # Calculate the number of words that need to be obf
    songLength = len(nonspecial)
    number_of_words_to_obfuscate = round(percentage * songLength)

    # Determine which groups of words should be obf'd
    obf_combo = findObfCombo(
        word_count, number_of_words_to_obfuscate, do_obf, dont_obf)

    # Obf the lyrics
    obfuscated_lines = []
    clean_lines = []
    for verse in wordlist:
        
        if verse:
            if verse[0] == "[" and verse[-1] == "]":
                obfuscated_lines.append("~")
                clean_lines.append('~')
                continue

            elif not verse.isalpha():
                obfuscated_lines.append(verse)
                clean_lines.append(verse)
                continue

            clean_lines.append(verse)
            for obf_word in obf_combo:
                if (obf_word not in special_chars):
                    regex = r"\b" + re.escape(obf_word) + r"\b"
                    if re.sub(regex, "_"*len(obf_word), verse) != verse:
                        verse = re.sub(regex, "_"*len(obf_word), verse)


            obfuscated_lines.append(verse)

    return obfuscated_lines, clean_lines



class User:
    def __init__(self, levelsUnlocked, wordsUsed, username):
        self.unlocked = levelsUnlocked
        self.wordsUsed = wordsUsed
        self.username = username

    def json(self):
        return ({
            "levelsUnlocked": self.unlocked,
            "wordsUsed": self.wordsUsed,
            "username": self.username
        })


class Song:
    def __init__(self, songID, artists, lyrics, name, obfEasy, obfMedium, obfHard):
        self.id = songID
        self.artists = " & ".join(artists)
        self.lyrics = lyrics
        self.name = name
        self.obfPatterns = {"easy": obfEasy,
                            "medium": obfMedium, "hard": obfHard}

    def tuple(self):
        return (self.id, json.dumps({"artists": self.artists, "lyrics": self.lyrics, "name": self.name, "obfPatterns": self.obfPatterns}))


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
                songData TEXT
            );"""
            create_easyLeaderboard_table = """CREATE TABLE easyLeaderboard (
                cookie TEXT,
                user TEXT,
                points INTEGER
            );"""

            create_mediumLeaderboard_table = """CREATE TABLE mediumLeaderboard (
                cookie TEXT,
                user TEXT,
                points INTEGER
            );"""

            create_hardLeaderboard_table = """CREATE TABLE hardLeaderboard (
                cookie TEXT,
                user TEXT,
                points INTEGER
            );"""

            create_user_table = """CREATE TABLE users (
                cookie TEXT,
                userData TEXT
            );"""

            db.execute(create_song_table)
            db.execute(create_easyLeaderboard_table)
            db.execute(create_mediumLeaderboard_table)
            db.execute(create_hardLeaderboard_table)
            db.execute(create_user_table)
            db.commit()
            print("Table reset.")
            return True
        except:
            print("Something went wrong with table reset.")
            return False

        finally:
            db.close()

    def downloadSongs(self, subset=100):
        # subset allows you to download only subset number of songs

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
                    if name and singers:
                        topFifty.append((name, singers))

                return topFifty
            else:
                return None

        def create_song(songLyrics, songName, songArtists, songID):
            easy, clean_lyrics = obfLyrics(
                songLyrics, songName, songArtists, .2)
            medium = obfLyrics(songLyrics, songName, songArtists, .5)[0]
            hard = obfLyrics(songLyrics, songName, songArtists, .8)[0]
            return (Song(songID, songArtists, clean_lyrics, songName, easy, medium, hard))

        def getLyrics(songName, songArtists, songArray, index):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                regex = r'[^a-zA-Z0-9\s]'
                name = re.sub(regex, '', songName.lower())
                artist = re.sub(regex, '', songArtists[0].lower())
                query = f'{name} {artist}'
                url = f"https://api.genius.com/search?q=" + \
                    re.sub(" ", "%20", query)

                access_token = os.environ.get("GENIUS_API_KEY")
                headers = {
                    'Authorization': "Bearer " + access_token
                }
                res = requests.get(url, headers=headers)
                data = json.loads(res.text)
                try:
                    song_id = data["response"]["hits"][0]["result"]["id"]
                except:
                    return False, False, False, False
                genius = lyricsgenius.Genius(access_token)
                lyrics = genius.lyrics(int(song_id))

                start = lyrics.find('[')
                if start == -1:
                    print("These lyrics aren't properly formatted, skipping")
                    return False, False, False, False
                clean_lyrics = lyrics[start:-7]

                print(repr(songName))
                print(repr(songArtists))
                if(songName and songArtists and clean_lyrics and song_id):
                    songArray[index] = (songName, songArtists, clean_lyrics, int(song_id))

            

        try:
            db = self.connect()
            cursor = db.cursor()
            songArray = []
            songNames = getTop50()
            counter = 0
            # Vars for multithreading
            downloadArray = [(False, False, False, False)] * len(songNames)
            threads = [None] * len(songNames)
            for song in songNames:
                if song:
                    counter += 1
                    if counter > subset:
                        break

                    name = song[0]
                    artists = song[1]
                    
                    # Multithreading
                    threads[counter - 1] = threading.Thread(target=getLyrics, args=(name, artists, downloadArray, counter - 1))
                    threads[counter - 1].start()
            
            # Wait for threads to finish
            for i in range(len(threads)):
                threads[i].join()

            for name, artists, lyrics, id in downloadArray:
                if lyrics == False or id == False or name == False or artists == False:
                    continue

                name = re.sub(r'[&]', "and",name)
                name = re.sub(r'[^a-zA-Z]+', " ",name)
                newSong = create_song(lyrics, name, artists, id)
                songArray.append(newSong.tuple())

            cursor.executemany(
                "INSERT INTO songs VALUES (?,?)", songArray)
            db.commit()

            return True
        except Exception as e:
            print("Something went wrong with downloading songs.")
            print(e)
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
    
    def getSongTableSize(self):
        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"SELECT COUNT(*) FROM songs"
            cursor.execute(query)
            row = cursor.fetchall()
            return int(row[0][0])
        except:
            return False
        finally:
            db.close()

    def sendTodaySongs(self, today):
        random.seed(today)
        indexes = []
        songs = []
        num_songs = self.getSongTableSize()
        if num_songs == 0:
            print("Song table is empty")
            return False
        while len(indexes) < 3:
            chosenIndex = random.randint(1, num_songs)
            chosenSong = self.getSongFromDB(chosenIndex)
            if chosenSong:
                if chosenSong not in indexes:
                    indexes.append(chosenSong)
        easySong = indexes[0]
        mediumSong = indexes[1]
        hardSong = indexes[2]

        if easySong == False or mediumSong == False or hardSong == False:
            return False
        
        easyData = json.loads(easySong[0][1])
        mediumData = json.loads(mediumSong[0][1])
        hardData = json.loads(hardSong[0][1])

        easyJSON = {
            "level": 1,
            "artist": easyData["artists"],
            "lyrics": easyData["lyrics"],
            "name": easyData["name"],
            "obfLyrics": easyData["obfPatterns"]["easy"]
        }
        mediumJSON = {
            "level": 2,
            "artist": mediumData["artists"],
            "lyrics": mediumData["lyrics"],
            "name": mediumData["name"],
            "obfLyrics": mediumData["obfPatterns"]["medium"]
        }

        hardJSON = {
            "level": 3,
            "artist": hardData["artists"],
            "lyrics": hardData["lyrics"],
            "name": hardData["name"],
            "obfLyrics": hardData["obfPatterns"]["hard"]
        }

        return [easyJSON, mediumJSON, hardJSON]

    def getUserFromCookie(self, cookie):

        try:
            db = self.connect()
            cursor = db.cursor()
            query = f"SELECT userData FROM users WHERE cookie = ? LIMIT 1"
            cursor.execute(query, (cookie,))
            row = cursor.fetchall()
            user = json.loads(str(row[0][0]))
            return user

        except Exception as e:
            print("Issue getting user: ", e)
            return False

        finally:
            db.close()

    def updateUser(self, cookie, wordlist, level, username):
        print("Updating: ",cookie, wordlist, level, username)
        user = self.getUserFromCookie(cookie)
        user['wordsUsed'] = wordlist
        user['levelsUnlocked'] = level
        user['username'] = username

        try:
            db = self.connect()
            cursor = db.cursor()
            query = 'UPDATE users SET userData = ? WHERE cookie = ?;'
            cursor.execute(query, (json.dumps(user), cookie))
            db.commit()
            return True

        except Exception as e:
            print("Something went wrong updating: ", e)
            return False
        finally:
            db.close()

    def addNewUser(self, cookie):
        try:
            db = self.connect()
            cursor = db.cursor()
            newUser = User(1, [], "")
            query = "INSERT INTO users VALUES (?, ?)"
            cursor.execute(query, (cookie, json.dumps(newUser.json())))
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()

    def getLeaderboard(self, level):
        try:
            db = self.connect()
            cursor = db.cursor()
            if level == 1:
                query = "SELECT * FROM easyLeaderboard ORDER BY points ASC"
            elif level == 2:
                query = "SELECT * FROM mediumLeaderboard ORDER BY points ASC"
            elif level == 3:
                query = "SELECT * FROM hardLeaderboard ORDER BY points ASC"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                return_data = list()
                for cookie, user, points in data:
                    return_data.append([user, points])
                return return_data
            else:
                print("no data")
                return False
        except Exception as e:
            print("something went wrong: ", e)
            return False
        finally:
            db.close()

    def getRanking(self, level, points):
        try:
            db = self.connect()
            cursor = db.cursor()
            if level == 1:
                query = "SELECT COUNT(*) FROM easyLeaderboard WHERE points < ?"
            elif level == 2:
                query = "SELECT COUNT(*) FROM mediumLeaderboard WHERE points < ?"
            elif level == 3:
                query = "SELECT COUNT(*) FROM hardLeaderboard WHERE points < ?"
            cursor.execute(query, (points,))
            data = cursor.fetchall()
            if data:
                return data[0][0] + 1
            else:
                return False
        except:
            return False
        finally:
            db.close()

    def addScoreToLeaderboard(self, points, cookie, level, username):
        try:
            db = self.connect()
            cursor = db.cursor()

            # Choose the appropriate leaderboard table
            if level == 1:
                leaderboard = "easyLeaderboard"
            elif level == 2:
                leaderboard = "mediumLeaderboard"
            elif level == 3:
                leaderboard = "hardLeaderboard"

            # Check if the cookie already exists in the leaderboard
            check_query = f"SELECT * FROM {leaderboard} WHERE cookie = ?"
            cursor.execute(check_query, (cookie,))
            userScore = cursor.fetchall()
            print("userScore: ", userScore)
            if userScore:
                if userScore[2] > points:
                    # If the cookie exists in the leaderboard, update the score if the new score is lower
                    query = f"UPDATE {leaderboard} SET points = ? WHERE cookie = ?"
                    cursor.execute(query, (points, cookie))
                    db.commit()
                    return True
                elif userScore[2] <= points:
                    # If the cookie exists in the leaderboard, but the new score is higher, do nothing
                    return True
                
            else:
                # If the cookie does not exist in the leaderboard, insert the new score
                query = f"INSERT INTO {leaderboard} VALUES (?,?,?)"
                cursor.execute(query, (cookie, username, points))
                db.commit()
                return True
        except:
            return False
        finally:
            db.close()

    def resetLeaderboard(self, level):
        try:
            db = self.connect()
            cursor = db.cursor()
            if level == 1:
                query = "DROP TABLE easyLeaderboard"
            elif level == 2:
                query = "DROP TABLE mediumLeaderboard"
            elif level == 3:
                query = "DROP TABLE hardLeaderboard"
            cursor.execute(query)
            db.commit()
            if level == 1:
                query = """CREATE TABLE easyLeaderboard (
                    cookie TEXT,
                    points INTEGER
                );"""
            elif level == 2:
                query = """CREATE TABLE mediumLeaderboard (
                    cookie TEXT,
                    points INTEGER
                );"""
            elif level == 3:
                query = """CREATE TABLE hardLeaderboard (
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
