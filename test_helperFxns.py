import unittest
from helperFxns import *


class TestUtils(unittest.TestCase):
    db = Lyridact_DB("test_data.db")
    sample_lyrics = "I used to bite my tounge and hold my breath Scared to rock the boat and make a mess So I sat quietly Agreed politely  I guess that I forgot I had a choice I let you push me past the breaking point I stood for nothing So I fell for everything  You held me down, but I got up (Hey!) Already brushing off the dust You hear my voice, you hear that sound Like thunder gonna shake the ground You held me down, but I got up (Hey!) Get ready 'cause I've had enough I see it all, I see it now  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Now I'm floating like a butterfly Stinging like a bee I earned my stripes I went from zero To my own hero  You held me down, but I got up (Hey!) Already brushing off the dust You hear my voice, you hear that sound Like thunder gonna shake the ground You held me down, but I got up (Got up!) Get ready 'cause I've had enough I see it all, I see it now  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You'll hear me roar Oh oh oh oh oh oh oh You're gonna hear me roar  Roar, roar, roar, roar, roar  I got the eye of the tiger A fighter Dancing through the fire 'Cause I am a champion and you're gonna hear me roar Louder, louder than a lion 'Cause I am a champion and you're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You're gonna hear me roar  Oh oh oh oh oh oh oh Oh oh oh oh oh oh oh You'll hear me roar Oh oh oh oh oh oh oh You're gonna hear me roar"
    sample_artists = ["Katy Perry"]
    sample_name = "Roar"

    lyric = ""
    def test_obfuscateLyrics(self):
        """
        song_length = len(self.sample_lyrics.lower().split())
        percentage = 0.5
        result = obfuscateLyrics(self.sample_lyrics, self.sample_name, self.sample_artists, percentage)

        count = 0
        for lyric in result:
            if "_" in lyric:
                count += 1
        
        actualObfuscation = count / song_length
        
        self.assertTrue(abs(percentage - actualObfuscation) < .05)
        """
        return True

    def test_database_reset(self):
        '''
        db = Lyridact_DB("test_data.db")
        
        check = db.reset()
        
        conn = db.connect().cursor()
        conn.execute("""SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';""")
        result = conn.fetchall()
        self.assertTrue( result[0][0] == "songs")
        self.assertTrue( result[1][0] == "leaderboard")
        self.assertTrue( result[2][0] == "users")
        self.assertTrue( check == True )
        '''
        return True

    def test_top50download(self):
        db = Lyridact_DB("test_data.db")
        #db.downloadSongs()
        return True

        #obf = {"1": "val1", "2":"val2"}
        #x = [(123, 'song name', 'hello lyrics', "songName", json.dumps(obf))]
        #db.addSongs(x)
        

        ##print("Songs have been downloaded - ", db.downloadSongs())

        
    def test_Leaderboard(self):
        db = Lyridact_DB("test_data.db")
        test_score = ("randomcookie", 99)
        db.addScoreToLeaderboard(test_score[1], test_score[0])
        lb = db.getLeaderboard()
        self.assertTrue( lb[0] == test_score)
        db.resetLeaderboard()
        lb = db.getLeaderboard()
        self.assertFalse(lb)
        
    def test_obf(self):
        lyrics = '[Verse 1: PinkPantheress]\nTake a look inside your heart\nIs there any room for me (Is there any room for me?)\nI won\'t have to hold my breath\nTill you get down on one knee (Till you get down on one knee)\nBecause you only want to hold me\nWhen I\'m looking good enough (When I\'m looking good enough)\nDid you ever feel me?\nWould you ever picture us? (Would you ever picture us?)\n\n[Verse 2: PinkPantheress]\nEvery time I pull my hair\nWell, it\'s only out of fear (Only out of fear)\nThat you\'ll find me ugly\nAnd one day you\'ll disappear because\nWhat\'s the point of crying?\nIt was nеver even lovе (It was never even love)\nDid you ever want me?\nWas I ever good enough? (Ever good enough?)\n[Chorus: PinkPantheress]\nThe-the boy\'s a liar, the boy\'s a liar\nHe doesn\'t see ya, you\'re not looking at me, boy\nThe boy\'s a liar, the boy\'s a liar\nHe doesn\'t see ya, you\'re not looking at me, boy\n\n[Post-Chorus: PinkPantheress]\nGood eno-o-ough, good eno-o-ough\nGood eno-o-ough, good eno-o-ough\nGood eno-o-ough, good eno-o-ough\nGood eno-o-ough, good eno-o-ough\n\n[Verse 3: Ice Spice]\nHe say that I\'m good enough, grabbin\' my duh-duh-duh\nThinkin\' \'bout shit that I shouldn\'t\'ve (Huh)\nSo I tell him there\'s one of me, he makin\' fun of me (Ha-ha)\nHis girl is a bum to me (Grrah)\nLike that boy is a cap\nSayin\' he home, but I know where he at, like\nBet he blowin\' her back\nThinkin\' \'bout me \'cause he know that it\'s fat (Damn)\nAnd it been what it been (Huh)\nCallin\' his phone like, "Yo, send me a pin"\nDuckin\' my shit, \'cause he know what I\'m on (Grrah)\nBut when he hit me I\'m not gon\' respond (Grrah)\nBut I don\'t sleep enough without you\nAnd I can\'t eat enough without you (Huh)\nIf you don\'t speak, does that mean we\'re through? (Huh)\nDon\'t like sneaky shit that you do (Grrah)\nYou might also like[Chorus: PinkPantheress]\nThe-the boy\'s a liar, the boy\'s a liar\nHe doesn\'t see ya, you\'re not looking at me, boy\nThe boy\'s a liar, the boy\'s a liar\nHe doesn\'t see ya, you\'re not looking at me, boy\n\n[Post-Chorus: PinkPantheress]\nGood eno-o-ough, good eno-o-ough\nGood eno-o-ough, good eno-o-ough\nGood eno-o-ough, good eno-o-ough\nGood eno-o-ough, good eno-o-ough'
        name = "Boy's a liar Pt. 2"
        artists = ['PinkPantheress', 'Ice Spice']
        
        easy = obfLyrics(lyrics, name, artists, .2)
        print(easy)

        return True
    


          
        

if __name__ == "__main__":
    unittest.main()