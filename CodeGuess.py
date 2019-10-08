import sqlite3 as lite
import random

conn = lite.connect("word.db")
c = conn.cursor()


def verify_word():
    word = input("enter a word to verify: \n")
    c.execute("SELECT * FROM words WHERE words=?",(word,))
    verified = c.fetchall()
    if verified != "":
        print(word+"is valid")


def game():
    length = int(input("How long is your word? "))
    guess = []
    count = 0
    notin = []

    for i in range(length):
        guess.append("_")

    found = False
    while found is False:
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']

        for i in notin:
            if i in alphabet:
                alphabet.remove(i)
        try:
            index = random.randint(0, len(alphabet) -1)
        except ValueError:
            print("no more letters available")
            break

        letter = alphabet[index]
        alphabet.remove(letter)
        q = "is '"+ letter+ "' in your word? (y/n)"
        is_in  = input(q)
        if is_in == "y":
            notin.append(letter)
            loop = True
            while loop is True:
                position = int(input("In what position? (first letter being at 1): "))
                guess[position-1] = letter
                print(guess)
                other = input("any other? (y/n)")
                if other == "n":
                    loop = False
                else:
                    continue

            query = ""
            for i in guess:
                query += i

            c.execute("SELECT words FROM words WHERE words LIKE ?", (query,))
            listwords = c.fetchall()
            if len(listwords) == 0:
                print("no words matching in databse")
                break

            if len(listwords) == 1:
                print(listwords[0][0], " guessed in ", count, " rounds")
                break

            listwords = []
            alphabet.clear()
            for t in listwords:
                for w in t:
                    listwords.append(w.lower())

            for i in alphabet:
                for j in i:
                    if j not in alphabet:
                        alphabet.append(j)

        elif is_in == "n":
            notin.append(letter)

        count += 1