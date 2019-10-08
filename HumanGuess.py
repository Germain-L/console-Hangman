import random
import sqlite3 as lite
#imports modules needed by the game

conn = lite.connect("word.db")
c = conn.cursor()
#opens a database which stores 25487 words

def generate():
    c.execute("SELECT * FROM words") #sql command to select everything from db
    rows = c.fetchall() #adds everything selected by sql command into a variable
    
    word = str(rows[random.randint(0, len(rows))][0]).lower()
    #selects a random word form tuple 'rows' but stores it as a tuple so
    #str(row[0]) is needed to convert to str
    #.lower() is used to convert capital letter at start of word
    
    return word


def verify(empty, word):
    wordCheck = "" #creates a new empty variable on each run 
    for i in empty:
        wordCheck += i
    #converts content from empty to string in new variable 

    if wordCheck == word: 
        return True
        #checks if empty (wordCheck here) is equal to the word to guess
        #if it is, function will be True

    elif wordCheck != word:
        return False
        #checks if empty (wordCheck here) is equal to the word to guess
        #if it is, function will be True


def game():
    word = generate() #runs generate function to select a random word

    empty = [] #creates new empty variable
    for i in range(0, len(word)):
        empty.append("_")
        #creates a template of length of the word to guess #
    
    score = 11 #initiates the score to be decreased if player guesses wrong
    while score > 0: 
        print(score, "guesses left") #tells the user how many guesses they have left
        guess = False #sets guess to False for later comparison
        print("word to guess: ", empty) #prints the template of word with guessed letters
        l = input("enter a letter: \n") #user enters a letter to guess

        for j in range(len(word)):
            if word[j] == l:
                empty[j] = l
                guess = True
                #this loop check every letter in the word to guess
                #if it matches guessed letter it replaces it in the template for the user

        if verify(empty, word) == True:
            break
            #checks if word is fully guessed and quits if it is
        
        if guess == False:
            score -= 1
            #if user didn't guess a letter score decreases by 1

        print("\n")

    if score >= 1:
        print(word, "\nyou won")
        #if score is bigger or equal 1, player is comgratulated

    elif score <= 0:
        print("you lost, word was: ", word)
        #if score is bigger or equal to 0, player is told they lost and word is printed

