You will write technical documentation that outlines the class diagrams, database, and API calls within your project. As the name suggests, this part should be technical.
<h1><strong>Technical Document</strong></h1>
<h2><strong>Class Diagram</strong></h2>
<p>There are three main parts to the class diagram: scripts.js, api.py, and helperFxns.py.
</p>

<h2><strong>script.js:</strong></h2>
<p>scrpit.js is what handles all the frontend functions, from simple buttons to fetching information from the backend to display to the user. There are 4 main functions that talk to the backend and a few others that are integral to running the game.
</p>

<h3><strong>getLeaderboardData()</strong></h3>
<p>This function sends the level that the user has completed to api_getLeaderborad() and receives the top five usernames and their respective number of guesses, in ascending order.
</p>

<h3><strong>addLBScore()</strong></h3>
<p>Similar to getLeaderboardData(), this function waits for the user to complete the level and once they do api_addLBScore() is given the parameters of the number of guesses, what level the player is on, and their username. Once complete the user's rank, top 5 or not, is returned.
</p>

<h3><strong>getSongData()</strong></h3>
<p>At the beginning of every day, the frontend requests a list of 3 songs of easy, medium, and hard difficulty from api_getSongs(). It then stores each song's title, obfuscated title, artist(s), the regular lyrics, and the obfuscated lyrics.
</p>

<h3><strong>sendUserData(userGuesses)</strong></h3>
<p>After each guess the function sends the words guessed, current level, and the player's username to api_updateUser() to be updated in the database.
</p>

<h3><strong>processGuess(guessString)</strong></h3>
<p>Whatever the user enters in to guess a obfuscated word it comes to this function. It first counts the number of that word in the song and fills in the lyrics accordingly. Then it fills in the the blanks of the song title if the guess is present in it.
</p>

<h3><strong>roundWin()</strong></h3>
<p>If the player has revealed all words in the title of the song, the lyrics are revealed with the song title. Then the next level's information is stored to be displayed, addLBScore() is called, getLeaderboardData(level) is called, then the leaderboard is displayed.
</p>

<h2><strong>api.py:</strong></h2>
<p>api.py is the middle man between the frontend and the backend, as it sends a jsonified package of information to helperFxns.py and awaits information to be sent back, if needed.
</p>

<h2><strong>helperFxns.py:</strong></h2>
<p>helperFxns.py is the bulk of the backend as it holds the functions to obfuscate the lyrics, get and store information into the database, get the songs from our external APIs, etc.
</p>

<h3><strong>obfLyrics()</strong></h3>
<p>To be abale to play the game, each song needs to have a certain percentage depending on the difficulty (20%, 50%, 80%). Due to the Genius API being a webscraper, there are many characters that are not normal and have special values to them, such as a " being \u0435, and it includes cues of when the chorus or verses are. So this function replaces every non-character with it's appropriate normal character, and removes unnecessary information. And to make things easier on the player, we decided to keep words that have special characters to remain revealed.
</p>

<h3><strong>User</strong></h3>
<p>This class' main function is to take the information of the user and package it as a dictionary to be stored into the database
</p>

<h3><strong>Song</strong></h3>
<p>This class', much like the User class, is mainly for packaging the song's information as a dictionary to be stored into the database
</p>

<h3><strong>Lyridact_DB</strong></h3>
<p>This is the main class of the file for this class is able to input and recieve data from the database. It is able to download songs from the external APIs from Spotify and Genius and stores those with the obfuscated lyrics in the database. It's able to get information from songs, users, or any leaderboard using SQLite3 methods. And if there were to be any corrupted data in the database, it could reset and reload all the information required to play the game again.
</p>

<h2><strong>Database</strong></h2>
<p>We use one database split into 5 different tables: songs, users, easyLeaderboard, mediumLeaderboard, and hardLeaderboard.</p>

<h3><strong>songs:</strong></h3>
<p>The songs database holds 2 columns: id and songData. Id is a unique identifier for each song. songData holds information about the song recieved from spotify and genius. It holds: artist(s), title, unobfuscated lyrics, easy obfuscated lyrics, medium obfuscated lyrics, and hard obfuscated lyrics.</p>

<h3><strong>users:</strong></h3>
<p>Holds 2 columns of cookie and userData. The cookie is just a unique string to be able to receive the proper userData from the table. userData hold the information of what level the user is on, the guesses the user has made, and the username.</p>

<h3><strong>easyLeaderboard, mediumLeaderboard, hardLeaderboard:</strong></h3>
<p>Each leaderboard holds the cookie, username, and points (number of guesses) of the players who have completed the respective difficulty. The cookie is stored in the leaderboard to ensure that the player's position is properly returned if they have the same username as another player</p>

<h2><strong>API calls</strong></h2>
<p>We have a few different API calls that are made. We have 2 separate API calls to external sources to get our song information and API calls to send and retrieve information from the database. Spotify's US top 50 songs of the week and Genius' lyrics are the external APIs utalized to get our songs/information</p>

<h3><strong>Spotify's US Top 50:</strong></h3>
<p>We are using a Spotify's free API to retrieve the top 50 artists of the week. The input of how to get the information all that is requred is the id of the playlist you want information from, and the proper client id and secret key. Through this we are able to get the artist(s) and the song title. We then use this information to get the lyrics from Genius</p>

<h3><strong>Genius:</strong></h3>
<p>Genius' API allows us to get the lyrics of a song with just the artist(s) and the song title. However, the API is a webscraper so there is a lot of unnecessary information and unique characters that need to be removed/replaced in the lyrics.
</p>

<h3><strong>Internal API calls:</strong></h3>
<h3><strong>Home Page:</strong></h3>
<p>Whenever a player loads into the game, they are assigned a cookie. That cookie then gets that user's information from the users table, but if the cookie returns no information that means the user has no information. If the user has no information we initialize that user's information to be stored in the database.
</p>

<h3><strong>Update User:</strong></h3>
<p>Whenever a player makes a guess, that guess is stored into the users table of the database under their cookie. And whenever the player completes a level, their levels unlocked is incremented and their word list is cleared.
</p>

<h3><strong>Add Leaderboard Score:</strong></h3>
<p>Whenever a player completes a level, the frontend then sends the cookie, number of guesses, the difficulty they completed, and the username of the player to store in the database. In return the backend returns the rank of the player on that difficulty.
</p>

<h3><strong>Get Leaderboard:</strong></h3>
<p>After the user's score is added to the leaderboard, another API call is made where the frontend sends the backend the difficulty completed then the backend returns the top 5 players (username, guesses) from that leaderboard ordered by ascending guesses.
</p>
 