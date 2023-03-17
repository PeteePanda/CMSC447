// Used to add data to the guesses table

// Get the <tbody> element
const tableBody = document.querySelector('table tbody');

// Get the button and input field elements
const addGuessBtn = document.querySelector('#guess-btn');
const guessInput = document.querySelector('#guess-input');

// Add an event listener to the button
addGuessBtn.addEventListener('click', function() {
    event.preventDefault();
    // Create a new row
    const newRow = document.createElement('tr');

    // Create three new <td> elements for each column
    const numberCell = document.createElement('td');
    const guessCell = document.createElement('td');
    const hitsCell = document.createElement('td');

    // Add content to the cells
    numberCell.textContent = tableBody.children.length + 1; // Increment row number
    guessCell.textContent = guessInput.value.toString().toLowerCase(); // Convert guess to lowercase
    hitsCell.textContent = "0"; // Initialize hits to zero

    // Append the cells to the new row
    newRow.appendChild(numberCell);
    newRow.appendChild(guessCell);
    newRow.appendChild(hitsCell);

    // Insert the new row at the top of the table
    tableBody.insertBefore(newRow, tableBody.firstChild);

    // Clear the input field
    guessInput.value = "";
});

// Add function to receive lyric data from database
// Lyric data should be already received as all lowercase