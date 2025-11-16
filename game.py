import description
from generator import GenAiHandler
import Person
import subprocess
import random
import psutil

class Game:
    def __init__(self, key):
        self.key = key 
        self.ai_handler = GenAiHandler(self.key)
        self.person = Person.Person()
        
    def get_ram_gb(self):
        mem_bytes = psutil.virtual_memory().total
        return mem_bytes / (1024 ** 3)
    
    def draw_card(self):
        event = description.pioche()
        return event
    
    def card_verificator(self, event, choice):
        key = event.split(":")[0]
        if key=="QH":
            self.person.game_over()
        if key=="JH":
            gb = self.get_ram_gb()
            if gb <= 8:
                print("Not enough RAM unfortunately...")
                self.person.game_over()
        if key=="KH":
            self.person.increase_hp(50)
        if key=="KS":
            while(not self.person.is_dead):
                self.person.reduce_hp(15)
        if key=="JC":
            num = random.randint(1,4)
            num2 = random.randint(1,4)
            if (num == num2):
                print("Not so lucky unfortunately...")
                self.person.game_over()
            else:
                self.person.increase_hp(num)
        if key=="QD":
            self.person.increase_charisma(12)
        if key=="QC":
            self.person.reduce_hp(25)
        if key=="KD":
            self.person.reduce_charisma(17)
        if key=="QS":
            self.person.increase_dexterity(9)
        if key[0] not in ["K", "Q", "J"]:
            rank = key[0]

            # Convert rank to number if possible
            if rank.isdigit():
                rank_value = int(rank)
            else:
                rank_value = rank  # "A"

            # Mapping attribute names to functions
            stat_reduce = {
                "Strength": self.person.reduce_strength,
                "Dexterity": self.person.reduce_dexterity,
                "Intelligence": self.person.reduce_intelligence,
                "Charisma": self.person.reduce_charisma,
            }

            stat_increase = {
                "Strength": self.person.increase_strength,
                "Dexterity": self.person.increase_dexterity,
                "Intelligence": self.person.increase_intelligence,
                "Charisma": self.person.increase_charisma,
            }

            # Determine if it's a decrease or increase
            if (rank_value == "A" and choice == choice) or (isinstance(rank_value, int) and rank_value <= 3):
                stat_reduce[choice](random.randint(1, 5))

            elif isinstance(rank_value, int) and rank_value >= 8:
                stat_increase[choice](random.randint(1, 5))

            
    def start(self, context):
        event = ""
        a = self.ai_handler.call_ai(event, context, prompt="")
        story, table = self.ai_handler.split_story_and_table(a)
        print(story)
        self.options = self.ai_handler.parse_options(table)
        print(self.options)
        return story, self.options
        
    def next_turn(self, choice, event):
        print(event[1])#the ascii card
        self.card_verificator(event[0], choice)
        a = self.ai_handler.call_ai(event[0], "", self.options[choice])
        story, table = self.ai_handler.split_story_and_table(a)
        print(story)
        # print(dm)
        # print(table)
        hp_stuff = self.ai_handler.extract_modifier(a)
        
        if hp_stuff[0] is not None:
            action, value = hp_stuff

            if action == "Reduce":
                self.person.reduce_hp(value)

            elif action == "Increase":
                self.person.increase_hp(value)

            print("Current HP:", self.person.hp)
    
        self.options = self.ai_handler.parse_options(table)
        print(self.options)
        return story, self.options
        