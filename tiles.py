import actions
import enemies
import items
import sounds
import utils
import world


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.beenThere = False

    def intro_text(self):
        raise NotImplementedError()

    def ascii_art(self):
        raise NotImplementedError()

    def sound(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Equip())
        moves.append(actions.Heal())
        moves.append(actions.Status())

        return moves


class StartingCompartment(MapTile):
    # override the intro_text method in the superclass
    def intro_text(self):
        if self.beenThere:
            return "Oh no not again at the starting point"

        else:
            self.beenThere = True
            return """
                    You landed in submarine starting point compartment now we have aleady given you very good guns which you can use against your enemy,
                .
                    """

    def modify_player(self, player):
        # Room has no action on player
        pass

    def ascii_art(self):
        pass

    def sound(self):
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item, beenThere):
        self.item = item
        self.beenThere = beenThere
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            sounds.enemy_attack()
            the_player.hp = the_player.hp - self.enemy.damage
            print(f"Enemy does {self.enemy.damage} damage.")
            if the_player.hp > 0:
                print("You have {} HP remaining.".format(the_player.hp))


    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Equip(), actions.Heal(),
                    actions.Status()]
        else:
            moves = self.adjacent_moves()
            moves.append(actions.Equip())
            moves.append(actions.Heal())
            moves.append(actions.Status())

            return moves


class EmptySubCompartment(MapTile):
    def intro_text(self):
        if self.beenThere:
            return """Oh not again in the same empty compartment!"""

        else:
            self.beenThere = True
            return """Ah! Empty compartment , This time i will try hard and find thannos and kill him for sure """

    def modify_player(self, player):
        # Room has no action on player
        pass

    def ascii_art(self):
        pass

    def sound(self):
        pass


class JokerCompartment(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Joker())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
           the mighty Joker is approaching you, don't let your guard down!
            """

        else:
            return """
            The corpse of a dead Joker laying on the ground.
            """

    def ascii_art(self):
        if self.enemy.is_alive():
            return utils.joker_ascii()

    def sound(self):
        if self.enemy.is_alive():
            return sounds.joker()


class VenomCompartment(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Venom())

    def intro_text(self):
        if self.enemy.is_alive():
            return """Now this is very a serious situation because i don't know what to use against this enemy ."""

        else:
            return """
             The corpse of a dead venom is rotting.
             """

    def ascii_art(self):
        if self.enemy.is_alive():
            return utils.venom_ascii()

    def sound(self):
        if self.enemy.is_alive():
            return sounds.venom()


class ThanosCompartment(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Thanos())

    def intro_text(self):
        if self.enemy.is_alive():
            return """Oh no. this might be a end of you because no one can stand against thanos"""

        else:
            return """now this is a real success !Thanos is lying on the ground without head """

    def ascii_art(self):
        if self.enemy.is_alive():
            return utils.thanos_ascii()

    def sound(self):
        if self.enemy.is_alive():
            return sounds.thanos()


class FindSwordCompartment(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Sword(), beenThere=False)

    def intro_text(self):
        if self.beenThere:
            return """
            You've been here before...
            This is where you found a sword"""
        else:
            self.beenThere = True
            return """
                    Your notice something shiny in the corner.
                    It's a Sword! You pick it up.
                    """

    def ascii_art(self):
        if not self.beenThere:
            return utils.sword_ascii()

    def sound(self):
        if not self.beenThere:
            return sounds.pulling_out_sword()



class DestructionCompartment(MapTile):
    def intro_text(self):
        return """Great! See that red button on main machine that is self destruction button can destroy whole 
        submarine and monsters inside it with in a flash... ... Now click it and get rid of these monsters. 
 
 
        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True

    def ascii_art(self):
        pass

    def sound(self):
        return sounds.nuke()
