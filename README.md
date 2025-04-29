Crossword Puzzler
A terminal-based interactive crossword puzzle game written in Python. This game allows players to load a crossword file, guess answers, reveal clues, get hints, and more — all through a simple command-line interface.

Features
Load and play crossword puzzles from external files

Display across and down clues

Make guesses and receive immediate feedback

Reveal answers or get hints for incorrect guesses

Restart or quit the game anytime

User-friendly help menu with available commands

Requirements
Python 3.x

A valid puzzle file in the format accepted by the Crossword class (from crossword.py)

Usage
Running the Game
Make sure crossword.py is in the same directory. Then run:

bash
Copy
Edit
python3 main.py
When prompted, enter the filename of the crossword puzzle you want to play.

Controls & Commands

Command	Format	Description
C n	C 5	Show first n across and down clues. Use C 0 to show all clues.
G	G i j A/D	Make a guess for the clue starting at row i, column j, direction A (across) or D (down).
R	R i j A/D	Reveal the full answer for the clue.
T	T i j A/D	Give a hint: shows the first incorrect letter in your guess.
H		Show help menu.
S		Restart the game with a new puzzle file.
Q		Quit the game.
Example
vbnet
Copy
Edit
Enter the filename of the puzzle you want to play: sample_puzzle.txt
Across
1. A fruit that's red
2. Opposite of no

Down
1. Used to write
2. Canine animal

Enter option: G 0 1 A
Enter your guess (use _ for blanks): apple
Input Validation
Coordinates i and j must be integers between 0 and 4.

Direction must be 'A' or 'D'.

Guess length must match the length of the clue.

Project Structure
bash
Copy
Edit
.
├── main.py         # Main game loop and logic
├── crossword.py    # Crossword puzzle class and logic
├── sample_puzzle.txt  # Example puzzle file (user-provided)
└── README.md       # This file
Notes
This project assumes the Crossword class and its methods (change_guess, reveal_answer, find_wrong_letter, is_solved, etc.) are defined in crossword.py.

The game operates entirely in the terminal — no GUI elements are used.

