from abc import abstractmethod
import time
from random import shuffle


class Strategy:
    @abstractmethod
    def logic(self, orig_word, max_attempt):
        pass


class NoStrategy(Strategy):

    def logic(self, orig_word, max_attempt):
        print("\nSelecting a new word...")
        time.sleep(2)

        partially_guessed_word = ["*" for i in range(0, len(orig_word))]
        previous_guesses = set()

        word_match = False
        remaining_attempts = max_attempt

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


class HintStrategy(Strategy):

    @staticmethod
    def hint_letter(word, partially_guessed_word):
        hinted_letter = ''
        for idx in range(0, len(partially_guessed_word)):
            if partially_guessed_word[idx] == "*":
                partially_guessed_word[idx] = word[idx]
                hinted_letter = word[idx]
                break
        return hinted_letter

    def logic(self, orig_word, max_attempt):
        print("\nThis is a hint-game, you get max 3 hints for every word! Press 9 at anytime to use them.")
        print("Selecting a new word...")
        time.sleep(2)

        partially_guessed_word = ["*" for i in range(0, len(orig_word))]
        previous_guesses = set()
        hint_letters = set()

        word_match = False
        remaining_attempts = max_attempt

        while remaining_attempts > 0 and not word_match:

            print(f"\nWord: {''.join(partially_guessed_word)}")
            print(f"Incorrect Attempts Remaining: {remaining_attempts}")
            print(f"Previous Guesses: {', '.join(previous_guesses)}")
            print(f"Hint Letters: {', '.join(hint_letters)}")

            new_guess = input("Choose the next new letter: ").upper()
            while new_guess in previous_guesses:
                new_guess = input("Choose a different new letter: ").upper()

            if new_guess == '9' and len(hint_letters) < 3:
                hint_letters.add(self.hint_letter(orig_word, partially_guessed_word))
            else:
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


class Context:
    def __init__(self, strategy):
        self._strategy = strategy
        self._max_attempts = 7

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def predict_word(self, orig_word):
        return self._strategy.logic(orig_word, self._max_attempts)

    def run_game(self):
        print("Starting the game...")
        time.sleep(2)
        print(f"You only get {self._max_attempts} incorrect guesses per word.")

        words_list = []
        with open('Words.txt', 'r') as file:
            words_list = [line_word.strip().upper() for line_word in file.readlines()]
        shuffle(words_list)

        for word in words_list[0:5]:
            success = self.predict_word(word)

            if success:
                print(f"Congratulations! You got it right: {word}")
            else:
                print(f"Sorry! Max Attempts Crossed. Better luck next time. The word was: {word}")
