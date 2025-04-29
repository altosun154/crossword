""" Source header """

from crossword import Crossword
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"
"\nAcross"
"\nDown"
"\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
"Invalid option/arguments. Type 'H' for help."
"Enter your guess (use _ for blanks): "
"This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")

def input( prompt=None ):
    """
      DO NOT MODIFY: Uncomment this function when submitting to Codio
      or when using the run_file.py to test your code.
      This function is needed for testing in Codio to echo the input to the output
      Function to get user input from the standard input (stdin) with an optional prompt.
      Args:
          prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
      Returns:
          str: The user input received from stdin.
    """
    if prompt:
        print( prompt, end="" )
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip( "\n" )
    print( aaa_str )
    return aaa_str


# DEFINE YOUR FUNCTIONS HERE
def open_file():
    """
    Opens a crossword puzzle file.

    Asks the user for a filename and attempts to create a Crossword object with it.
    If the file is not found, it displays an error message and prompts the user again.

    Returns:
        Crossword: A Crossword object representing the crossword puzzle from the file.
    """
    while True:
        try:
            filename = input(PUZZLE_PROMPT)
            crossword = Crossword(filename)
            return crossword
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)

def display_clues(crossword, num_clues):
    """
    Displays sorted across and down clues from the crossword.

    Parameters:
        crossword (Crossword): The Crossword object containing the clues to be displayed.
        num_clues (int): The number of clues to be displayed. If set to 0, displays all available clues.

    Returns:
        None
    """
    across_clues = []
    down_clues = []
    for clue in crossword.clues.values():
        if clue.down_across == 'A':
            across_clues.append(clue)
        else:
            down_clues.append(clue)
    across_clues.sort()
    down_clues.sort()
    if num_clues == 0 or num_clues > len(across_clues):
        num_clues = len(across_clues)
    print("\nAcross")
    for i in range(num_clues):
        print(f"{across_clues[i]}")
    if num_clues == 0 or num_clues > len(down_clues):
        num_clues = len(down_clues)
    print("\nDown")
    for i in range(num_clues):
        print(f"{down_clues[i]}")

def validate_commands(crossword, commands):
    """
    Validates the commands entered by the user.

    Parameters:
        crossword (Crossword): The Crossword object containing the crossword puzzle.
        commands (str): The user input commands to be validated.

    Returns:
        list or None: A validated list of commands if input is valid, otherwise None.
    """
    commands = commands.split()
    if commands[0] == 'C':
        if len(commands) == 2 and commands[1].isdigit():
            return commands
    elif commands[0] in ['H', 'S', 'Q']:
        if len(commands) == 1:
            return commands
    elif commands[0] in ['G', 'R', 'T']:
        if len(commands) == 4 and commands[1].isdigit() and commands[2].isdigit() and commands[3] in ['A', 'D'] and int(commands[1]) in range(5) and int(commands[2]) in range(5):
            if (int(commands[1]), int(commands[2]), commands[3]) in crossword.clues:
                return commands
    return None






def main():
    # Open the crossword puzzle file and display initial information
    crossword = open_file()
    display_clues(crossword, 5)
    print(crossword)
    print(HELP_MENU)

    # Continue prompting the user for commands until the puzzle is solved or the user quits
    while not crossword.is_solved():
        commands = input(OPTION_PROMPT)
        commands = validate_commands(crossword, commands)

        # Handle invalid commands
        if not commands:
            print("Invalid option/arguments. Type 'H' for help.")
            continue

        # Process valid commands
        if commands[0] == 'C':
            display_clues(crossword, int(commands[1]))
        elif commands[0] == 'G':
            clue = crossword.clues[(int(commands[1]), int(commands[2]), commands[3])]
            while True:
                guess = input("Enter your guess (use _ for blanks): ")
                guess = guess.upper()
                try:
                    crossword.change_guess(clue, guess)
                    print(crossword)
                    break
                except RuntimeError as error_msg:
                    print(error_msg)
        elif commands[0] == 'R':
            clue = crossword.clues[(int(commands[1]), int(commands[2]), commands[3])]
            crossword.reveal_answer(clue)
            print(crossword)
        elif commands[0] == 'T':
            clue = crossword.clues[(int(commands[1]), int(commands[2]), commands[3])]
            wrong_letter = crossword.find_wrong_letter(clue)
            if wrong_letter != -1:
                print("Letter {} is wrong, it should be {}".format(int(wrong_letter) + 1, clue.answer[wrong_letter]))
            else:
                print("This clue is already correct!")
        elif commands[0] == 'H':
            print(HELP_MENU)
        elif commands[0] == 'S':
            crossword = open_file()
            display_clues(crossword, 5)
            print(crossword)
            print(HELP_MENU)
        elif commands[0] == 'Q':
            break

    # Check if the puzzle is solved and print a congratulatory message
    if crossword.is_solved():
        print("\nPuzzle solved! Congratulations!")


if __name__ == "__main__":
    main()
