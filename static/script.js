const addGuessBtn = document.querySelector('#guess-btn');
const nameBtn = document.querySelector('#username-btn');

// Prevent page from refreshing when user hits [Enter] for their username
nameBtn.addEventListener('click', (event)=>{
    event.preventDefault();
});

// Event Listener to manage a user guesses; activates whenever submit button is clicked
addGuessBtn.addEventListener('click', (event)=>{
    event.preventDefault(); // prevent refresh of page
    const guessInput = document.querySelector('#guess-input');
    let guessString = guessInput.value.toString().toLowerCase().split(" ").join(""); // format guess string
    // Check if word was already guessed or response is blank
    if(usedGuesses.includes(guessString) || (guessString == "") || invalidWords.includes(guessString) || guessString.length > 15){
        console.log("Invalid or used word");
    }
    else{
        // Add word to already guessed words
        usedGuesses.push(guessString);
        
        // Check the guess with the puzzle
        let wordCount = processGuess(guessString);

        // Send updated guess data to DB
        sendUserData(usedGuesses);

        // Update table with guess
        modifyTable(guessString,wordCount);

        // Reload page with updated info
        updatePage();

        // Check win condition
        roundWin();
    }

    // Clear the input field
    guessInput.value = "";
});

// Tries to solve the puzzle using the valid guess and returns how frequent it shows up in the puzzle
function processGuess(guessString){
       // Count the number of hits in the song and fill in the lyrics (brokeSong array)
       let wordCount = 0;
       for (i in finishedSong) {
           if(guessString == finishedSong[i].toLowerCase()){
               wordCount+=1;
               brokeSong[i] = finishedSong[i];
           }
       }

       // If their guess is in the song name, increment wordCount and fill in title
       for (i in songName) {
           if(guessString == songName[i].toLowerCase()){
               wordCount+=1;
               songBlank[i] = songName[i];
           }
       }
       return wordCount;
}

// Clear out a table
function clearTable(tableName){
    var myTable = document.getElementById(tableName);
    var rowCount = myTable.rows.length;
    for (var x=rowCount-1; x>0; x--) {
        myTable.deleteRow(x);
    }
}

// Updates table with guesses
function modifyTable(guessString,wordCount){
    // Get the <tbody>, button and input field elements
    const tableBody = document.getElementById("guessTable").querySelector('tbody');

    // Create a new row
    const newRow = document.createElement('tr');

    // Create three new <td> elements for each column
    const numberCell = document.createElement('td');
    const guessCell = document.createElement('td');
    const hitsCell = document.createElement('td');

    // Add content to the cells
    numberCell.textContent = tableBody.children.length + 1; // Increment row number
    guessCell.textContent = guessString;
    hitsCell.textContent = String(wordCount);

    // Append the cells to the new row
    newRow.appendChild(numberCell);
    newRow.appendChild(guessCell);
    newRow.appendChild(hitsCell);

    // Insert the new row at the top of the table
    tableBody.insertBefore(newRow, tableBody.firstChild);
}

// Update the page main-content whenever a song is loaded in, or a guess was correct
function updatePage() {
    let title = document.getElementById('name');
    let artist = document.getElementById('artist');
    let lyrics = document.getElementById('lyrics');

    // Clear out the page
    title.innerHTML = "";
    artist.innerHTML = "";
    lyrics.innerHTML = "";

    // Display Title
    title.innerHTML += "'";
    for(i in songBlank){ // Iterate through each word
        // Insert a space in front of every word in title except the first
        if(i != 0){ 
            title.innerHTML += " ";
        }

         // If the first index of the word is a blank (accounts for words that start with ' (like 'bout)), display a blank char box for each letter.
         // Otherwise fill in the title if it was guessed.
        if((songBlank[i])[0] == '_'){
            for(char in songBlank[i]){
                title.innerHTML += String.fromCharCode(9608);
            }
        }
        else{
            title.innerHTML += songBlank[i];
        }
    }
    title.innerHTML += "'";

    // Reveal Song Artist - MODIFY IT SO THAT ARTIST ISNT REVEALED DEPENDING ON DIFFICULTY
    artist.innerHTML += songArtist;

    // Format lyrics
    for(i in brokeSong){
        // Add Line Breaks when necessary to separate parts of the song
        if(brokeSong[i] == "~"){
            lyrics.innerHTML += "<br><br>";
        }
        else{
            // If the first index of that character is a blank, the word hasn't been solved yet, and fill page with blanks
            if(((brokeSong[i])[0] == "_") || ((brokeSong[i])[0] == "'" && (brokeSong[i])[1] == '_')){
                for(char in brokeSong[i]){
                    lyrics.innerHTML += String.fromCharCode(9608);
                }
            }
            else{
                lyrics.innerHTML += brokeSong[i]; // Add word by word
            }
            lyrics.innerHTML += " "; // Spaces between each word
        }
    }
}

// Check round win at end of guess
async function roundWin(){
    let titleFinished = true;
    // Check if title was guessed first (win condition)
    for(i in songName){
        if(songName[i] != songBlank[i]){
            titleFinished = false; // Title wasn't guessed
        }
    }
    let lyricsFinished = true;
    // Check if all lyrics were guessed
    for(i in finishedSong){ // Check every word if all the lyrics were filled in
        if(finishedSong[i] != brokeSong[i]){
            lyricsFinished = false;
        }
    }

    // Check win condition
    if(titleFinished || lyricsFinished){
        // Set both unfinished title and lyrics to their finished versions
        songBlank = songName;
        brokeSong = finishedSong;
        // Reload page with updated info
        updatePage();

        // Level Ending Message
        popup.classList.add("open-popup"); // Load instructions popup
        overlay.style.display = 'block';
        let popupHeader = document.getElementById('popup-header');
        let popupText = document.getElementById('popup-text');
        let popupButton = document.getElementById('popup-button');

        popupButton.innerHTML = "Next Level";
        if(level == 1){
            popupHeader.innerHTML = "Congrats you beat today's Easy Level!";
            // Set the new level's variables
            songName = songName2;
            songBlank = songBlank2;
            songArtist = songArtist2;
            finishedSong = finishedSong2;
            brokeSong = brokeSong2;
        }
        else if(level == 2){
            popupHeader.innerHTML = "Congrats you beat today's Medium Level!";
            // Set the new level's variables
            songName = songName3;
            songBlank = songBlank3;
            songArtist = songArtist3;
            finishedSong = finishedSong3;
            brokeSong = brokeSong3;
        }
        else if(level >= 3){
            popupHeader.innerHTML = "Congrats you beat today's Hard Level!";
            popupButton.innerHTML = "See you tomorrow!";
            // Get rid of guess input box when the hard level is beaten
            let  inputDiv = document.querySelector('.input');
            inputDiv.style.display = 'none';
            daily = true;
            hideGiveUpButton();
        }
        let rank = await addLBScore(); // Add user's score to leaderboards
        await getLeaderboardData(level); // Get the updated leaderboard data
        popupText.innerHTML = "You placed rank #${rank}!";
        displayLeaderboard(level); // Display the leaderboard data
        playAudio();
        level += 1; // Progress to next level
    }
    else if(level > 3){
        const overlay = document.querySelector('.overlay')
        overlay.style.display = 'block';
        yesButton();
    }
}

// Play Victory Audio
function playAudio() {
    console.log('plays');
    var audio = new Audio("static/victory.mp3");
    audio.play();
}
  
// Displays the leaderboard on the popup in table format, depending on the level
function displayLeaderboard(level){
    leaderboardDiv.style.display = 'block'; // Display leaderboard in popup
    // Choose the leaderboard to display
    let leaderboard = [];
    if(level == 1){
        leaderboard = leaderboard1;
    }
    else if(level == 2){
        leaderboard = leaderboard2;
    }
    else{
        leaderboard = leaderboard3;
    }
    // Clear the table
    clearTable("leaderboard-table");
    // Get the <tbody>, button and input field elements
    const tableBody = document.getElementById("leaderboard-table").querySelector('tbody');

    // Add everybody to the leaderboard
    for(let i = 0; i < leaderboard.length; i++){
        // Get user and their guesses
        let userName = leaderboard[i][0];
        let userGuesses = leaderboard[i][1];

        // Create a new row
        const newRow = document.createElement('tr');

        // Create new <td> elements for each column
        const nameCell = document.createElement('td');
        const numGuessCell = document.createElement('td');

        // Add content to the cells
        nameCell.textContent = userName;
        numGuessCell.textContent = userGuesses;

        // Append the cells to the new row
        newRow.appendChild(nameCell);
        newRow.appendChild(numGuessCell);

        // Insert the new row at the top of the table
        tableBody.appendChild(newRow);
    }
}

// Sends guessData to DB as a cookie
function sendUserData(usedGuesses){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/updateUser", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"words": usedGuesses, "level": level, "user": username});
    xhr.send(data);

    console.log("sendUsedGuesses function Activated");
    console.log(usedGuesses);
    console.log(level);
    console.log(username);
}

// Sends user score to the DB Leaderboard
async function addLBScore(){
    let points = usedGuesses.length;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/addLBScore", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"cookie": cookieStr, "points": points, "level": level, "username": username});
    xhr.send(data);

    console.log("addLBScore function Activated");
    console.log(username);
    console.log(points);
    console.log(level);
    console.log(cookieStr);
}

// Creates a list of all invalid words the user cannot guess for each game.
// This means words already in the brokeSong. They do not count as guesses.
function listInvalids(){
    invalidWords = []; // clear list
    for(i in brokeSong){
        if(brokeSong[i] == finishedSong[i]){
            invalidWords.push(brokeSong[i].toLowerCase());
        }
    }
}

// When the user is on the last level and it is already skipped/finished
function hideGiveUpButton(){
    const giveUpButton = document.getElementById('give-up-btn');
    giveUpButton.style.visibility = 'hidden'; 
}

// When the user clicks on the "Give Up Button"
function showGiveUpPopUp(){
    //show the overlay and the confirming give up popup
    const giveupPopup = document.getElementById('giveup-popup');
    const overlay = document.querySelector('.overlay')
    overlay.style.display = 'block';
    giveupPopup.style.visibility = 'visible'; 
}

// When the user clicks "Yes" on the Give-Up Popup - Go to next game
function yesButton(){
    const giveupPopup = document.getElementById('giveup-popup');
    const popupHeader = document.getElementById('popup-header');
    const popupText = document.querySelector('#popup-text');
    const popupButton = document.getElementById('popup-button');

    giveupPopup.style.visibility = 'hidden'; 
    songBlank = songName;
    brokeSong = finishedSong;
    updatePage();
    //Change the popup html class for the skip level popup
    popupText.textContent = "";
    popup.classList.add("open-popup")
    popupButton.classList.add("yes-button")
    popupButton.innerHTML = "Next Level";
    if(level == 1){
        popupHeader.innerHTML = "You have skipped today's Easy Level! ";
        popupText.textContent = displayLeaderboard(level);
        // Set the new level's variables
        songName = songName2;
        songBlank = songBlank2;
        songArtist = songArtist2;
        finishedSong = finishedSong2;
        brokeSong = brokeSong2;
    }
    else if(level == 2){
        popupHeader.innerHTML = "You have skipped today's Medium Level!";
        popupText.textContent = displayLeaderboard(level);
        // Set the new level's variables
        songName = songName3;
        songBlank = songBlank3;
        songArtist = songArtist3;
        finishedSong = finishedSong3;
        brokeSong = brokeSong3;
    }
    else if(level >= 3){
        popupHeader.innerHTML = "You have skipped today's Hard Level!";
        popupText.textContent = displayLeaderboard(level);
        popupButton.innerHTML = "Come back tommorow and try again!";
        // Get rid of guess input box when the hard level is beaten
        let inputDiv = document.querySelector('.input');
        inputDiv.style.display = 'none';
        daily = true;
        hideGiveUpButton();
    }
    level += 1;
    usedGuesses = []; // Reset usedGuesses to prepare for next game
    sendUserData(usedGuesses); // Update the cookie data to show they skipped
}

// When the user clicks "No" on the Give-Up Popup - Close the popup and overlay and go back to the main screen
function noButton(){
    const overlay = document.querySelector('.overlay')
    const giveupPopup = document.getElementById('giveup-popup');
    overlay.style.display = 'none';
    giveupPopup.style.visibility = 'hidden'; 
}

function showUsernamePopUp(){
    //show the overlay and the username popup if the user has no name already
    if(username == ""){
        const usernamePopup = document.getElementById('username-popup');
        const overlay = document.querySelector('.overlay')
        overlay.style.display = 'block';
        usernamePopup.style.visibility = 'visible'; 
    }
}

function createUsername(){
    // Manage Player Name - Only give a name if one isn't already given; user can change it while they're still on first level by refreshing
    // close the popup when the form is submitted
    const nameInput = document.querySelector('#name-input');
    let playerName = nameInput.value.toString().toLowerCase().split(" ").join("").replace(/[^a-zA-Z0-9]/g, '').substring(0, 15); // format name input
    if(playerName.length > 15) { // check if playerName is longer than 15 characters
        playerName = playerName.substring(0, 15); // only take the first 15 characters of the name
    }

    if(playerName != ""){
        username = playerName; // Give player their chosen name
    }
    else{
        username = "Player #" + Math.floor(Math.random() * 9002); // Give player a random number between 0-9001
    }
    nameInput.value = ""; // Clear the text box

    // Hide the Popup
    const usernamePopup = document.getElementById('username-popup');
    const overlay = document.querySelector('.overlay')
    overlay.style.display = 'none';
    usernamePopup.style.visibility = 'hidden'; 
    usernamePopup.style.display = 'none'; 
}

// Close popup ; initiates a game start
function closePopup(){
    popup.classList.remove("open-popup");
    overlay.style.display = 'none';
    if(sessionReload == false){ // If session hasn't already been reloaded, attempt to load a cookie
            reloadCookies();
            sessionReload = true;
            updatePage(); // Update the page with new song data
            roundWin(); // Check if user already won this round
    }
    else{
        usedGuesses = []; // Clear used guesses list
        if(level <= 3){
            clearTable("guessTable"); // Empty the guess table
        }
        updatePage(); // Update the page with new song data
    }
    listInvalids(); // Populate a list of all invalid guesses
    
    if(level == 1){
        showUsernamePopUp();
    }
}

// RELOAD COOKIES
function reloadCookies(){
    // If there are guesses from a previous session or they aren't on the first level
    console.log(usedGuesses);
    console.log(level);
    console.log(username);
    if(usedGuesses.length != 0 || level != 1){
        if(level == 2){
            songName = songName2;
            songBlank = songBlank2;
            songArtist = songArtist2;
            finishedSong = finishedSong2;
            brokeSong = brokeSong2;
        }
        else if(level >= 3){
            songName = songName3;
            songBlank = songBlank3;
            songArtist = songArtist3;
            finishedSong = finishedSong3;
            brokeSong = brokeSong3;
        }
        for(i in usedGuesses){
            let guessString = usedGuesses[i];
            // Check the guess with the puzzle
            let wordCount = processGuess(guessString);
            // Update table with guess
            modifyTable(guessString,wordCount);
        }
    }
}

// Gets the leaderboard data from the DB
async function getLeaderboardData(level){
    const reqlb = await fetch('/api/getLB', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"level": level})
    });
    const reqData = await reqlb.json();
    console.log("Leaderboard Data Received");
    if(reqData.length != 0){ // TEMPORARY; to only load in data if there even is data
        if (level == 1){
            leaderboard1 = reqData;
        }
        else if (level == 2){
            leaderboard2 = reqData;
        } else if (level == 3){
            leaderboard3 = reqData;
        }
    }
    console.log(leaderboard1);
}

// Generate a blank space array for a song title
function generateBlank(songName){
    var blankTitle = [];
    for(i in songName){ // Iterate through each word in the title
        let tempString = "";
        for(j in songName[i]){ // Iterate through each letter in the word and make a blank for each
            tempString = tempString.concat('_');
        }
        blankTitle.push(tempString);
    }
    return blankTitle;
}

// Get song data from DB
async function getSongData(){
    const req = await fetch('/api/getDailySongs', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    const reqData = await req.json();
    console.log("Song Data Received");

    // Level 1 Song
    songName = reqData[0]['name'].split(" ");
    songBlank = generateBlank(songName);
    songArtist = reqData[0]['artist'];
    finishedSong = reqData[0]['lyrics'];
    brokeSong = reqData[0]['obfLyrics'];

    console.log("Level 1 Song:");
    console.log(songName);
    console.log(songBlank);
    console.log(songArtist);
    console.log(finishedSong);
    console.log(brokeSong);

    // Level 2 Song
    songName2 = reqData[1]['name'].split(" ");
    songBlank2 = generateBlank(songName2);
    songArtist2 = reqData[1]['artist'];
    finishedSong2 = reqData[1]['lyrics'];
    brokeSong2 = reqData[1]['obfLyrics'];

    console.log("Level 2 Song:");
    console.log(songName2);
    console.log(songBlank2);
    console.log(songArtist2);
    console.log(finishedSong2);
    console.log(brokeSong2);

    // Level 3 Song
    songName3 = reqData[2]['name'].split(" ");
    songBlank3 = generateBlank(songName3);
    songArtist3 = reqData[2]['artist'];
    finishedSong3 = reqData[2]['lyrics'];
    brokeSong3 = reqData[2]['obfLyrics'];

    console.log("Level 3 Song:");
    console.log(songName3);
    console.log(songBlank3);
    console.log(songArtist3);
    console.log(finishedSong3);
    console.log(brokeSong3);
    
}
// SAMPLE DATA BELOW FOR HARD CODED TESTING
let songName= [];
let songBlank = [];
let songArtist = "";
let finishedSong = [];
let brokeSong = [];
let leaderboard1 = [['user1', 'numGuess1'], ['user2', 'numGuess2'], ['user3', 'numGuess3'], ['user4', 'numGuess4'],['user5', 'numGuess5']];


let songName2 = [];
let songBlank2 = [];
let songArtist2 = "";
let finishedSong2 = [];
let brokeSong2 = [];
let leaderboard2 = [['user6', 'numGuess6'], ['user7', 'numGuess7'], ['user8', 'numGuess8'], ['user9', 'numGuess9'],['user10', 'numGuess10']];


let songName3 = [];
let songBlank3 = [];
let songArtist3 = "";
let finishedSong3 =  [];
let brokeSong3 = [];
let leaderboard3 = [['user11', 'numGuess11'], ['user12', 'numGuess12'], ['user13', 'numGuess13'], ['user14', 'numGuess14'],['user15', 'numGuess15']];


// START INITIAL STARTUP CODE
// DO NOT MODIFY
getSongData();

// Load instructions popup and black overlay ; when user closes out popup, page is updated with song info
popup.classList.add("open-popup"); 
const overlay = document.querySelector('.overlay');
overlay.style.display = 'block';
let leaderboardDiv = document.getElementById('leaderboard');

let invalidWords = [];
let sessionReload = false; // Denotes if a session reload has happened already
let daily = false; // Denote whether or not the last level is complete or not

// END INITIAL STARTUP CODE