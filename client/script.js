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
                // Add code to fill in the brokeSong array and reload it on page
                brokeSong[i] = finishedSong[i];
            }
        }
        // Update page
        updatePage();
        console.log(brokeSong); //testing

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

// Add function to receive lyric data from database

// Data received:
// Song Name - String
// Song Artist - String
// Percentage Difficulty - String
// Array of strings (completed song)
// Array of strings (lyrics with obfuscated words)


// Load data from database into page (temp data below)
let songName = "Roar";
let songArtist = "Katy Perry";
let percentDif = "20%";
let finishedSong = ['i', 'used', 'to', 'bite', 'my', 'tongue', 'and', 'hold', 'my', 'breath', 'scared', 'to', 'rock', 'the', 'boat', 'and', 'make', 'a', 'mess', 'so', 'i', 'sat', 'quietly', 'agreed', 'politely', 'i', 'guess', 'that', 'i', 'forgot', 'i', 'had', 'a', 'choice', 'i', 'let', 'you', 'push', 'me', 'past', 'the', 'breaking', 'point', 'i', 'stood', 'for', 'nothing', 'so', 'i', 'fell', 'for', 'everything', '~', 'you', 'held', 'me', 'down,', 'but', 'i', 'got', 'up', '(hey!)', 'already', 'brushing', 'off', 'the', 'dust', 'you', 'hear'];
let brokeSong = ['_', 'used', 'to', 'bite', 'my', '______', 'and', 'hold', 'my', '______', 'scared', 'to', 'rock', 'the', '___', 'and', 'make', 'a', 'mess', 'so', 'i', 'sat', '_______', 'agreed', 'politely', 'i', 'guess', 'that', 'i', 'forgot', 'i', 'had', 'a', 'choice', 'i', 'let', 'you', 'push', 'me', 'past', 'the', 'breaking', 'point', 'i', 'stood', 'for', 'nothing', 'so', 'i', 'fell', 'for', 'everything', '~', 'you', 'held', 'me', 'down,', 'but', 'i', 'got', 'up', '(hey!)', 'already', 'brushing', 'off', 'the', 'dust', 'you', 'hear'];
updatePage();

// Update the page whenever a song is loaded in, or the broke song array is modified
function updatePage() {
    let title = document.getElementById('name');
    let artist = document.getElementById('artist');
    let lyrics = document.getElementById('lyrics');
    console.log('hi');
    // Clear out the page
    title.innerHTML = "";
    artist.innerHTML = "";
    lyrics.innerHTML = "";

    title.innerHTML += "'";
    title.innerHTML += songName;
    title.innerHTML += "'";

    artist.innerHTML += songArtist;

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
}
