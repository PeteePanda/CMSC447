import unittest
from helperFxns import *
import datetime


class TestUtils(unittest.TestCase):
      
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

        for _ in range(100):
            easy = " ".join(obfLyrics(lyrics, name, artists, .2)[0])
            wordCount = len(lyrics.split())
            obfCount = len(re.findall(r'_+', easy))
            self.assertTrue( (obfCount / wordCount) <= .25)
        

    def test_download_and_obf(self):
        db = Lyridact_DB("test_data.db")
        db.reset()
        self.assertTrue(db.downloadSongs(100))
    
    def test_sendTodaySongs(self):
        db = Lyridact_DB("test_data.db")
        for day in range(100):
            today = datetime.datetime.today()
            test = (today + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
            songs = db.sendTodaySongs(test)
            self.assertTrue(songs)

    def test_obf_percent(self):
        db = Lyridact_DB("test_data.db")
        song_info = db.getSongFromDB(0)
        print("Printing, song info: ")

        
        table_len = db.getSongTableSize()
        print("Table size: ", table_len)
        complete_test = True
        obf_count = 0
        word_count = 0
        easy_total = 0
        medium_total = 0
        hard_total = 0
        for i in range(table_len):
            song_info = db.getSongFromDB(i)
            for column in song_info:
                for thing in column:
                    if isinstance(thing, str):
                        word = ""
                        obf_count = 0
                        word_count = 0
                        for character in thing:
                            if character == "\"":
                                #print(word, end="")
                                if "_" in word:
                                    obf_count += 1
                                word_count += .5
                                word = ""
                            else:
                                word += character

                            if word == "easyOBF":
                                #print("\nclean obf: ", obf_count, "\nword: ", word_count, "\nRatio: ", obf_count/word_count)
                                print(id, end="")
                                obf_count = 0
                                word_count = 0
                            elif word == "mediumOBF":
                                print("\neasy Ratio: ", obf_count/word_count, end="")
                                if not(obf_count/word_count > 15 and obf_count/word_count < 25):
                                    complete_test = False
                                
                                easy_total += obf_count/word_count
                                obf_count = 0
                                word_count = 0
                            elif word == "hardOBF":
                                print("\nmedium Ratio: ", obf_count/word_count, end="")
                                
                                medium_total += obf_count/word_count
                                obf_count = 0
                                word_count = 0
                    else:
                        id = thing
                        print()
            print("\nhard Ratio: ", obf_count/word_count)
            if not(obf_count/word_count > 65 and obf_count/word_count < 75):
                complete_test = False
            
            hard_total += obf_count/word_count
            #print(id, "\nOBF Percentage +/- 5%")
        print("\nAverage obf Percentages: \neasy: ", easy_total/table_len, "\nmedium", medium_total/table_len, "\nhard", hard_total/table_len)

if __name__ == "__main__":
    unittest.main()