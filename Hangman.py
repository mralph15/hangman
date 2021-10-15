'''
Description:
        A Hangman game that allows the user to play and guess a secret word.

@author: Matthew Ralph
'''

import random

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the
    game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game. 
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12")
    difficulty = input("(h)ard or (e)asy> ")
    if difficulty == "h":
        return 8
    if difficulty == "e":
        return 12

def getWord(words, length):
    '''
    Selects the secret word that the user must guess. 
    This is done by randomly selecting a word from words
    that is of length length.
    '''
    valid_words = []
    for word in words:
        if len(word) == length:
            valid_words.append(word)
    rand_int = random.randint(0,len(valid_words)-1)
    return valid_words[rand_int]

def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user,
    using the information in the parameters.
    '''
    letsguessed = " ".join(sorted(lettersGuessed))
    line1 = "letters you've guessed: " + letsguessed
    line2 = "misses remaining = " + str(missesLeft)
    currentword = " ".join(hangmanWord)
    return line1 + "\n" + line2 + "\n" + currentword

def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and
    checks if it is a repeated letter.
    '''
    print(displayString)
    valid_guess = 0
    while valid_guess != 1:
        guess = input("letter> ")
        if guess in lettersGuessed:
            print("you already guessed that")
        else:
            return guess

def updateHangmanWord(guessedLetter, secretWord, hangmanWord):
    '''
    Updates hangmanWord according to whether guessedLetter
    is in secretWord and where in secretWord guessedLetter is in.
    '''
    new_hangmanWord = []
    secret = [ch for ch in secretWord]
    if secretWord.count(guessedLetter) > 0:
        for let in secret:
            if let in hangmanWord:
                new_hangmanWord.append(let)
            elif let == guessedLetter:
                new_hangmanWord.append(let)
            else:
                new_hangmanWord.append("_")
        return new_hangmanWord
    else:
        return hangmanWord

def processUserGuess(guessedLetter, secretWord, hangmanWord, missesLeft):
    '''
    Uses the information in the parameters to update
    the user's progress in the hangman game.
    '''
    if guessedLetter in secretWord:
        new = updateHangmanWord(guessedLetter, secretWord, hangmanWord)
        return [new, missesLeft, True]
    else:
        return [hangmanWord, missesLeft - 1, False]

def runGame(filename):
    '''
    This function sets up the game, runs each round,
    and prints a final message on whether or not the
    user won. True is returned if the user won the game.
    If the user lost the game, False is returned.
    '''
    f = open(filename, "r")
    wordsClean = [w.strip() for w in f.read().split()]
    f.close()
    length = random.randint(5,10)
    missesLeft = handleUserInputDifficulty()
    max_miss = missesLeft
    secretWord = getWord(wordsClean,length)
    hangmanWord = ["_" for ch in secretWord]
    lettersGuessed = []

    while missesLeft > 0:
        displayString = createDisplayString(lettersGuessed,missesLeft,hangmanWord)
        guess = handleUserInputLetterGuess(lettersGuessed,displayString)
        lettersGuessed.append(guess)
        hangmanWord = updateHangmanWord(guess, secretWord, hangmanWord)
        roundoutcome = processUserGuess(guess,secretWord,hangmanWord,missesLeft)
        if roundoutcome[2] == False:
            missesLeft = roundoutcome[1]
            print("you missed: " + guess + " not in word")
        if hangmanWord.count("_") == 0:
            print("you guessed the word: " + secretWord)
            print("you made " + str(len(lettersGuessed)) + " guesses with " + str(len(lettersGuessed)-missesLeft) + " misses")
            break
    if missesLeft > 0:
        return True
    else:
        print("you're hung!!" + "\n" + "word is " + secretWord)
        print("you made " + str(len(lettersGuessed)) + " guesses with " + str(max_miss) + " misses")
        return False

if __name__ == "__main__":
    '''
    Running Hangman.py should start the game,
    which is done by calling runGame,
    therefore, we have provided you this code below.
    '''
    wins = 0
    loss = 0
    if runGame('lowerwords.txt') == True:
        wins +=1
    else:
        loss +=1
    inp = input("Do you want to play again? y or n> ")
    while inp == "y":
        if runGame('lowerwords.txt') == True:
            wins += 1
        else:
            loss += 1
        inp = input("Do you want to play again? y or n> ")
    print("You won " + str(wins) + " game(s) and lost " + str(loss))