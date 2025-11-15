import description
from generator import GenAiHandler
import Person
import subprocess

class Game:
    def __init__(self, key):
        self.key = key 
        self.ai_handler = GenAiHandler(self.key)
        self.person = Person.Person()
        
    def get_ram_gb(self):
        output = subprocess.check_output("wmic computersystem get TotalPhysicalMemory", shell=True)
        # WMIC output includes the header and number, so extract digits
        mem_str = ''.join(filter(str.isdigit, output.decode()))
        mem_bytes = int(mem_str)
        return mem_bytes / (1024 ** 3)
    
    def draw_card(self):
        event = description.pioche()
        return event
    
    def card_verificator(self, event):
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
        self.card_verificator(event[0])
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
        