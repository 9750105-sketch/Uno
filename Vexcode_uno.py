import urandom
from vex import *

brain = Brain()

# --- Drivetrain Movement Functions ---
# Adjust distance and speed variables based on your robot's physical setup

def drive_forward_step():
    # Drives forward one standard unit/tile
    # Example: drivetrain.drive_for(FORWARD, 200, MM)
    print("Driving Forward...")
    wait(500, MSEC)

def turn_left_90():
    # Turns 90 degrees left
    # Example: drivetrain.turn_for(LEFT, 90, DEGREES)
    print("Turning Left 90 Deg...")
    wait(500, MSEC)

def turn_right_90():
    # Turns 90 degrees right
    # Example: drivetrain.turn_for(RIGHT, 90, DEGREES)
    print("Turning Right 90 Deg...")
    wait(500, MSEC)

def drive_to_center():
    # Drive 2 units forward to reach the center discard table
    print("\n--- Moving to Center ---")
    drive_forward_step()
    drive_forward_step()

def drive_back_to_player():
    # Turn around (two 90-degree turns) and drive back 2 units
    print("\n--- Returning to Player ---")
    turn_right_90()
    turn_right_90()
    drive_forward_step()
    drive_forward_step()
    # Turn back around to face forward again
    turn_right_90()
    turn_right_90()

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

# --- Display & Input Helpers ---

def wait_for_release():
    while brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing():
        wait(20, MSEC)

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
            col = 9
        else:
            col = 1
            line += 1

# --- Top Card Selection Menu ---

def input_top_card():
    colors = ["Red", "Blue", "Green", "Yellow", "Wild"]
    color_idx = 0
    needs_redraw = True
    
    while not brain.buttonCheck.pressing():
        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("TOP CARD COLOR")
            brain.screen.set_cursor(3, 1)
            brain.screen.print("Color: " + colors[color_idx])
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[< >] [CHECK:OK]")
            needs_redraw = False
        
        if brain.buttonRight.pressing():
            color_idx = (color_idx + 1) % len(colors)
            needs_redraw = True
            wait_for_release()
        elif brain.buttonLeft.pressing():
            color_idx = (color_idx - 1) % len(colors)
            needs_redraw = True
            wait_for_release()
        wait(20, MSEC)
        
    wait_for_release()
        
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Rev", "+2", "Wild", "+4"]
    val_idx = 0
    needs_redraw = True
    
    while not brain.buttonCheck.pressing():
        if needs_redraw:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("TOP CARD VALUE")
            brain.screen.set_cursor(3, 1)
            brain.screen.print("Value: " + values[val_idx])
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[< >] [CHECK:OK]")
            needs_redraw = False
        
        if brain.buttonRight.pressing():
            val_idx = (val_idx + 1) % len(values)
            needs_redraw = True
            wait_for_release()
        elif brain.buttonLeft.pressing():
            val_idx = (val_idx - 1) % len(values)
            needs_redraw = True
            wait_for_release()
        wait(20, MSEC)

    wait_for_release()
    return (colors[color_idx], values[val_idx])

# --- Turn Logic & Driving Actions ---

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
        brain.screen.print("Press CHECK to")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("Drive & Draw")
        
        while not brain.buttonCheck.pressing():
            wait(20, MSEC)
        wait_for_release()
        
        # 1. Robot drives to center
        drive_to_center()
        
        # 2. Draw card action
        if deck:
            drawn_card = deck.pop()
            player_hand.append(drawn_card)
            print("Drew card at center: " + drawn_card[0] + " " + drawn_card[1])
            
        # 3. Robot returns to player
        drive_back_to_player()
        
        return top_card

    # Choose playable card
    select_pos = 0
    needs_redraw = True
    
    while not brain.buttonCheck.pressing():
        if needs_redraw:
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
            needs_redraw = False
        
        if brain.buttonRight.pressing():
            select_pos = (select_pos + 1) % len(playable_indices)
            needs_redraw = True
            wait_for_release()
        elif brain.buttonLeft.pressing():
            select_pos = (select_pos - 1) % len(playable_indices)
            needs_redraw = True
            wait_for_release()
        wait(20, MSEC)
        
    wait_for_release()
    
    # 1. Robot drives to center to discard
    drive_to_center()
    
    # 2. Discard card action
    played_card = player_hand.pop(playable_indices[select_pos])
    print("Discarded at center: " + played_card[0] + " " + played_card[1])
    
    # 3. Robot returns to player
    drive_back_to_player()
    
    return played_card

# --- Main Game Loop ---

def main():
    deck = create_deck()
    shuffle_deck(deck)
    
    # 1. Deal 7 cards
    player_hand = [deck.pop() for _ in range(7)]
    
    # 2. Display initial hand
    display_hand(player_hand)
    print("Hand loaded. Press CHECK to set top card.")
    
    while not brain.buttonCheck.pressing():
        wait(20, MSEC)
    wait_for_release()
    
    # 3. Set starting top card
    top_card = input_top_card()
    
    # 4. Continuous Game Loop
    while True:
        if len(player_hand) == 0:
            brain.screen.clear_screen()
            brain.screen.set_cursor(3, 1)
            brain.screen.print("YOU WIN!")
            break

        # Run player's turn (drives forward, draws/discards, drives back)
        top_card = player_turn_menu(deck, player_hand, top_card)
        
        # Display hand after returning
        display_hand(player_hand)
        print("\n--- Hand Updated ---")
        for idx, card in enumerate(player_hand, 1):
            print("Card " + str(idx) + ": " + card[0] + " " + card[1])

        brain.screen.set_cursor(5, 9)
        brain.screen.print("[CHK:NEXT]")
        while not brain.buttonCheck.pressing():
            wait(20, MSEC)
        wait_for_release()

# Run program
main()