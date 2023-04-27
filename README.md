
# CMSC 447 Project - Lyridact

A web-based game where lyrics to a song with varying amounts of words redacted are given to a player, who then tries to guess word by word what the title of the song is. There are 3 levels and they are updated everyday. Users can compete and have their scores uploaded to the global leaderboards.
## Preview

![Screenshot of Lyridact](https://github.com/PeteePanda/CMSC447/tree/main/media/GameShot1.png)



## Run Locally

Clone the project 

```bash
  git clone https://github.com/PeteePanda/CMSC447.git
```

Go to the project directory and open a terminal. This assumes you have Python3 installed.


Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

Add a ".env" file in the main directory and fill it in with the following:
```bash
SPOTIFY_CLIENT_ID="YOUR_SPOTIFY_API_CLIENT_ID_HERE"
SPOTIFY_SECRET="YOUR_SPOTIFY_API_KEY_HERE"
GENIUS_API_KEY="YOUR_GENIUS_API_KEY_HERE"

```

Start the server

```bash
python3 api.py
```




## Acknowledgements

 - [Spotify API for Top 50 Songs](https://developer.spotify.com/)
 - [Genius API for Lyric Data](https://docs.genius.com/)


## Authors

- [@Aidan-John](https://github.com/Aidan-John)
- [@Skhan2602](https://github.com/Skhan2602)
- [@ProgrammingMonke](https://github.com/ProgrammingMonke)
- [@NonnieNguyen](https://github.com/NonnieNguyen)
- [@PeteePanda](https://github.com/PeteePanda)

