import sounds
import utils
import world
from player import Player


def play():
    world.load_tiles()
    name = input("Whats Your name?: \t")
    player = Player(name)
    # These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)
    sounds.phone_ringing()
    print(f"Hello {name}")
    intro_text = """As you know in the end of "End game avenger" , Thanos  in the end  killed by Thor but he actually Managed to escape by using time travel in the meantime, 
    he has been hiding in ocean and thinking about a big revenge. so after 6 years he is coming here with a submarine to destroy whole earth, your task is to destroy his submarine and save the humankindd"""
    print(intro_text)
    sounds.submarine_coming()
    utils.submarine_ascii()
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break
    if player.is_alive() and player.victory:
        print("You won!")
        sounds.win()

    print("Game Over you Lost!")
    sounds.game_over()


if __name__ == "__main__":
    play()
