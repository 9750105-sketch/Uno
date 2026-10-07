#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

# Create events
FWD = Event()
RT = Event()
LT = Event()

# Functions
def when_started():
    FWD.broadcast_and_wait()
    LT.broadcast_and_wait()
    FWD.broadcast_and_wait()
    RT.broadcast_and_wait()
    FWD.broadcast_and_wait()

def motor1_move_foward():
  #  motor_1.spin_for(FORWARD, 425, DEGREES)
    print("motor1 FWD 425")
def motor5_move_foward():
    #motor_5.spin_for(FORWARD, 425, DEGREES)
    print("motor5 FWD 425")
def motor1_turn_right():
    #motor_1.spin_for(FORWARD, 220, DEGREES)
    print("motor1 FWD 220")
def motor5_turn_right():
   # motor_5.spin_for(REVERSE, 220, DEGREES)
   print("motor5 REV 220")
def motor1_turn_left():
    #motor_1.spin_for(REVERSE, 200, DEGREES)
    print("motor1 REV 220")
def motor5_turn_left():
   # motor_5.spin_for(FORWARD, 220, DEGREES)
    print("motor5 FWD 220")

# Registe callback dunctions to the events 
FWD(motor1_move_foward)
FWD(motor5_move_foward)
RT(motor1_turn_right)
RT(motor5_turn_right)
LT(motor1_turn_left)
LT(motor5_turn_left)
wait(15, MSEC)

# Start the program!
when_started() 

import random
from vex import *

# Initialize VEX EXP Brain
brain = Brain()

# Card definitions
COLORS = ["Red", "Blue", "Green", "Yellow"]
NUMBERS = [str(i) for i in range(10)]  # '0' through '9'
SPECIALS = ["Skip", "Reverse", "Draw 2"]

def create_deck():
    deck = []
    
    # Add colored cards
    for color in COLORS:
        # One '0' per color
        deck.append((color, "0"))
        
        # Two of '1'-'9' and special cards per color
        for num in NUMBERS[1:]:
            deck.append((color, num))
            deck.append((color, num))
            
        for special in SPECIALS:
            deck.append((color, special))
            deck.append((color, special))
            
    # Add Wild cards
    for _ in range(4):
        deck.append(("Wild", "Wild"))
        deck.append(("Wild", "Draw 4"))

    return deck
   
def shuffle_deck(deck):
    # Perform Fisher-Yates shuffle using supported randint
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck     
    import urandom
from vex import *

brain = Brain()



def shuffle_deck(deck):
    for i in range(len(deck) - 1, 0, -1):
        j = urandom.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

def start_game():
    # Setup deck
    deck = create_deck()
    shuffle_deck(deck)
    
    # Draw starting hand of 7 cards
    player_hand = [deck.pop() for _ in range(7)]
    
    # 1. Print starting hand to the console
    print("--- Starting Hand ---")
    for i, card in enumerate(player_hand, 1):
        print(f"Card {i}: {card[0]} {card[1]}")
    print("---------------------\n")
    
    # 2. Print starting hand & info to the VEX EXP screen (5 rows, 16 cols max)
    brain.screen.clear_screen()
    
    # Row 1: Header / Title
    brain.screen.set_cursor(1, 1)
    brain.screen.print("UNO - Hand: 7")
    
    # Rows 2 to 4: Display first 3 cards (abbreviated to fit 16 columns)
    for row_idx in range(3):
        color, value = player_hand[row_idx]
        brain.screen.set_cursor(row_idx + 2, 1)
        # Formats string to stay within 16 characters (e.g. "C1: Red 7")
        card_str = f"C{row_idx+1}: {color[:3]} {value}"
        brain.screen.print(card_str[:16])
        
    # Row 5: Show remaining card count indicator
    brain.screen.set_cursor(5, 1)
    brain.screen.print("+4 more cards...")

    return deck, player_hand

# Run the function
deck, player_hand = start_game()


# --- Test standard setup ---
deck = create_deck()
shuffle_deck(deck)

# Deal initial hands (Player vs Brain AI)
player_hand = [deck.pop() for _ in range(7)]
ai_hand = [deck.pop() for _ in range(7)]
discard_pile = [deck.pop()]

# Display starting state on EXP Brain Screen
brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
brain.screen.print("Top Card:", discard_pile[-1][0], discard_pile[-1][1])
brain.screen.set_cursor(2, 1)
brain.screen.print("Player Cards:")