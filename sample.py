import Person
import description
import game

p = Person.Person()
# print(p.hp)
# p.reduce_hp(15)
# print(p.hp)

# for i in range(5):
#     event = description.pioche()
#     print(event)

game = game.Game(key="AIzaSyDduw3y8iM1vMjR0EGEyfIfp8qE3aj93iE")
print(p.hp)
game.start("I wake up in a cave by the ocean after taking a short nap in the office.")
#game.start()
#while (not p.is_dead):
for i in range(4):
    e = game.draw_card()
    game.next_turn('Strength', e)