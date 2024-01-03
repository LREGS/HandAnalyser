import os 
import re
from dataclasses import dataclass

current_dir = os.path.dirname(os.path.abspath(__file__))

#Use file system where we can loop through the files to get all hands histroy
#as its currently seperated by days. For now we're working on one day. 
handHistory = "30-12.txt"

playres = ""
text_file_path = os.path.join(current_dir, 'hands', handHistory)

with open(text_file_path,'r') as file:
    content = file.read().strip()
    hands = content.split("\nPokerStars")



@dataclass
class Player:
    name: str
    stack: int 
    seat: str
    hand: str

class PSHandHistory:
    def __init__(self, hands):

        self._seat_re = re.compile(r"^Seat (?P<seat>\d+): (?P<name>.+?) \(\$?(?P<stack>\d+(\.\d+)?) in chips\)")

        self.positions_re = re.compile(r"^Zoom (?P<positions>.*?\*)")
        self.action_re = re.compile(r"\*(?P<action>.*?\bSUMMARY\b)")
        self.summary_re = re.compile(r"\bSUMMARY\b(?P<action>.*)")

        self.games =  [hand.strip() for hand in hands]
    
        #summaries has one less than the rest of the lits?!
        self.positions = [match.group() for game in self.games if (match := self.positions_re.search(game.replace('\n', ' '))) is not None]
        self.action = [action.group() for game in self.games if (action := self.action_re.search(game.replace('\n', ' '))) is not None]
        self.sum = [sum.group() for game in self.games if (sum := self.summary_re.search(game.replace('\n', ' '))) is not None]
        self.players = []


    
    def parse_players(self):
        for hand in self.positions:
            matches = self._seat_re.finditer(hand)
            for match in matches:
                seat_info = match.groupdict()
                print(seat_info)
    
        # for hand in self.positions:
        #     print(hand)
        #     for line in hand.split('\n'):
        #         print(line)
        #         match = self._seat_re.match(line)
        #         if match:
        #             print(match)
        #             self.players.append(Player(
        #             name = match.group("name"),
        #             stack = match.group("stack"),
        #             seat = match.group("seat"),
        #             hand = None,))
        #         else:
        #             # print("no match")
        #             continue
        # #         if not match:
        # #             print("no match")

        # # print(self.players)



hh = PSHandHistory(hands)
hh.parse_players()


"""
> store game in list 
> it through list, then it through each item but only in sections 
Section 1: up to ***HoleCards*** - Gets players in the game, their seat and their stack size 
Section2: Between ***HoleCards*** and ***summary*** details of action during the game
Section 3: After Summary - Total pot size, winner - but will probably be following this as we map the gamea anyway"""