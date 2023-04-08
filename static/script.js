
// Get the <tbody>, button and input field elements
const tableBody = document.querySelector('table tbody');
const addGuessBtn = document.querySelector('#guess-btn');
const guessInput = document.querySelector('#guess-input');

// Event Listener to manage a user guesses; activates whenever submit button is clicked
addGuessBtn.addEventListener('click', function() {
    event.preventDefault(); // prevent refresh of page
    let guessString = guessInput.value.toString().toLowerCase().split(" ").join(""); // format guess string

    // Check if word was already guessed or response is blank
    if(usedGuesses.includes(guessString) || (guessString == "")){
        console.log("Invalid or used word");
    }
    else{
        // Add word to already guessed words
        usedGuesses.push(guessString);

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
        
        // Send updated guess data to DB
        sendUserData(usedGuesses);

        // Update table with guess
        modifyTable(guessString,wordCount);

        // Reload page with updated info
        updatePage();
    }

    // Clear the input field
    guessInput.value = "";
});

// Clear out guesses table
function clearTable(){
    var myTable = document.getElementById("guessTable");
    var rowCount = myTable.rows.length;
    for (var x=rowCount-1; x>0; x--) {
        myTable.deleteRow(x);
    }
}

// Updates table with guesses
function modifyTable(guessString,wordCount){
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
    // Check win condition
    roundWin();
}

// Check round win at end of guess
function roundWin(){
    let finished = true;
    // Check if title was guessed first
    for(i in songName){
        if(songName[i] != songBlank[i]){
            finished = false;
        }
    }
    // If title wasn't fully guessed, check if all lyrics were guessed
    if(finished == false){
        for(i in finishedSong){ // Check every lyric if all the lyrics were filled in
            if(finishedSong[i] != brokeSong[i]){
                finished = false;
            }
        }
    }

    // Check win condition
    if(finished){
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
            percentDif = percentDif2;
            finishedSong = finishedSong2;
            brokeSong = brokeSong2;
        }
        else if(level == 2){
            popupHeader.innerHTML = "Congrats you beat today's Medium Level!";
            // Set the new level's variables
            songName = songName3;
            songBlank = songBlank3;
            songArtist = songArtist3;
            percentDif = percentDif3;
            finishedSong = finishedSong3;
            brokeSong = brokeSong3;
        }
        else if(level >= 3){
            popupHeader.innerHTML = "Congrats you beat today's Hard Level!";
            popupButton.innerHTML = "Replay Level 3";
            level = 3; // Reset level to 3
            // TEAM DECIDES WHAT TO DO AFTER HARD LEVEL IS BEAT
        }
        popupText.innerHTML = "Here's the leaderboard info in table format";
        displayLeaderboard(level);
        level += 1; // Progress to next level
    }
}

// Displays the leaderboard on the popup in table format, depending on the level
function displayLeaderboard(level){
    console.log('displayLeaderboard() called');
}

// Close popup
function closePopup(){
    popup.classList.remove("open-popup");
    overlay.style.display = 'none';
    updatePage(); // Update the page with new song data
    usedGuesses = []; // Clear used guesses list
    clearTable(); // Empty the table
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



// SAMPLE DATA BELOW FOR HARD CODED TESTING
let songName = ["Roar"];
let songBlank = ["____"];
let songArtist = "Katy Perry";
let percentDif = "20%";
let finishedSong = ['I', 'used', 'to', 'bite', 'my', 'tongue', 'and', 'hold', 'my', 'breath', 'Scared', 'to', 'rock', 'the', 'boat', 'and', 'make', 'a', 'mess', 'So', 'I', 'sat', 'quietly,', 'agreed', 'politely', 'I', 'guess', 'that', 'I', 'forgot', 'I', 'had', 'a', 'choice', 'I', 'let', 'you', 'push', 'me', 'past', 'the', 'breaking', 'point', 'I', 'stood', 'for', 'nothing,', 'so', 'I', 'fell', 'for', 'everything', '~', 'You', 'held', 'me', 'down,', 'but', 'I', 'got', 'up', '(hey)', 'Already', 'brushing', 'off', 'the', 'dust', 'You', 'hear', 'my', 'voice,', 'you', 'hear', 'that', 'sound', 'Like', 'thunder,', 'gonna', 'shake', 'the', 'ground', 'You', 'held', 'me', 'down,', 'but', 'I', 'got', 'up', '(hey)', 'Get', 'ready', "'cause", "I've", 'had', 'enough', 'I', 'see', 'it', 'all,', 'I', 'see', 'it', 'now', '~', 'I', 'got', 'the', 'eye', 'of', 'the', 'tiger,', 'a', 'fighter', 'Dancing', 'through', 'the', 'fire', "'Cause", 'I', 'am', 'a', 'champion,', 'and', "you're", 'gonna', 'hear', 'me', 'roar', 'Louder,', 'louder', 'than', 'a', 'lion', "'Cause", 'I', 'am', 'a', 'champion,', 'and', "you're", 'gonna', 'hear', 'me', 'roar', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh', 'oh',"You're", 'gonna', 'hear', 'me', 'roar',];
let brokeSong = ['_', '____', 'to', 'bite', '__', '______', 'and', 'hold', 'my', '______', '______', 'to', '____', 'the', 'boat', 'and', 'make', 'a', 'mess', 'so', '_', '___', '_______', '______', 'politely', 'i', 'guess', '____', 'i', 'forgot', 'i', 'had', '_', 'choice', '_', '___', 'you', 'push', '__', '____', 'the', 'breaking', 'point', '_', '_____', 'for', 'nothing', 'so', '_', 'fell', 'for', '__________', '~', '___', 'held', '__', 'down,', 'but', 'i', 'got', '__', '(hey!)', 'already', 'brushing', 'off', 'the', 'dust', '___', 'hear', '__', 'voice,', 'you', '____', '____', '_____', 'like', 'thunder', '_____', '_____', 'the', 'ground', 'you', 'held', '__', '_____', 'but', 'i', '___', '__', '_____', 'get', 'ready', '______', "i've", 'had', '______', 'i', 'see', '__', 'all,', 'i', 'see', '__', 'now', '~','i', '___', 'the', '___', '__', '___', '_____', 'a', 'fighter', 'dancing', '_______', '___', 'fire', "'cause", '_', 'am', 'a', '________', '___', '______', '_____', '____', 'me', '____', '_______', '______', 'than', 'a', '____', '______', 'i', 'am', '_', 'champion', '___', "you're", '_____', '____', 'me', '____', '__', 'oh', 'oh', '__', '__', '__', '__', '__', 'oh', '__', 'oh', 'oh', '__', 'oh', 'oh', 'oh', '__', '__', 'oh', 'oh', 'oh', '______', 'gonna', '____', 'me', '____'];

let songName2 = ["Flowers"];
let songBlank2 = ["_______"];
let songArtist2 = "Miley Cyrus";
let percentDif2 = "50%";
let finishedSong2 =  ['i', 'can', 'buy', 'myself', 'flowers'];
let brokeSong2 = ['i', '___', 'buy', 'myself', '_______'];

let songName3 = ["Just", "The", "Way", "You", "Are"];
let songBlank3 = ["____", "___", "___", "___", "___"];
let songArtist3 = "Bruno Mars";
let percentDif3 = "80%";
let finishedSong3 =  ['her', 'eyes', 'her', 'eyes', 'make', 'the', 'stars', 'look', 'like', "they're", 'not', 'shining'];
let brokeSong3 = ['___', 'eyes', '___', 'eyes', '____', 'the', '_____', 'look', '____', "they're", 'not', '_______'];


// START INITIAL STARTUP CODE
// DO NOT MODIFY

// GET RID OF BEFORE MERGE
let usedGuesses = [];
let level = 1;

// Load instructions popup and black overlay ; when user closes out popup, page is updated with song info
popup.classList.add("open-popup"); 
const overlay = document.querySelector('.overlay');
overlay.style.display = 'block';


// END INITIAL STARTUP CODE