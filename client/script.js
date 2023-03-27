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
            console.log(brokeSong); //testing
        }
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
let finishedSong = ["You're","gonna","hear","me","roar"];
let brokeSong = ["_____","_____","hear","__","roar"];

