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
import urandom
from vex import *

brain = Brain()

# --- Deck & Card Functions ---

def create_deck():
    colors = ["Red", "Blue", "Green", "Yellow"]
    numbers = [str(i) for i in range(10)]
    specials = ["Skip", "Rev", "+2"]
    deck = []

    for color in colors:
        deck.append((color, "0"))
        for num in numbers[1:]:
            deck.append((color, num))
            deck.append((color, num))
        for special in specials:
            deck.append((color, special))
            deck.append((color, special))

    for _ in range(4):
        deck.append(("Wild", "Wild"))
        deck.append(("Wild", "+4"))

    return deck

def shuffle_deck(deck):
    for i in range(len(deck) - 1, 0, -1):
        j = urandom.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

def format_card(card):
    color_code = card[0][0]  # 'R', 'B', 'G', 'Y', 'W'
    val = card[1]
    if val == "Skip":
        val = "SK"
    elif val == "Rev":
        val = "RV"
    elif val == "Wild":
        val = "WD"
    return color_code + ":" + val

# --- Display Functions ---

def display_hand(player_hand):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("HAND (" + str(len(player_hand)) + " cards)")
    
    line = 2
    col = 1
    for idx, card in enumerate(player_hand):
        if line > 5:
            break
        brain.screen.set_cursor(line, col)
        card_text = str(idx + 1) + ":" + format_card(card)
        brain.screen.print(card_text)
        
        if col == 1:
            col = 9  # Second column on the 16-char screen
        else:
            col = 1
            line += 1

# --- Top Card Selection Menu ---

def input_top_card():
    colors = ["Red", "Blue", "Green", "Yellow", "Wild"]
    color_idx = 0
    
    # 1. Select Color using Brain Left/Right buttons & Check to confirm
    while not brain.buttonCheck.pressing():
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP CARD COLOR")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Color: " + colors[color_idx])
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[< >] [CHECK:OK]")
        
        if brain.buttonRight.pressing():
            color_idx = (color_idx + 1) % len(colors)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonLeft.pressing():
            color_idx = (color_idx - 1) % len(colors)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        wait(50, MSEC)
        
    while brain.buttonCheck.pressing():
        wait(20, MSEC)
        
    # 2. Select Value using Brain Left/Right buttons & Check to confirm
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Rev", "+2", "Wild", "+4"]
    val_idx = 0
    
    while not brain.buttonCheck.pressing():
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP CARD VALUE")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Value: " + values[val_idx])
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[< >] [CHECK:OK]")
        
        if brain.buttonRight.pressing():
            val_idx = (val_idx + 1) % len(values)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonLeft.pressing():
            val_idx = (val_idx - 1) % len(values)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        wait(50, MSEC)

    while brain.buttonCheck.pressing():
        wait(20, MSEC)

    return (colors[color_idx], values[val_idx])

# --- Turn Logic & Menu ---

def is_valid_move(card, top_card):
    card_color, card_val = card
    top_color, top_val = top_card
    
    if card_color == "Wild":
        return True
    if card_color == top_color or card_val == top_val:
        return True
    return False

def player_turn_menu(deck, player_hand, top_card):
    playable_indices = [i for i, card in enumerate(player_hand) if is_valid_move(card, top_card)]
    
    if not playable_indices:
        # Forced draw
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("NO VALID MOVES!")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Press CHECK")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("to Draw Card")
        
        while not brain.buttonCheck.pressing():
            wait(20, MSEC)
        while brain.buttonCheck.pressing():
            wait(20, MSEC)
            
        if deck:
            drawn_card = deck.pop()
            player_hand.append(drawn_card)
            print("Drew card: " + drawn_card[0] + " " + drawn_card[1])
        return top_card

    # Choose playable card
    select_pos = 0
    while not brain.buttonCheck.pressing():
        current_card_idx = playable_indices[select_pos]
        selected_card = player_hand[current_card_idx]
        
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("PLAY CARD?")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("Top: " + format_card(top_card))
        brain.screen.set_cursor(3, 1)
        brain.screen.print("C" + str(current_card_idx + 1) + ": " + format_card(selected_card))
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[< >] [CHECK]")
        
        if brain.buttonRight.pressing():
            select_pos = (select_pos + 1) % len(playable_indices)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonLeft.pressing():
            select_pos = (select_pos - 1) % len(playable_indices)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        wait(50, MSEC)
        
    while brain.buttonCheck.pressing():
        wait(20, MSEC)
        
    played_card = player_hand.pop(playable_indices[select_pos])
    print("Played: " + played_card[0] + " " + played_card[1])
    return played_card

# --- Main Game Loop ---

def main():
    deck = create_deck()
    shuffle_deck(deck)
    
    # Deal 7 cards
    player_hand = [deck.pop() for _ in range(7)]
    
    # Input top card via Brain buttons
    top_card = input_top_card()
    
    # Run play/draw action via Brain buttons
    top_card = player_turn_menu(deck, player_hand, top_card)
    
    # Display remaining hand on Brain screen
    display_hand(player_hand)
    
    print("\n--- Hand Updated ---")
    for idx, card in enumerate(player_hand, 1):
        print("Card " + str(idx) + ": " + card[0] + " " + card[1])

# Run program
main()