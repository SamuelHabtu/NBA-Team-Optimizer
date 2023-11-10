import csv
import random

def randomStart(players):
    chosen_players = dict({})
    for position in players:
        pick = random.choice(players[position])
        #no duppies >:^)
        while pick in chosen_players.values():
            pick = random.choice(players[position])
        chosen_players[position] = pick
    return chosen_players

def salaryCheck(squad, cap = 200):

    for player in squad:
        cap -= squad[player]["Salary"]
    #this returns True or False aka 1 or 0
    return cap >= 0

def evaluateSquad(squad):
    score = 0
    for player in squad:
        score += squad[player]["FFPG"]
    return score * salaryCheck(squad)

def hillClimb(players,num_restarts = 200, max_iterations = 20000):

    best_squad = None
    best_score = float("-inf")
    for _ in range(num_restarts): 
        print(f"Start #{_ + 1}")
        cur_squad = randomStart(players)
        cur_score = evaluateSquad(cur_squad)
        for _ in range(max_iterations):
            neighbour_squad = dict(cur_squad) #make a shallow copy
            position_to_swap = random.choice(list(cur_squad.keys()))
            new_player = random.choice([p for p in players[position_to_swap] if p not in cur_squad.values()])  # Exclude players already in squad
            neighbour_squad[position_to_swap] = new_player
            neighbour_score = evaluateSquad(neighbour_squad)
            if neighbour_score > cur_score:
                cur_squad = dict(neighbour_squad)
                cur_score = neighbour_score
                if cur_score > best_score:
                    best_squad = cur_squad
                    best_score = cur_score
    return best_squad

def extractPlayers(filenames = ["Yahoo Cup PGs.csv", "Yahoo Cup SGs.csv", "Yahoo Cup SFs.csv", "Yahoo Cup PFs.csv", "Yahoo Cup Cs.csv"]):
    players = dict({})
    players["PG"] = []
    players["SG"] = []
    players["SF"] = []
    players["PF"] = []
    players["C"] = []

    for file in filenames:
        with open(file, newline = '') as csvfile:
            csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        
            for player in csvdata:
                new_player = dict({"Name": player[0], "FFPG": float(player[1]), "Salary": int(player[2])})
                new_player["Name"] = player[0]
                new_player["FFPG"] = float(player[1])
                new_player["Salary"] = int(player[2])
                players[file[10:-5]].append(new_player)
    

    #Gotta remove duplicate Lads
    forwards = list(players["SF"])
    forwards.extend(x for x in players["PF"] if x not in forwards)
    guards = list(players["PG"])
    guards.extend(x for x in players["SG"] if x not in guards)
    centers = list(players["C"])
    players["F"] = forwards
    players["G"] = guards
    util = list(centers)
    util.extend(x for x in players["F"])
    util.extend(x for x in players["G"])
    players["Util"] = util
    return players

def main():
    
    players = extractPlayers()

    hill_squad = hillClimb(players)
    for slot in hill_squad:
        print(f"{slot} {hill_squad[slot]['Name']}")
    total_ffpg = evaluateSquad(hill_squad)
    print(f"for a combined FFPG of:{total_ffpg} OR {total_ffpg/len(hill_squad.keys())} average ffpg")
    
if __name__ == '__main__':
    main()