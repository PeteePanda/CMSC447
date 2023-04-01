
// Get the <tbody>, button and input field elements
const tableBody = document.querySelector('table tbody');
const addGuessBtn = document.querySelector('#guess-btn');
const guessInput = document.querySelector('#guess-input');

// Event Listener to manage a user guesses; activates whenever submit button is clicked
addGuessBtn.addEventListener('click', function() {
    event.preventDefault(); // prevent refresh of page
    let guessString = guessInput.value.toString().toLowerCase().split(" ").join(""); // format guess string

    // Check if word was already guessed
    if(usedGuesses.includes(guessString)){
        console.log("Invalid or used word");
    }
    else{
        // Add word to already guessed words
        usedGuesses.push(guessString)
        // Count the number of hits in the song and fill in the brokeSong array
        let wordCount = 0;
        for (i in finishedSong) {
            if(guessString == finishedSong[i].toLowerCase()){
                wordCount+=1;
                brokeSong[i] = finishedSong[i];
            }
        }

        // If they guess the song name correctly
        if(guessString == songName.toLowerCase()){
            brokeSong = finishedSong; // Fill in the whole lyrics
            songBlank = songName; // Fill in the song name
            wordCount+=1
        }

        // Send updated guess data to DB
        sendCookie(usedGuesses);

        // Update table with guess
        modifyTable(guessString,wordCount);

        // Reload page with updated info
        updatePage();
    }

    // Clear the input field
    guessInput.value = "";
});

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

    // Make the song title blank if it hasnt been guessed yet
    if(songBlank[0] == '_'){
        title.innerHTML += "'";
        for(char in songBlank){
            title.innerHTML += String.fromCharCode(9619);
        }
        title.innerHTML += "'";
    }
    else{
        title.innerHTML += "'";
        title.innerHTML += songBlank; // Fill in title if it was guessed
        title.innerHTML += "'";
    }

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
                    lyrics.innerHTML += String.fromCharCode(9619);
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
    // Check if title was guessed or if all lyrics were guessed
    if(songName != songBlank){ // Check if title was gussed first
        for(i in finishedSong){ // Check every lyric if all the lyrics were filled in
            if(finishedSong[i] != brokeSong[i]){
                finished = false;
            }
        }
    }

    // Check win condition
    if(finished){
        // Fill in title if it was guessed
        let title = document.getElementById('name');
        title.innerHTML = "";
        title.innerHTML += "'";
        title.innerHTML += songName; 
        title.innerHTML += "'";

        // Level Ending Message
        popup.classList.add("open-popup"); // Load instructions popup
        overlay.style.display = 'block';
        let popupHeader = document.getElementById('popup-header');
        let popupText = document.getElementById('popup-text');
        let popupButton = document.getElementById('popup-button');

        popupButton.innerHTML = "Next Level";
        if(level == 1){
            popupHeader.innerHTML = "Congrats you beat today's Easy Level!";
        }
        else if(level == 2){
            popupHeader.innerHTML = "Congrats you beat today's Medium Level!";
        }
        else if(level >= 3){
            popupHeader.innerHTML = "Congrats you beat today's Hard Level! Would you like to replay this level?";
            popupButton.innerHTML = "Replay Level 3";
            level = 3; // Reset level to 3
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

// Close instructions popup
function closePopup(){
    popup.classList.remove("open-popup");
    overlay.style.display = 'none';
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
function sendCookie(usedGuesses){
    // HAS TO BE COMPLETED TO KEEP TRACK OF USER DATA
    console.log("sendCookie function Activated");
}



// SAMPLE DATA BELOW FOR HARD CODED TESTING
let songName = "Roar";
let songBlank = "____";
let songArtist = "Katy Perry";
let percentDif = "20%";
let finishedSong = ['i', 'used', 'to', 'bite', 'my', 'tongue', 'and', 'hold', 'my', 'breath', 'scared', 'to', 'rock', 'the', 'boat', 'and', 'make', 'a', 'mess', 'so', 'i', 'sat', 'quietly', 'agreed', 'politely', 'i', 'guess', 'that', 'i', 'forgot', 'i', 'had', 'a', 'choice', 'i', 'let', 'you', 'push', 'me', 'past', 'the', 'breaking', 'point', 'i', 'stood', 'for', 'nothing', 'so', 'i', 'fell', 'for', 'everything', '~', 'you', 'held', 'me', 'down,', 'but', 'i', 'got', 'up', '(hey!)', 'already', 'brushing', 'off', 'the', 'dust', 'you', 'hear'];
let brokeSong = ['_', 'used', 'to', 'bite', 'my', '______', 'and', 'hold', 'my', '______', 'scared', 'to', 'rock', 'the', '___', 'and', 'make', 'a', 'mess', 'so', 'i', 'sat', '_______', 'agreed', 'politely', '_', 'guess', 'that', '_', 'forgot', 'i', 'had', 'a', 'choice', '_', 'let', 'you', 'push', 'me', 'past', 'the', '________', 'point', 'i', 'stood', 'for', 'nothing', 'so', 'i', '____', 'for', 'everything', '~', 'you', 'held', 'me', 'down,', 'but', 'i', 'got', 'up', '(hey!)', 'already', 'brushing', 'off', '___', 'dust', 'you', 'hear'];

let songName2 = "Flowers";
let songArtist2 = "Miley Cyrus";
let percentDif2 = "20%";
let finishedSong2 = ['i', 'used', 'to', 'bite', 'my', 'tongue', 'and', 'hold', 'my', 'breath', 'scared', 'to', 'rock', 'the', 'boat', 'and', 'make', 'a', 'mess', 'so', 'i', 'sat', 'quietly', 'agreed', 'politely', 'i', 'guess', 'that', 'i', 'forgot', 'i', 'had', 'a', 'choice', 'i', 'let', 'you', 'push', 'me', 'past', 'the', 'breaking', 'point', 'i', 'stood', 'for', 'nothing', 'so', 'i', 'fell', 'for', 'everything', '~', 'you', 'held', 'me', 'down,', 'but', 'i', 'got', 'up', '(hey!)', 'already', 'brushing', 'off', 'the', 'dust', 'you', 'hear'];
let brokeSong2 = ['_', 'used', 'to', 'bite', 'my', '______', 'and', 'hold', 'my', '______', 'scared', 'to', 'rock', 'the', '___', 'and', 'make', 'a', 'mess', 'so', 'i', 'sat', '_______', 'agreed', 'politely', '_', 'guess', 'that', '_', 'forgot', 'i', 'had', 'a', 'choice', '_', 'let', 'you', 'push', 'me', 'past', 'the', '________', 'point', 'i', 'stood', 'for', 'nothing', 'so', 'i', '____', 'for', 'everything', '~', 'you', 'held', 'me', 'down,', 'but', 'i', 'got', 'up', '(hey!)', 'already', 'brushing', 'off', '___', 'dust', 'you', 'hear'];


// START INITIAL STARTUP CODE
// DO NOT MODIFY

updatePage(); // Initial page update to load lyrics
// Load instructions popup and black overlay
popup.classList.add("open-popup"); 
const overlay = document.querySelector('.overlay');
overlay.style.display = 'block';
let level = 1;
let usedGuesses = [""]; // Keep track of used guesses; WILL BE SENT TO DB

// END INITIAL STARTUP CODE