import time
from random import shuffle

def game_setup(incorrect_attempts):
    print("Starting a game of Hangman...")
    time.sleep(2)
    print(f"You only get {incorrect_attempts} incorrect guesses per word.")


def read_words_from_file():
    words = []

    with open('Words.txt', 'r') as file:
        words = [line_word.strip().upper() for line_word in file.readlines()]
    return words


def predict_word(orig_word, remaining_attempts):
    print("\nSelecting a new word...")
    time.sleep(2)

    partially_guessed_word = ["*" for i in range(0, len(orig_word))]
    previous_guesses = set()

    word_match = False

    while remaining_attempts > 0 and not word_match:

        print(f"\nWord: {''.join(partially_guessed_word)}")
        print(f"Incorrect Attempts Remaining: {remaining_attempts}")
        print(f"Previous Guesses: {', '.join(previous_guesses)}")

        new_guess = input("Choose the next new letter: ").upper()
        while new_guess in previous_guesses:
            new_guess = input("Choose a different new letter: ").upper()

        previous_guesses.add(new_guess)

        valid_guess = False
        for idx in range(0, len(partially_guessed_word)):
            if partially_guessed_word[idx] == "*" and new_guess == orig_word[idx]:
                partially_guessed_word[idx] = new_guess
                valid_guess = True

        if not valid_guess:
            remaining_attempts -= 1

        word_match = ''.join(partially_guessed_word) == orig_word

    return word_match


def run_game():
    rem_attempts = 7
    game_setup(rem_attempts)
    words_list = read_words_from_file()
    shuffle(words_list)

    for word in words_list[0:5]:
        # print(word)
        rem_attempts = 7
        success = predict_word(word, rem_attempts)

        if success:
            print(f"Congratulations! You got it right: {word}")
        else:
            print(f"Sorry! Max Attempts Crossed. Better luck next time. The word was: {word}")


run_game()
