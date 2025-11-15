import random

class Person:
    def __init__(self):

        self.charisma = random.randint(25, 61)
        self.dexterity = random.randint(25, 61)
        self.intelligence = random.randint(25, 61)
        
        self.hp = 100 + (self.dexterity) 
        self.max_hp = self.hp
        
    def reduce_hp(self, value):
        self.hp -= value
        if (self.hp <= 0):
            self.game_over()
            
    def increase_hp(self, value):
        self.hp += value
        if (self.hp >= self.max_hp):
            self.hp = self.max_hp
    
    def increase_max_hp(self, value):
        self.max_hp += value
        self.increase_hp(value)
    
    def game_over(self):
        print("YOU DIED (of course it's a Dark Souls reference!)")