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

game = game.Game()
print(p.hp)
game.start()
#while (not p.is_dead):
for i in range(4):
    game.next_turn('Strength')