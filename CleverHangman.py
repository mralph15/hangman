'''
Description:
        A Hangman game where a greedy algorithm means the computer
        switches up the word on the user to make it harder to guess.

@author: Matthew Ralph
'''

import random

def handleUserInputDebugMode():
    '''
    This function asks the user if they would like to play the
    game in (d)ebug or (p)lay mode, then returns a
    corresponding to their choice.
    '''
    choice = input("Which mode do you want: (d)ebug or (p)lay: ")
    if choice == "d":
        return True
    if choice == "p":
        return False

def handleUserInputWordLength():
    '''
    This function asks the user how many letters
    (between 5-10) they would like to be in the
    secretWord they are to guess.
    '''
    num = input("How many letters in the word you'll guess: ")
    return int(num)

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

def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user,
    using the information in the parameters.
    '''
    letsnotguessed = ""
    for ch in "abcdefghijklmnopqrstuvwxyz":
        if ch in lettersGuessed:
            letsnotguessed += " "
        else:
            letsnotguessed += ch
    line1 = "letters not yet guessed: " + letsnotguessed
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

def createTemplate(currTemplate, letterGuess, word):
    '''
    Given the current template, the letter guessed, and a word
    this functions returns a new template corresponding to
    updated letter passed.
    '''
    new_word = ""
    for ch in word:
        if ch in currTemplate or ch == letterGuess:
            new_word += ch
        else:
            new_word += "_"
    return new_word

def getNewWordList(currTemplate, letterGuess, wordList, debug):
    '''
    Returns a tuple of the new template and list of possible words
    given the current template, letter guess, and list of words.
    If debug mode is on, then will also print all possible templates
    considered and the number of words which was in each.
    '''
    d = {}
    for word in wordList:
        if len(word) == len(currTemplate):
            temp = createTemplate(currTemplate, letterGuess, word)
            if temp not in d:
                d[temp] = [word]
            else:
                d[temp].append(word)
    nword = 0
    bigtemp = ""
    biglist = []
    lst = [(k, v) for (k, v) in d.items()]
    for entry in sorted(lst, key = lambda x: x[0].count("_"),reverse=True):
        if len(entry[1]) > nword:
            nword = len(entry[1])
            bigtemp = entry[0]
            biglist = entry[1]
    ret = []
    if debug == True:
        for (k,v) in d.items():
            ret.append(k + " : " + str(len(v)))
        for item in sorted(ret):
            print(item)
        print("# keys = " + str(len(d)))
    return (bigtemp, biglist)

def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    Returns a list of the misses left after a guessed letter
    and whether or not the letter was in the word.
    '''
    if guessedLetter in hangmanWord:
        return [missesLeft,True]
    else:
        return [missesLeft-1,False]

def findallidx(char, word):
    '''
    Given an character and word, this function returns a list
    of all the indices in which the character appears in the word.
    '''
    indices = []
    idx = -1
    for ch in word:
        idx += 1
        if ch == char:
            indices.append(idx)
    return indices

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
    debug = handleUserInputDebugMode()
    length = handleUserInputWordLength()
    missesLeft = handleUserInputDifficulty()
    max_miss = missesLeft
    currTemplate = "_"*length
    secret = getNewWordList(currTemplate,"",wordsClean,False)
    secretWord = secret[1][random.randint(0,len(secret[1])-1)]
    hangmanWord = ["_" for ch in secretWord]
    lettersGuessed = []

    while missesLeft > 0:
        displayString = createDisplayString(lettersGuessed,missesLeft,hangmanWord)
        if debug == True:
            displayString += "\n" + "(word is " + secretWord + ")" + "\n" + "# possible words: " + str(len(secret[1]))
        guess = handleUserInputLetterGuess(lettersGuessed,displayString)
        lettersGuessed.append(guess)
        secret = getNewWordList(currTemplate,guess,wordsClean,debug)
        secretWord = secret[1][random.randint(0,len(secret[1])-1)]
        currTemplate = secret[0]
        hangmanWord = [ch for ch in secret[0]]
        roundoutcome = processUserGuessClever(guess, hangmanWord, missesLeft)
        if roundoutcome[1] == False:
            missesLeft = roundoutcome[0]
            new_wordsClean = []
            for word in wordsClean:
                if guess not in word:
                    new_wordsClean.append(word)
            wordsClean = new_wordsClean
            print("you missed: " + guess + " not in word")
        if roundoutcome[1] == True:
            new_wordsClean = []
            y = findallidx(guess,currTemplate)
            for word in wordsClean:
                if guess in word:
                    x = findallidx(guess,word)
                    if x == y:
                        new_wordsClean.append(word)
            wordsClean = new_wordsClean
        if hangmanWord.count("_") == 0:
            print("you guessed the word: " + secretWord)
            print("you made " + str(len(lettersGuessed)) + " guesses with " + str(max_miss-missesLeft) + " misses")
            break
    if missesLeft > 0:
        return True
    else:
        print("you're hung!!" + "\n" + "word is " + secretWord)
        print("you made " + str(len(lettersGuessed)) + " guesses with " + str(max_miss) + " misses")
        return False

if __name__ == "__main__":
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
