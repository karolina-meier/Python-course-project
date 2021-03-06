"""Welcome to Simple Black Jack GAME."""

"""Creating: card (suit, rank, value) ."""

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

    def __init__(self,suit,rank):

        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):

        return self.rank + " of " + self.suit

"""Instantiate a new deck. Shuffle a Deck. Deal Cards From Deck object."""

class Deck:

    def __init__(self):

        self.deck = []

        for suit in suits:
            for rank in ranks:
                #create the Card object
                created_card = Card(suit,rank)
                self.deck.append(created_card)

    def __str__(self):

        return f"Instantiate a new deck of {len(self.deck)} cards"

    def shuffle(self):

        random.shuffle(self.deck)

    def deal(self):

        return self.deck.pop()

class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 #add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:

    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('Please enter how many chips would you like to bet: '))
        except ValueError:
            print('Sorry, a bet must be an integer')
        else:
            if chips.bet > chips.total:
                print("Sorry, don't have enough chips. \nYou have :", chips.total , "chips.")
            else:
                break

def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:
        x = (input("Would you like to Hit? \nEnter y or n: ")).lower()

        if x[0] == 'y':
            hit(deck,hand)
        elif x[0] == 'n':
            print("Player stands. Dealer is playing")
            playing = False
        else:
            print("Incorrect income. Please try again")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print("<card hidden> and ", dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep = '\n')

def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep = '\n')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep = '\n')
    print("Player's Hand =", player.value)

def player_busts(player,dealer,chips):
    print('Player busts!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player wins!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('Dealer busts!')
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('Dealer wins!')
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and Player tie! \nIt's a push.")


while True:
    # Print an opening statement
    print('Welcome to Black Jack! \nGet as close to 21 as you can without going over!\nDealer hits until she reaches 17. \nAces count as 1 or 11.')

    # Create & shuffle the deck, deal two cards to each player

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand,player_chips)
            print("\nPlayer's busted! End of game.",player_chips.total)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value <17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)


    # Inform Player of their chips total
    print("\nPlayer's wins! Your total chips:",player_chips.total)

    # Ask to play again
    new_game = (input("Would you like to play again? \nEnter y or n: ")).lower()

    if new_game[0] == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing!')
        break
