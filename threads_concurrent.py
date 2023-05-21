#!/usr/bin/env python3
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
import random

class ThreadConcurrent:
    """
    This program generates poker hands and asks the user how many
    royal flush hands they would like to draw and how many threads
    they would like to use. (A royal flush is a poker hand that 
    includes the cards '10', 'J', 'Q', 'K', 'A', all being the
    same suit.)
    """
    def __init__(self, lock=True):
        self.lock = threading.Lock() if lock else None
        self.royal_flush_count = 0

    def draw_number_of_royal_flushes(self, num):
        """
        Allows the user to ask for a number of royal flush
        draws. Each time a royal flush is drawn, the 
        royal_flush_count field is updated.
        """
        while self.royal_flush_count < num:
            result = self.draw_hand()
            if result == "Not a royal flush.":
                continue
            else:
                self.royal_flush_count += 1

    def draw_hand(self):
        """
        Creates a new deck (shuffled), then draws
        and returns a hand of five cards to the caller.
        """
        deck = Deck()
        hand = [deck.draw_card() for i in range(5)]
        return hand
        
    def hand_is_royal_flush(self, hand):
        """
        Determines whether param: hand is a royal flush.
        First checks that all cards in the hand are of
        the same suit. Then, the hand is checked to see
        if all the necessary card ranks are present for
        the hand to be a royal flush.
        """
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


class Card:
    def __init__(self, 
                 rank=random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']),
                 suit=random.choice(['Spades', 'Diamonds', 'Clubs', 'Hearts'])):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Creates a string representation of the card
        (used for debugging).
        """
        return str(f'{self.rank}-{self.suit}')
    

class Deck:
    def __init__(self):
        self.cards = self.get_cards(shuffled=True)

    def get_cards(self, shuffled=True):
        """
        Returns a deck of all 52 distinct cards in a standard deck.
        If param: shuffled is True, then the cards are shuffled
        and the newly shuffled deck is returned.
        """
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
        """
        Draws a single card from the deck. If the deck is empty,
        then a new deck is created before drawing a card.
        """
        if self.cards:
            return self.cards.pop()
        else:  # Out of cards; re-shuffle deck
            self.cards = self.get_cards
            return self.cards.pop()


if __name__ == "__main__":
    print(f'\nThis program calculates how long it takes to draw a royal flush' \
        '\n from a deck of cards. A royal flush is a hand of the same suit that' \
        '\n contains the ranks "10", "J", "Q", "K", and "A".\n')
    num_royal_flushes = int(input("How many royal flushes would you like to draw? "))
    num_threads = int(input("How many threads would you like to use? "))
    tc = ThreadConcurrent(lock=True)
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            executor.submit(tc.draw_number_of_royal_flushes, num_royal_flushes)

    total_time = time.time() - start_time
    print(f'It took {total_time} seconds to draw a royal flush.')
