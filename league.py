class Player:

    def __init__(self, name, position, stats):

        self.name = name
        self.position = position
        self.stats = stats
        #calculating the players generic position(for quotas and limits!)
        if "G" in self.position:
            self.generic_position = "G"
        elif "F" in self.position:
            self.generic_position = "F"
        else:
            self.generic_position = "C"


class Team:
    
    def __init__(self, name, position_limits = {"G": 3, "F": 3, "C": 2, "U": 2, "B": 5 }, position_quotas = {"PG": 1,  "SG": 1, "SF": 1, "PF": 1, "C": 2}):

        self.name = name
        self.players = {}
        self.position_limits = position_limits
        self.position_quotas = position_quotas
        self.position_counts = {position: 0 for position in position_quotas.keys()}
        self.max             = sum(position_limits.values())

    def addPlayer(self, player):

        generic_position = player.generic_position
        #need to collect the other position as well for checking!
        if "S" in player.position:
            other_position = "P"
        else:
            other_position = "S"
        other_position = other_position + generic_position

        #check if we have reached our positional limit AFTER filling our utility and Bench up
        if self.position_counts[player.generic_position] >= self.position_limits[player.generic_position]:

            print("team {self.name} Cannot add another {player.generic_position}!!! there are already {self.position_counts[player.generic_position]}")
        #case: theres only 1 spot left for the position and the quote for the other position is not met, e.g: you hvae 2 PG's already and you want to add a 3rd(but the quota
        # guards is 1 pg and 1 sg)
        elif self.position_counts[player.generic_position] == self.position_limits[player.generic_position] - 1 and self.position_counts[other_position] == 0:

            print("team {self.name} Cannot add another {player.position}!!! the quota for {other_position} is not Met")
        


    def removePlayer(self, name):
        if name in self.players:
            del self.players[name]
        else:
            print(f"{name} is not on Team {self.name}")
    
def startersFilled(team):
    for position in position