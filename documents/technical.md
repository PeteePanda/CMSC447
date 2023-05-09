You will write technical documentation that outlines the class diagrams, database, and API calls within your project. As the name suggests, this part should be technical.

<h2><strong>Database</strong></h2>
<p>We use one database split into 5 different tables: songs, users, easyLeaderboard, mediumLeaderboard, and hardLeaderboard.</p>

<h3><strong>songs:</strong></h3>
<p>The songs database holds 2 columns: id and songData. Id is a unique identifier for each song and is used***. songData holds information about the song recieved from spotify and genius. It holds: artist(s), title, unobfuscated lyrics, easy obfuscated lyrics, medium obfuscated lyrics, and hard obfuscated lyrics.</p>

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
<h4><strong>Home Page:</strong></h4>
<p>Whenever a player loads into the game, they are assigned a cookie. That cookie then gets that user's information from the users table, but if the cookie returns no information that means the user has no information. If the user has no information we initialize that user's information to be stored in the database.
</p>

<h4><strong>Update User:</strong></h4>
<p>Whenever a player makes a guess, that guess is stored into the users table of the database under their cookie. And whenever the player completes a level, their levels unlocked is incremented and their word list is cleared.
</p>

<h4><strong>Add Leaderboard Score:</strong></h4>
<p>Whenever a player completes a level, the frontend then sends the cookie, number of guesses, the difficulty they completed, and the username of the player to store in the database. In return the backend returns the rank of the player on that difficulty.
</p>

<h4><strong>Get Leaderboard: </strong></h4>
<p>After the user's score is added to the leaderboard, another API call is made where the frontend sends the backend the difficulty completed then the backend returns the top 5 players from that leaderboard ordered by ascending guesses.
</p>