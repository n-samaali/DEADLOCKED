import random
#coeur, carreau, trefle, pique
# hearts, diamond, spade, clubs
description = {"JH":"Checks your PC's RAM. If it's lower or equal to 8GB, the game crashes and it's Game Over, else the game continues", "QH":"The Queen of Hearts executes you. Game Over", "KH": "Adds 50 HP to compensate for his wife's behavior",
               "JD":"Tells you a corny joke", "QD":"Increases your charisma by 12", "KD": "Decreases your strength by 17",
               "JS":"I'm Professor Jake! Gives you fun facts about bash and C", "QS":"Increases dexterity by 9", "KS":"Takes control of your character and kills you slowly",
               "JC":"Feeling lucky? Picks a number between 1 & 4. One of these numbers is game over, and the other 3 heal you by their number", "QC":"Decreases your HP by 25", "KC":"You win bragging rights because you pulled me! A card that's as likely to pull as a 3 of hearts...",
               }

def pioche():
    event = ""
    rank = random.randint(1,13)
    suit = random.randint(1,4)
    rank_dictionary = {1:"A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K"}
    suit_dictionary = {1:"♥", 2:"♦", 3:"♠", 4:"♣"}
    suit_letters = {1:"H", 2:"D", 3:"S", 4:"C"}
    card_letter = rank_dictionary[rank]+suit_letters[suit]
    if card_letter in description:
        event = description[card_letter]
    return ((card_letter + ":" + event), card_ascii(rank_dictionary[rank], suit_dictionary[suit]))

def card_ascii(rank, suit, width=13, height=7):
    """
    rank: string, e.g. 'A', '10', 'K'
    suit: one-character suit, e.g. '♠', '♥', '♦', '♣'
    width: total characters across including border (odd recommended)
    height: total lines including top/bottom border (odd recommended)
    """
    # content area dimensions
    inner_w = width - 2
    inner_h = height - 2

    # top/bottom borders
    top = "┌" + "─" * inner_w + "┐"
    bot = "└" + "─" * inner_w + "┘"

    # prepare lines
    lines = [top]
    # first line with rank left-aligned
    left_rank = rank
    first = "│" + left_rank + " " * (inner_w - len(left_rank)) + "│"
    lines.append(first)

    # number of lines above/below center
    above = (inner_h - 1) // 2
    below = inner_h - 1 - above

    # empty lines above center
    for _ in range(above):
        lines.append("│" + " " * inner_w + "│")

    # center line with suit centered
    suit_line = " " * ((inner_w - 1) // 2) + suit + " " * (inner_w - 1 - (inner_w - 1) // 2)
    lines.append("│" + suit_line + "│")

    # empty lines below center
    for _ in range(below):
        lines.append("│" + " " * inner_w + "│")

    # last line with rank right-aligned
    right_rank = rank
    last = "│" + " " * (inner_w - len(right_rank)) + right_rank + "│"
    lines.append(last)

    lines.append(bot)
    return "\n".join(lines)