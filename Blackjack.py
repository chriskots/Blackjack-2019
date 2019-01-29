import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

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
        if(card.rank == 'Ace'):
            self.aces += 1
    
    def adjust_for_ace(self):
        if(self.aces > 0 and self.value > 11):
            self.aces -= 1
            self.value -= 10

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How much would you like to bet? '))
        except ValueError:
            print('Please enter a correct type')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        hitStand = input("'h' or 's'")
        if(hitStand == 'h'):
            hit(deck, hand)
        elif(hitStand == 's'):
            playing = False
        else:
            print('Please enter a correct input')
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player, dealer, chips):
    print('Player Busts!')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('Player Wins!')
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print('Dealer Busts!')
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print('Dealer Wins!')
    chips.lose_bet()
    
def push():
    print("Dealer and Player tie! It's a push.")

playing = True
while True:
    # Print an opening statement
    print('Welcome! Get as close to 21 as you can without going over!\nThe dealer will hit until they reach 17. Aces count as 1 or 11')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    playerHand = Hand()
    playerHand.add_card(deck.deal())
    playerHand.add_card(deck.deal())
    
    dealerHand = Hand()
    dealerHand.add_card(deck.deal())
    dealerHand.add_card(deck.deal())
        
    # Set up the Player's chips
    playerChips = Chips()
    
    # Prompt the Player for their bet
    take_bet(playerChips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(playerHand, dealerHand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, playerHand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(playerHand, dealerHand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if(playerHand.value > 21):
            player_busts(playerHand, dealerHand, playerChips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if(playerHand.value <= 21):
        while(dealerHand.value < 17):
            hit(deck,dealerHand)
    
        # Show all cards
        show_all(playerHand, dealerHand)
    
        # Run different winning scenarios
        if dealerHand.value > 21:
            dealer_busts(playerHand,dealerHand,playerChips)
        elif dealerHand.value > playerHand.value:
            dealer_wins(playerHand,dealerHand,playerChips)
        elif dealerHand.value < playerHand.value:
            player_wins(playerHand,dealerHand,playerChips)
        else:
            push(playerHand,dealerHand)
    
    # Inform Player of their chips total 
    print(f'Your new chip total is: {playerChips.total}')
    
    # Ask to play again
    again = input("Play again? 'yes' or 'no' ")
    if(again == 'yes'):
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
