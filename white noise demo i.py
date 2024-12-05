import time
import random
import os
import json

SAVE_FILE = "white_noise_save.json"

def save_game(player_health, noise_level, turns_survived, monster_distance):
    """Save the game state to a file."""
    save_data = {
        "player_health": player_health,
        "noise_level": noise_level,
        "turns_survived": turns_survived,
        "monster_distance": monster_distance,
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(save_data, file)
    print("\nGame saved!")

def load_game():
    """Load the game state from a file if it exists."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            save_data = json.load(file)
        print("\nGame loaded!")
        return save_data["player_health"], save_data["noise_level"], save_data["turns_survived"], save_data["monster_distance"]
    else:
        print("\nNo save file found. Starting a new game.")
        return 100, 0, 0, random.randint(5, 10)

def delete_save():
    """Delete the save file."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("\nAll saved data wiped.")

def white_noise_demo():
    print("WELCOME TO WHITE NOISE: Demo")
    print("Survive monsters that will rip and tear if they hear slight noises.")
    print("You must survive 20 turns without being caught.\n")

    # Load or start new game
    choice = input("Do you want to load a previous game? (yes/no): ").strip().lower()
    if choice == "yes":
        player_health, noise_level, turns_survived, monster_distance = load_game()
    else:
        player_health, noise_level, turns_survived, monster_distance = 100, 0, 0, random.randint(5, 10)

    max_turns = 20  # Total turns in the demo

    # Helper functions
    def increase_noise(amount):
        nonlocal noise_level
        noise_level += amount
        print(f"Your noise level is now: {noise_level}")
        if noise_level >= monster_distance:
            print("\nThe monsters heard you! They're coming!")
            return True
        return False

    def check_monster_distance():
        nonlocal monster_distance
        monster_distance = random.randint(3, 8)
        print(f"The nearest monster is {monster_distance} units away.")

    # Game loop
    while player_health > 0 and turns_survived < max_turns:
        print("\n--- NEW TURN ---")
        print(f"Health: {player_health}")
        check_monster_distance()
        print("Choose an action:")
        print("1. Move quickly (noisy but covers more distance)")
        print("2. Move quietly (silent but slower progress)")
        print("3. Hide and wait (low noise, but monsters may roam closer)")
        print("4. Search for supplies (noisy, chance to find health)")
        print("5. Save and quit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print("You moved quickly!")
            if increase_noise(random.randint(5, 8)):
                player_health -= 40
            else:
                print("You made your way quickly silently.")

        elif choice == "2":
            print("You moved quietly...")
            if increase_noise(random.randint(1, 3)):
                player_health -= 20
            else:
                print("You are safe! ...for now.")

        elif choice == "3":
            print("You hid and waited.")
            time.sleep(1)
            print("The monsters roamed closer.")
            check_monster_distance()
            if random.choice([True, False]):  # 50% chance to reduce distance
                monster_distance -= 1
                print("The monsters are very close now!")

        elif choice == "4":
            print("You searched for supplies...")
            if increase_noise(random.randint(4, 7)):
                player_health -= 50
            else:
                if random.choice([True, False]):
                    print("You found a medkit! Restored 20 health.")
                    player_health = min(100, player_health + 20)
                else:
                    print("You found nothing but made noise.")

        elif choice == "5":
            save_game(player_health, noise_level, turns_survived, monster_distance)
            print("Play again soon.")
            return

        else:
            print("Invalid choice. You stayed still and made no progress.")
        
        turns_survived += 1
        print(f"Turns survived: {turns_survived}/{max_turns}")

        # Check if the player has been caught
        if player_health <= 0 or noise_level >= monster_distance:
            print("\nThere is something behind you...")
            time.sleep(2)
            print("You hear an abrupt screech before getting dragged into the darkness...")
            time.sleep(2)
            print("\nSILENCE BROKEN")
            delete_save()  # Wipe save data
            input("\nPress Enter to quit the game...")
            return

    # Game end if all turns are survived
    if player_health > 0 and turns_survived >= max_turns:
        print("You survived! ...FOR NOW.")
        print("I will add more into the full game! Thanks for playing and leave a star on my GitHub!")
        delete_save()  # Wipe save data

# Run the game
if __name__ == "__main__":
    white_noise_demo()
