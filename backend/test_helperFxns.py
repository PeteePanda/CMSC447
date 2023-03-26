import unittest
from helperFxns import *

###################### IMPORTANT ######################
###### RUNNING THIS TEST WILL CLEAR THE DATABASE ######
#######################################################


class TestUtils(unittest.TestCase):
    sample_lyrics = "I used to bite my tongue and hold my breath Scared to rock the boat and make a mess So I sat quietly Agreed politely  I guess that I forgot I had a choice I let you push me past the breaking point I stood for nothing So I fell for everything  You held me down, but I got up (Hey!) Already brushing off the dust You hear my voice, you hear that sound Like thunder gonna shake the ground You held me down, but I got up (Hey!) Get ready 'cause I've had enough I see it all, I see it now  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Now I'm floating like a butterfly Stinging like a bee I earned my stripes I went from zero To my own hero  You held me down, but I got up (Hey!) Already brushing off the dust You hear my voice, you hear that sound Like thunder gonna shake the ground You held me down, but I got up (Got up!) Get ready 'cause I've had enough I see it all, I see it now  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You'll hear me roar Oh oh oh oh oh oh oh You're gonna hear me roar  Roar, roar, roar, roar, roar  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You'll hear me roar Oh oh oh oh oh oh oh You're gonna hear me roar"
    sample_artist = "Katy Perry"
    sample_name = "Roar"

    def test_obfuscateLyrics(self):
        song_length = len(self.sample_lyrics.lower().split())
        percentage = 0.5
        result = obfuscateLyrics(self.sample_lyrics, self.sample_artist, self.sample_name, percentage)

        count = 0
        for lyric in result["obfuscatedLyrics"]:
            if lyric == "_":
                count += 1
        
        actualObfuscation = count / song_length
        self.assertTrue(abs(percentage - actualObfuscation) < .05)

    def test_database_reset(self):
        reset_db = Lyridactle_DB().reset()
        
        conn = sqlite3.connect("data.db").cursor()
        conn.execute("""SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';""")
        result = conn.fetchall()
        self.assertTrue( result[0][0] == "songs")
        self.assertTrue( result[1][0] == "leaderboard")
        self.assertTrue( result[2][0] == "users")
        self.assertTrue( reset_db == True)
          
        

if __name__ == "__main__":
    unittest.main()