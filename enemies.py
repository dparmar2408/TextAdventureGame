class Enemy:
    def __init__(self, name, hp, damage, experience):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.experience = experience

    def is_alive(self):
        return self.hp > 0


class Venom(Enemy):
    def __init__(self):
        super().__init__(name="Venom", hp=140, damage=45, experience=80)


class Joker(Enemy):
    def __init__(self):
        super().__init__(name="Alien", hp=35, damage=25, experience=20)



class Thanos(Enemy):
    def __init__(self):
        super().__init__(name="Thanos", hp=200, damage=80, experience=150)
