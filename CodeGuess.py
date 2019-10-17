import sqlite3 as lite
import random, time

# Set seed so different each time game played
random.seed(time.time())

# When TAKE_CHANCES is True, the letter chosen will be random, taking into account probabilities
# When TAKE_CHANCES is False, the letter chosen will be the most likely one
TAKE_CHANCES = False

conn = lite.connect("word.db")
c = conn.cursor()


def verify_word():
    word = input("enter a word to verify: \n")
    c.execute("SELECT * FROM words WHERE words=?",(word,))
    verified = c.fetchall()
    if len(verified) > 0:
        print("{} is valid".format(word))
    else:
        print("{} is not valid".format(word))


def game():
    length = int(input("How long is your word? "))
    guess = []
    count = 0
    notin = []
    letters_not_used = []

    for i in range(length):
        guess.append("_")

    found = False
    while found is False:
        # Weighted alphabet means some letters are more likely to be guessed than others
##        weighted_alphabet = {'a':15 , 'b':1, 'c':1, 'd':1, 'e':15, 'f':1, 'g':1, 'h':1, 'i':15, 'j':1, 'k':1, 'l':1, 'm':1, 'n':1, 'o':15, 'p':1, 'q':1, 'r':1, 's':1, 't':1,
##                    'u':15, 'v':1, 'w':1, 'x':1, 'y':7, 'z':1}
        weighted_alphabet = {'a':0 , 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0,
                    'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}

        # Ensure weighted_alphabet doesn't contain any letters already guessed
        for i in notin:
            if i in weighted_alphabet:
                del weighted_alphabet[i]

        # Get list of possible words 
        c.execute("SELECT words FROM words WHERE words LIKE '{}' AND LENGTH(words) = {}".format("".join(guess), len(guess)))
        possible_words = ["".join(ii for ii in i[0].lower() if ii.isalpha()) for i in c.fetchall()]
        temp = list(possible_words)
        # Eliminate any words containing letters not in the word
        for i in possible_words:
            for ii in i:
                if ii in letters_not_used and i in temp:
                    temp.remove(i)
        possible_words = list(temp)
        # Make list of possible letters in the word from list of possible words
        possible_letters = []
        for i in possible_words:
            for ii in i:
                if ii not in possible_letters: possible_letters.append(ii)
        temp = dict(weighted_alphabet)
        # Eliminate any letters from alpbabet which are not in possible_letters
        for i in weighted_alphabet:
            if i not in possible_letters: del temp[i]
        weighted_alphabet = dict(temp)
        # Increase chance of each letter being guessed based on its probability according to the list of possible words
        for i in possible_words:
            for ii in i:
                try:
                    weighted_alphabet[ii] += 1
                except KeyError:
                    pass

        # Make standard alphabet from weighted_alphabet
        alphabet = []
        for i in weighted_alphabet:
            for ii in range(weighted_alphabet[i]):
                alphabet.append(i)
        # If TAKE_CHANCES is True, make a random choice taking into account probabilities
        if TAKE_CHANCES:
            try:
                index = random.randint(0, len(alphabet) -1)
                letter = alphabet[index]
            except ValueError:
                print("no more letters available")
                break
        # If TAKE_CHANCES is False, choose the most likely letter
        else:
            if len(weighted_alphabet) > 0:
                letter = max(weighted_alphabet, key=weighted_alphabet.get)
            else:
                print("no more letters available")
                break

        del weighted_alphabet[letter]
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
            letters_not_used.append(letter)
            notin.append(letter)

        count += 1
