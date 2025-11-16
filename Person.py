import random

class Person:
    def __init__(self):

        self.strength = random.randint(25,61)
        self.charisma = random.randint(25, 61)
        self.dexterity = random.randint(25, 61)
        self.intelligence = random.randint(25, 61)
        
        self.hp = 100
        self.max_hp = self.hp
        self.hp = self.hp/self.max_hp*100
        self.is_dead = False
        
    def reduce_hp(self, value):
        self.hp -= value
        if (self.hp <= 0):
            self.is_dead = True
            self.game_over()
            
    def increase_hp(self, value):
        self.hp += value
        if (self.hp >= self.max_hp):
            self.hp = self.max_hp
    
    def increase_max_hp(self, value):
        self.max_hp += value
        self.increase_hp(value)
    
    def game_over(self):
        self.hp = 0
        self.is_dead = True
        
    def _modify_stat(self, stat_name, value):
        """Generic internal function to modify any stat safely."""
        old_value = getattr(self, stat_name)
        new_value = max(0, old_value + value)
        setattr(self, stat_name, new_value)

    def increase_strength(self, value):
        self._modify_stat("strength", value)

    def reduce_strength(self, value):
        self._modify_stat("strength", -value)

    # Charisma
    def increase_charisma(self, value):
        self._modify_stat("charisma", value)

    def reduce_charisma(self, value):
        self._modify_stat("charisma", -value)

    # Dexterity
    def increase_dexterity(self, value):
        self._modify_stat("dexterity", value)

    def reduce_dexterity(self, value):
        self._modify_stat("dexterity", -value)

    # Intelligence
    def increase_intelligence(self, value):
        self._modify_stat("intelligence", value)

    def reduce_intelligence(self, value):
        self._modify_stat("intelligence", -value)