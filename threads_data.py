"""
Citations
https://realpython.com/intro-to-python-threading/
https://www.youtube.com/watch?v=usyg5vbni34
"""

import logging
import time
import threading
import concurrent.futures


class ThreadPractice:
    def __init__(self, lock=False, sleep_time=1.0):
        self.correct_sentence = ""
        self.sentence = ""
        self.lock = threading.Lock() if lock else None
        self.sleep_time = sleep_time

    def run(self):
        running = True
        while running:
            print(f'\nCorrect sentence:\n{self.correct_sentence}')
            print(f'Your sentence:\n{self.sentence}')
            word = str(input("\n(Type 'q' to quit. Must type 'q' for each thread.)\nPlease add another word to the sentence: "))
            if word.lower() == 'q':
                running = False
                break
            if self.lock:
                self.add_word_locked(word)
            else:
                self.add_word_unlocked(word)


    def add_word_unlocked(self, word):
        self.correct_sentence += word + " "
        current_sentence = self.sentence
        current_sentence += word + " "
        time.sleep(self.sleep_time)
        self.sentence = current_sentence

    def add_word_locked(self, word):
        self.correct_sentence += word + " "
        with self.lock:
            current_sentence = self.sentence
            current_sentence += word + " "
            time.sleep(self.sleep_time)
            self.sentence = current_sentence

if __name__ == "__main__":
    print(f'This program .')
    locked_answer = input("Would you like to use a lock? (Please answer 'y' or 'n'): ")
    if locked_answer.lower() == "yes" or locked_answer.lower() == "y":
        locked = True
    else:
        locked = False
    sleep_time = float(input("Enter the number of seconds you would like each addition to sleep: "))
    tp = ThreadPractice(lock=locked, sleep_time=sleep_time)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for i in range(2):
            executor.submit(tp.run)
