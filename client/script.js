let usedGuesses = [""]; // Keep track of used guesses

// Used to add data to the guesses table

// Get the <tbody> element
const tableBody = document.querySelector('table tbody');

// Get the button and input field elements
const addGuessBtn = document.querySelector('#guess-btn');
const guessInput = document.querySelector('#guess-input');

// Add an event listener to the submit button
addGuessBtn.addEventListener('click', function() {
    event.preventDefault(); // prevent refresh of page
    let guessString = guessInput.value.toString().toLowerCase().split(" ").join(""); // format guess string
    if(usedGuesses.includes(guessString)){
        console.log("Invalid or used word");
    }
    else{
        // Add word to already guessed words
        usedGuesses.push(guessString)
        // Count the number of hits in the song
        let wordCount = 0;
        for (i in finishedSong) {
            if(guessString == finishedSong[i].toLowerCase()){
                wordCount+=1;
                // Fill in the brokeSong array
                brokeSong[i] = finishedSong[i];
            }
        }
        // If they guess the song name
        if(guessString == songName.toLowerCase()){
            brokeSong = finishedSong; // Fill in the whole lyrics
            songBlank = songName; // Fill in the song name
            wordCount+=1
        }
        // Reload page with updated solution
        updatePage();
        
        // Update table
        modifyTable(guessString,wordCount);
}

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

    // Clear the input field
    guessInput.value = "";
});

// Update the content whenever a song is loaded in, or a guess was correct
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

    // Reveal Song Artist
    artist.innerHTML += songArtist;

    // Format lyrics
    for(i in brokeSong){
        // Add Line Breaks when necessary to separate parts of the song
        if(brokeSong[i] == "~"){
            lyrics.innerHTML += "<br><br>";
        }
        else{
            if((brokeSong[i])[0] == "_"){
                for(char in brokeSong[i]){
                    lyrics.innerHTML += String.fromCharCode(9619);
                }
            }
            else{
                lyrics.innerHTML += brokeSong[i]; // Add word by word or blank if its blank
            }
            lyrics.innerHTML += " ";
        }
    }
    roundWin();
}

// Check round win at end of guess
function roundWin(){
    let finished = true;
    // Check if title was guessed or if all lyrics were guessed
    if(songName != songBlank){
        for(i in finishedSong){
            if(finishedSong[i] != brokeSong[i]){
                finished = false;
            }
        }
    }

    if(finished){
        let title = document.getElementById('name');
        title.innerHTML = "";
        title.innerHTML += "'";
        title.innerHTML += songName; // Fill in title if it was guessed
        title.innerHTML += "'";

        // Level Ending Message
        // Modify text based on level variable
        popup.classList.add("open-popup"); // Load instructions popup
        overlay.style.display = 'block';
        let popupHeader = document.getElementById('popup-header');
        popupHeader.innerHTML = "Congrats you beat the level!";
        let popupText = document.getElementById('popup-text');
        popupText.innerHTML = "You did it.";
        level += 1;
    }
}

// Close instructions popup
function closePopup(){
    popup.classList.remove("open-popup");
    overlay.style.display = 'none';
}


// Requests Data from DB and pulls JSON data and formats it
function requestData(){
    console.log('hi');
}

// Data received:
// Song Name - String
// Song Artist - String
// Percentage Difficulty - String
// Array of strings (completed song)
// Array of strings (lyrics with obfuscated words)


// Load data from database into page (temp data below)
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

// INITIAL STARTUP THINGS
updatePage(); // Initial page update to load lyrics

// Load instructions popup and black overlay
popup.classList.add("open-popup"); 
const overlay = document.querySelector('.overlay');
overlay.style.display = 'block';

let level = 1;