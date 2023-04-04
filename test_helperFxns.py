import unittest
from helperFxns import *


class TestUtils(unittest.TestCase):
    db = Lyridact_DB("test_data.db")
    sample_lyrics = "I used to bite my tounge and hold my breath Scared to rock the boat and make a mess So I sat quietly Agreed politely  I guess that I forgot I had a choice I let you push me past the breaking point I stood for nothing So I fell for everything  You held me down, but I got up (Hey!) Already brushing off the dust You hear my voice, you hear that sound Like thunder gonna shake the ground You held me down, but I got up (Hey!) Get ready 'cause I've had enough I see it all, I see it now  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Now I'm floating like a butterfly Stinging like a bee I earned my stripes I went from zero To my own hero  You held me down, but I got up (Hey!) Already brushing off the dust You hear my voice, you hear that sound Like thunder gonna shake the ground You held me down, but I got up (Got up!) Get ready 'cause I've had enough I see it all, I see it now  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You'll hear me roar Oh oh oh oh oh oh oh You're gonna hear me roar  Roar, roar, roar, roar, roar  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You'll hear me roar Oh oh oh oh oh oh oh You're gonna hear me roar"
    sample_artists = ["Katy Perry"]
    sample_name = "Roar"

    def test_obfuscateLyrics(self):
        song_length = len(self.sample_lyrics.lower().split())
        percentage = 0.5
        result = obfuscateLyrics(self.sample_lyrics, self.sample_name, self.sample_artists, percentage)

        count = 0
        for lyric in result:
            if "_" in lyric:
                count += 1
        
        actualObfuscation = count / song_length
        
        self.assertTrue(abs(percentage - actualObfuscation) < .05)

    def test_database_reset(self):
        db = self.db
        
        check = db.reset()
        
        conn = sqlite3.connect(db.DBpath).cursor()
        conn.execute("""SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';""")
        result = conn.fetchall()
        self.assertTrue( result[0][0] == "songs")
        self.assertTrue( result[1][0] == "leaderboard")
        self.assertTrue( result[2][0] == "users")
        self.assertTrue( check == True )

    def test_top50download(self):
        db = self.db
        #obf = {"1": "val1", "2":"val2"}
        #x = [(123, 'song name', 'hello lyrics', "songName", json.dumps(obf))]
        #db.addSongs(x)
        

        print("Songs have been downloaded - ", db.downloadSongs())
        

          
        

if __name__ == "__main__":
    unittest.main()