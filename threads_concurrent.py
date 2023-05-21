"""
Citations
https://realpython.com/intro-to-python-threading/
https://www.youtube.com/watch?v=usyg5vbni34
https://stackoverflow.com/questions/905189/why-does-sys-exit-not-exit-when-called-inside-a-thread-in-python
https://superfastpython.com/threadpoolexecutor-wait-all-tasks/
"""

import time
import threading
import concurrent.futures
import sys
import random

class Card:
    def __init__(self, 
                 rank=random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']),
                 suit=random.choice(['Spades', 'Diamonds', 'Clubs', 'Hearts'])):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return str(f'{self.rank}-{self.suit}')
    

class Deck:
    def __init__(self):
        self.cards = self.get_cards(shuffled=True)

    def get_cards(self, shuffled=True):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
        deck = []
        for rank in ranks:
            for suit in suits:
                deck.append(Card(rank=rank, suit=suit))

        if shuffled:
            shuffled_deck = []
            while deck:
                shuffled_deck.append(deck.pop(random.randint(0, len(deck) - 1)))
            deck = shuffled_deck
        return deck
    
    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:  # Out of cards; re-shuffle deck
            self.cards = self.get_cards
            return self.cards.pop()
        


class ThreadConcurrent:
    def __init__(self, lock=True):
        self.lock = threading.Lock() if lock else None
        self.hand_count = 0

    def try_to_draw_royal_flush(self):
        still_trying = True
        while still_trying:
            result = self.draw_hand()
            if result == "Not a royal flush.":
                continue
            else:
                return result

    def try_to_draw_two_consecutive_royal_flushes(self):
        still_trying = True
        while still_trying:
            hand1 = self.draw_hand()
            # print(str(hand1[0]))
            hand2 = self.draw_hand()
            if self.hand_is_royal_flush(hand1) and self.hand_is_royal_flush(hand2):
                return
            else:
                continue

    def draw_hand(self):
        deck = Deck()
        hand = [deck.draw_card() for i in range(5)]
        return hand
        
    def hand_is_royal_flush(self, hand):
        suit = hand[0].suit
        for card in hand:
            if card.suit == suit:
                continue
            else:
                return False
        
        for card in hand:
            if card.rank == '10' or card.rank == 'J' or card.rank == 'Q' \
                    or card.rank == 'K' or card.rank == 'A':
                continue
            else:
                return False
        
        return True


if __name__ == "__main__":
    print(f'\nThis program calculates how long it takes to draw a royal flush' \
        '\n from a deck of cards. A royal flush is a hand of the same suit that' \
        '\n contains the ranks "10", "J", "Q", "K", and "A".\n')
    start_time = time.time()
    num_threads = int(input("How many threads would you like to use? "))
    tc = ThreadConcurrent(lock=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # futures = [executor.submit(tc.try_to_draw_two_consecutive_royal_flushes for i in range(num_threads))]
        # concurrent.futures.wait(futures)
        for i in range(num_threads):
            executor.submit(tc.try_to_draw_two_consecutive_royal_flushes)

    total_time = time.time() - start_time
    print(f'It took {total_time} milliseconds to draw a royal flush.')


    
    
    # print(f'\nThis program allows you to type a sentence one word at a time.' \
    #     '\nTyping words quickly when the lock causes some words to be dropped.' \
    #     '\nIf the lock is on, the sentence will be displayed correctly.\n')
    # ceiling = int(input("Up to what number would you like to calculate the primes? "))
    # num_threads = int(input("How many threads would you like to use? "))
    # region_size = ceiling // num_threads


    # tc = ThreadConcurrent(ceiling, lock=True)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # for i in range(num_threads):
        #     start_index = i * region_size   # Double check for OBOE
        #     end_index = (i + 1) * region_size  # Double check for OBOE
        #     executor.submit(tc.calculate_primes, start_index, end_index)
        #     final = [i for i in range(tc.ceiling + 1) if tc.nums[i]]
        #     print(final)
        
        # futures = [executor.submit(tc.calculate_primes, i * region_size, (i + 1) * region_size) for i in range(num_threads)]
        # concurrent.futures.wait(futures)
        # final = [i for i in range(tc.ceiling + 1) if tc.nums[i]]
        # print(final)
        



# def find_primes(self):
    #     all_nums = [1] * (self.primes_up_to + 1)
    #     all_nums[0], all_nums[1] = 0, 0