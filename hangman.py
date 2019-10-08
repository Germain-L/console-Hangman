import CodeGuess
import HumanGuess

while True:
    print('\n------------------------------')
    print('1: Computer guesses a word')
    print('------------------------------')
    print('2: You guess a word')
    print('------------------------------')
    print('3: Search if word is available')
    print('------------------------------')

    choice = str(input())
    print("\n")

    if choice == '1':
        CodeGuess.game()
    
    elif choice == '2':
        HumanGuess.game()

    elif choice == '3':
        CodeGuess.verify_word()
    
    else:
        print('invlaid, try again')