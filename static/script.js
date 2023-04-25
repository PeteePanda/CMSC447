const addGuessBtn = document.querySelector('#guess-btn');
// Event Listener to manage a user guesses; activates whenever submit button is clicked
addGuessBtn.addEventListener('click', function() {
    event.preventDefault(); // prevent refresh of page
    const guessInput = document.querySelector('#guess-input');
    let guessString = guessInput.value.toString().toLowerCase().split(" ").join(""); // format guess string

    // Check if word was already guessed or response is blank
    if(usedGuesses.includes(guessString)){
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

    for(i in finishedSong) {
        if(guessString == finishedSong[i].toLowerCase() || guessString == finishedSong[i].toLowerCase().slice(-1) || guessString == finishedSong[i].toLowerCase().slice(0) ){
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
    console.log("getting songblank ", songBlank )
    for(i in songBlank){ // Iterate through each word
        // Insert a space in front of every word in title except the first
        if(i != 0){ 
            title.innerHTML += " ";
        }

         // If the first index of the word is a blank, display a blank char box for each letter.
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
            if((brokeSong[i])[0] == "_"){
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
            songBlank = getBlanks();
            songArtist = songArtist2;
            percentDif = percentDif2;
            finishedSong = finishedSong2;
            brokeSong = brokeSong2;
        }
        else if(level == 2){
            popupHeader.innerHTML = "Congrats you beat today's Medium Level!";
            // Set the new level's variables
            songName = songName3;
            songBlank = getBlanks();
            songArtist = songArtist3;
            percentDif = percentDif3;
            finishedSong = finishedSong3;
            brokeSong = brokeSong3;
        }
        else if(level >= 3){
            popupHeader.innerHTML = "Congrats you beat today's Hard Level!";
            popupButton.innerHTML = "See you tomorrow!";
            level = 3; // Reset level to 3
        }
        popupText.innerHTML = "You placed [INSERT RANK HERE].";
        await getLeaderboardData(level);
        displayLeaderboard(level);
        // playAudio();
        level += 1; // Progress to next level
    }
}

function getBlanks(){
    const result = [];
    for (let str of songName) {
        const underscoreStr = "_".repeat(str.length);
        result.push(underscoreStr);
    }
    return result;
}

// function playAudio() {
//     var audio = new Audio("victory.mp3");
//     audio.play();
// }
  
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

// Requests Data from DB and pulls JSON data and formats it
function requestData(){
    // HAS TO BE COMPLETED TO GET SONG DATA FOR GAME

    // Data received (correct if wrong):
    // Song Name - String
    // Song Artist - String
    // Percentage Difficulty - String
    // Array of strings (completed song)
    // Array of strings (lyrics with obfuscated words)

    console.log('requestData() called');
}

// Sends guessData to DB as a cookie
function sendUserData(usedGuesses){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/updateUser", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"words": usedGuesses, "level": level});
    xhr.send(data);

    console.log("sendUsedGuesses function Activated");
    console.log(usedGuesses);
    console.log(level);
}

// Gets the leaderboard data from the DB
async function getLeaderboardData(level){
    const req = await fetch('/api/getLB', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"level": level})
    });
    const reqData = await req.json();
    console.log("Leaderboard Data Received");
    if (level == 1){
        leaderboard1 = reqData;
    }
    else if (level == 2){
        leaderboard2 = reqData;
    } else if (level == 3){
        leaderboard3 = reqData;
    }
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
    console.log("Level 1");
    songName = reqData[0]['name'].split(" ");
    console.log(songName);
    songBlank = getBlanks();
    songArtist = reqData[0]['artist'];
    console.log(songArtist);
    finishedSong = reqData[0]['lyrics'];
    brokeSong = reqData[0]['obfLyrics'];
    console.log(finishedSong);
    console.log(brokeSong);

    console.log("Level 2");
    songName2 = reqData[1]['name'].split(" ");
    console.log(songName2);
    songArtist2 = reqData[1]['artist'];
    console.log(songArtist2);
    finishedSong2 = reqData[1]['lyrics'];
    brokeSong2 = reqData[1]['obfLyrics'];
    console.log(finishedSong2);
    console.log(brokeSong2);

    console.log("Level 3");
    songName3 = reqData[2]['name'].split(" ");
    console.log(songName3);
    songArtist3 = reqData[2]['artist'];
    console.log(songArtist3);
    finishedSong3 = reqData[2]['lyrics'];
    brokeSong3 = reqData[2]['obfLyrics'];
    console.log(finishedSong3);
    console.log(brokeSong3);


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

// Close popup ; initiates a game start
function closePopup(){
    popup.classList.remove("open-popup");
    overlay.style.display = 'none';
    if(sessionReload == false){
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
}

// RELOAD COOKIES
function reloadCookies(){
    // If there are guesses from a previous session or they aren't on the first level
    console.log(usedGuesses);
    console.log(level);
    if(usedGuesses.length != 0 || level != 1){
        if(level == 2){
            songName = songName2;
            songBlank = songBlank2;
            songArtist = songArtist2;
            percentDif = percentDif2;
            finishedSong = finishedSong2;
            brokeSong = brokeSong2;
        }
        else if(level == 3){
            songName = songName3;
            songBlank = songBlank3;
            songArtist = songArtist3;
            percentDif = percentDif3;
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

// SAMPLE DATA BELOW FOR HARD CODED TESTING
let songName = ["Roar"];
let songBlank = ["____"];
let songArtist = "Katy Perry";
let percentDif = "20%";
let finishedSong = ['I', 'used', 'to', 'bite', 'my', 'tongue', 'and', 'hold', 'my', 'breath', 'Scared', 'to', 'rock', 'the', 'boat', 'and', 'make', 'a', 'mess', 'So', 'I', 'sat', 'quietly', 'agreed', 'politely', 'I', 'guess', 'that', 'I', 'forgot', 'I', 'had', 'a', 'choice', 'I', 'let', 'you', 'push', 'me', 'past', 'the', 'breaking', 'point', 'I', 'stood', 'for', 'nothing,', 'so', 'I', 'fell', 'for', 'everything', '~', 'You', 'held', 'me', 'down,', 'but', 'I', 'got', 'up', '(hey)', 'Already', 'brushing', 'off', 'the', 'dust', 'You', 'hear', 'my', 'voice,', 'you', 'hear', 'that', 'sound', 'Like', 'thunder,', 'gonna', 'shake', 'the', 'ground', 'You', 'held', 'me', 'down,', 'but', 'I', 'got', 'up', '(hey)', 'Get', 'ready', "'cause", "I've", 'had', 'enough', 'I', 'see', 'it', 'all,', 'I', 'see', 'it', 'now', '~', 'I', 'got', 'the', 'eye', 'of', 'the', 'tiger,', 'a', 'fighter', 'Dancing', 'through', 'the', 'fire', "'Cause", 'I', 'am', 'a', 'champion,', 'and', "you're", 'gonna', 'hear', 'me', 'roar', 'Louder,', 'louder', 'than', 'a', 'lion', "'Cause", 'I', 'am', 'a', 'champion,', 'and', "you're", 'gonna', 'hear', 'me', 'roar', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh',"You're", 'gonna', 'hear', 'me', 'roar',];
let brokeSong = ['_', '____', 'to', 'bite', '__', '______', 'and', 'hold', '__', '______', '______', 'to', '____', 'the', 'boat', 'and', 'make', 'a', 'mess', 'so', '_', '___', '_______', '______', 'politely', 'i', 'guess', '____', 'i', 'forgot', 'i', 'had', 'a', 'choice', '_', '___', 'you', 'push', '__', '____', 'the', 'breaking', 'point', '_', '_____', 'for', 'nothing', 'so', '_', 'fell', 'for', '__________', '~', '___', 'held', '__', 'down,', 'but', 'i', 'got', '__', '(hey!)', 'already', 'brushing', 'off', 'the', 'dust', '___', 'hear', '__', 'voice,', 'you', '____', '____', '_____', 'like', 'thunder', '_____', '_____', 'the', 'ground', 'you', 'held', '__', '_____', 'but', 'i', '___', '__', '_____', 'get', 'ready', '______', "i've", 'had', '______', 'i', 'see', '__', 'all,', 'i', 'see', '__', 'now', '~','i', '___', 'the', '___', '__', '___', '_____', 'a', 'fighter', 'dancing', '_______', '___', 'fire', "'cause", '_', 'am', 'a', '________', '___', '______', '_____', '____', 'me', '____', '_______', '______', 'than', 'a', '____', '______', 'i', 'am', '_', 'champion', '___', "you're", '_____', '____', 'me', '____', '__', 'oh', 'oh', '__', '__', '__', '__', '__', 'oh', '__', 'oh', 'oh', '__', 'oh', 'oh', 'oh', '__', '__', 'oh', 'oh', 'oh', '______', 'gonna', '____', 'me', '____'];
let leaderboard1 = [['user1', 'numGuess1'], ['user2', 'numGuess2'], ['user3', 'numGuess3'], ['user4', 'numGuess4'],['user5', 'numGuess5']];


let songName2 = ["Flowers"];
let songBlank2 = ["_______"];
let songArtist2 = "Miley Cyrus";
let percentDif2 = "50%";
let finishedSong2 =  ['i', 'can', 'buy', 'myself', 'flowers'];
let brokeSong2 = ['i', '___', 'buy', 'myself', '_______'];
let leaderboard2 = [['user6', 'numGuess6'], ['user7', 'numGuess7'], ['user8', 'numGuess8'], ['user9', 'numGuess9'],['user10', 'numGuess10']];


let songName3 = ["Just", "The", "Way", "You", "Are"];
let songBlank3 = ["____", "___", "___", "___", "___"];
let songArtist3 = "Bruno Mars";
let percentDif3 = "80%";
let finishedSong3 =  ['her', 'eyes', 'her', 'eyes', 'make', 'the', 'stars', 'look', 'like', "they're", 'not', 'shining'];
let brokeSong3 = ['___', 'eyes', '___', 'eyes', '____', '___', '_____', 'look', '____', "they're", 'not', '_______'];
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

// END INITIAL STARTUP CODE