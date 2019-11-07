"""
Game to teach young children arithmetic:

This is an interactive game that teaches 5 to 7 year olds how to add,
subtract, multiply and divide positive integers.

The game supports tailored learning by dynamically adapting its questions
according to the child’s ability to learn as follows:
• If the child answers three consecutive questions correctly, the game
  moves up a level and starts monitoring the child’s answers afresh.
  If the game is already at the highest level, the level remains unchanged.

• If the child answers three consecutive questions incorrectly the game
  moves down a level and starts monitoring the child’s answers afresh.
  If the game is already at lowest level, the level remains unchanged.

The game has seven levels of difficulty, each higher level allows for a
wider range of integers to be used. The lowest level uses the integer
range 1- 4; the next 1- 5; then 1-6, 1-7, 1-8 and so on until 1-10.

Example questions include:
• What is 1 + 4?
• What is 5 * 2?
• What is 8 / 2?
"""

import os
import platform
import random

from classes.history import History
from classes.customExceptions import *

level = 1  # ranges from 1-7 inclusive
hist = History()  # stores correct/incorrect answer history


if platform.system() == "Linux":
    ansiiRed = "\033[1;31m"
    ansiiGreen = "\033[1;32m"
    ansiiBlue = "\033[1;34m"
    ansiiReset = "\033[0;0m"
else:
    ansiiRed = ""
    ansiiGreen = ""
    ansiiBlue = ""
    ansiiReset = ""


# the main menu
menu = ([1, 'addition', '+'],
        [2, 'subtraction', '-'],
        [3, 'multiplication', '*'],
        [4, 'division', '/'],
        [5, 'random sums', '+-*/'],
        [6, 'quit'])


# Begins the game
def main():
    _clear()
    print("Hello, what type of sums would you like to do?\n\n")
    while True:
        _openMenu()


# Opens the main menu once, requests user input and calls the
# appropriate method from the user input.
def _openMenu():
    print("Select one of the following options by typing :\n" + ansiiBlue)
    print("(1) Addition (2) Subtraction (3) Multiplication")
    print("(4) Division (5) Random sums (6) Quit\n" + ansiiReset)

    try:
        selection = input("-->").lower().strip()

        try:
            selection = int(selection)
            try:
                # starts game with correct operators based on menu selection
                _askQuestions(list(filter(lambda x: x[0] == selection, menu))[0][2])
            except IndexError:
                if selection == 6:
                    _endGame()
                else:
                    raise MenuError

        except ValueError:
            try:
                # starts game with correct operators based on menu selection
                _askQuestions(list(filter(lambda x: x[1] == selection, menu))[0][2])
            except IndexError:
                raise MenuError

    except (KeyboardInterrupt, EOFError, MenuError):
        _clear()


# Will reset all variables in preparation to begin asking questions.
# Then, will ask questions until user states they no longer wish to
# to continue.
# 'operators' is a string containing all possible operators to use in
# the generated questions.
def _askQuestions(operators):
    global level
    level = 1
    hist.reset()
    _clear()

    print("Type your answer and then press Enter\n\n")
    while _randQuestion(list(operators)) == True:
        pass

    _clear()
    if hist.totalRight > 1:
        print(ansiiGreen + "Congratulations, you got " + str(hist.totalRight)
              + " correct answers!")
    if hist.highestLevel == 7:
        print("You also reached the highest level in the game! Way to go!")
    elif hist.highestLevel > 1:
        print("You also reached level " + str(hist.highestLevel) + "! Way to go!")
    print("\n" + ansiiReset)
    return


# Generates a random question, from a list of possible operators and
# the current level, asks it, then
# 'operators' is a list of all possible operators to use in
# the generated questions.
def _randQuestion(operators):
    global level
    operator = random.choice(operators)

    while True:
        question = str(random.randint(1, level + 3)) + " " + operator + " " +\
                   str(random.randint(1, level + 3))
        if eval(question) % 1 == 0 and eval(question) >= 0:
            break

    while True:
        try:
            print("Current level: " + ansiiBlue + str(level) + ansiiReset
                  + "\tCorrect answers: " + ansiiGreen + str(hist.totalRight)
                  + ansiiReset + "\n\n")
            print("What is " + ansiiBlue + question + ansiiReset + "?")
            answer = float(input("-->").strip())
            break
        except (KeyboardInterrupt, EOFError, ValueError):
            _clear()
            print("Hmm, I didn't understand that...")
            print("Please type in a number such as 1\n\n")
            continue

    hist.add(answer == eval(question))
    _clear()
    if answer == eval(question):
        if hist.threeRight() and level < 7:
            level += 1
            hist.newLevel()
        print(ansiiGreen + "That is correct, well done!\n\n" + ansiiReset)

    else:
        if hist.threeWrong() and level > 1:
            level -= 1
            hist.newLevel()
        print(ansiiRed + "Not right" + ", the correct answer is:\n\n"
              + ansiiBlue + question + " = " + str(int(eval(question)))
              + ansiiReset + "\n")

    while True:
        print("Press " + ansiiGreen + "Y" + ansiiReset
              + " to try another sum or "
              + ansiiRed + "N" + ansiiReset + " to stop.")
        try:
            choice = input("-->").strip().lower()
            if choice == "y":
                _clear()
                return True
            elif choice == "n":
                return False
                raise BackToMenu
            else:
                _clear()
                continue
        except (EOFError, KeyboardInterrupt):
            _clear()
            continue


# Clears the standard output screen
def _clear():
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        for i in range(100):
            print("\n")


# Exits the program
def _endGame():
    _clear()
    print("Thanks for playing!")
    raise SystemExit


if __name__ == "__main__":
    main()
