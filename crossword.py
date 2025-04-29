

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):
      """
        Changes the current guess for the given clue on the board.

        Parameters:
            clue (Clue): The clue object representing the clue for which the guess is being changed.
            new_guess (str): The new guess to be placed on the board.

        Raises:
            RuntimeError: If the length of the new guess does not match the length of the clue's answer,
                          or if the new guess contains invalid characters.

        Returns:
            None
      """
      row, column, down_across= clue.indices[0], clue.indices[1], clue.down_across
      i = 0
      if len(new_guess) == len(clue.answer) and all(ch in GUESS_CHARS for ch in new_guess):
          while i < len(new_guess):
              if down_across == 'A':
                  self.board[row][column + i] = new_guess[i]
              else:
                  self.board[row + i][column] = new_guess[i]
              i += 1
      elif len(new_guess) != len(clue.answer):
          raise RuntimeError("Guess length does not match the length of the clue.\n")
      elif not all(ch in GUESS_CHARS for ch in new_guess):
          raise RuntimeError("Guess contains invalid characters.\n")
      return None


    def reveal_answer(self, clue):
        """
        Reveals the answer of the given clue on the board.

        Parameters:
            clue (Clue): The clue object representing the clue for which the answer is being revealed.

        Returns:
            None
        """
        row, column, down_across = clue.indices[0], clue.indices[1], clue.down_across
        i = 0
        while i < len(clue.answer):
            if down_across == 'A':
                self.board[row][column + i] = clue.answer[i]
            else:
                self.board[row + i][column] = clue.answer[i]
            i += 1

    def find_wrong_letter(self, clue):
        """
        Finds the index of the first wrong letter in the current guess for the given clue.

        Parameters:
            clue (Clue): The clue object representing the clue for which the wrong letter is being searched.

        Returns:
            int: The index of the first wrong letter in the current guess for the given clue.
                 Returns -1 if all letters in the guess are correct.
        """
        row, column, down_across = clue.indices[0], clue.indices[1], clue.down_across
        i = 0
        while i < len(clue.answer):
            if down_across == 'A':
                if self.board[row][column + i] != clue.answer[i]:
                    return i
            else:
                if self.board[row + i][column] != clue.answer[i]:
                    return i
            i += 1
        return -1
    def is_solved(self):
        """
        Checks if the crossword puzzle is solved.

        Returns:
            bool: True if all clues have been correctly guessed, False otherwise.
        """
        for key in self.clues:
            if self.find_wrong_letter(self.clues[key]) != -1:
                return False
        return True

