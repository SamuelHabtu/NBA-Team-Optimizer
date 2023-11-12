import csv
import itertools
import random

def randomStart(players, teamsize = 15):
    return random.sample(players,teamsize)

def evaluateSquad(cur_squad, potential_squad):
    avgs = averages(potential_squad)
    cur_avgs = averages(cur_squad)
    win_counter = 0
    for category in cur_avgs:
        win_counter += battle(cur_avgs, avgs, category)
    return win_counter

def hillClimb(players,num_restarts = 5000, max_iterations = 100, team_size = 15):

    best_squad = None
    best_score = float("-inf")
    for _ in range(num_restarts): 
        #print(f"Start #{_ + 1}")
        cur_squad = randomStart(players, team_size)
        cur_score = sum(normalizedScore(cur_squad))
        for _ in range(max_iterations):
            neighbour_squad = cur_squad.copy()
            index_to_swap = random.randint(0, team_size - 1)
            new_player = new_player = random.choice([p for p in players if p not in cur_squad])  # Exclude players already in squad
            neighbour_squad[index_to_swap] = new_player
            neighbour_score = sum(normalizedScore(neighbour_squad))
            if neighbour_score > cur_score:
                cur_squad = neighbour_squad[:]
                cur_score = neighbour_score
                if cur_score > best_score:
                    best_squad = cur_squad[:]
                    best_score = cur_score


    
    return best_squad


def averages(team):

    averages = {}
    total_fga = 0
    total_3pa = 0
    total_fgm = 0
    total_3pm = 0
    total_pts = 0
    total_reb = 0
    total_ast = 0
    total_stl = 0
    total_blk = 0
    total_pf = 0
    total_to = 0
    for player in team:
        total_fga += player["FGA"]
        total_3pa += player["3PTA"]
        total_fgm += player["FGM"]
        total_3pm += player["3PM"]
        total_pts += player["PTS"]
        total_reb += player["REB"]
        total_ast += player["AST"]
        total_stl += player["STL"]
        total_blk += player["BLK"]
        total_to += player["TO"]
        total_pf += player["PF"]

    averages["FG%"] = total_fgm/total_fga
    averages["3PT%"] = total_3pm/total_3pa
    averages["REB"] = total_reb#/len(team)
    averages["AST"] = total_ast#/len(team)
    averages["STL"] = total_stl#/len(team)
    averages["BLK"] = total_blk#/len(team)
    averages["A/T"] = total_ast/total_to
    averages["PF"] = -total_pf#/len(team) 
    
    return averages

def optimize(players, teamsize = 15):

    current_squad = players[:teamsize]
    print(len(list(itertools.combinations(players, 15))))

    for temp_squad in itertools.combinations(players, 15):
        if normalizedScore(current_squad) < normalizedScore(temp_squad):
            current_squad = temp_squad[:]
    '''
    for i in range(len(current_squad)):
        for j in range(len(players)):
            if players[j] not in current_squad:
                temp_squad = []
                temp_squad = current_squad[:i]
                temp_squad.append(players[j])
                temp_squad += current_squad[i + 1:]
                if normalizedScore(current_squad) < normalizedScore(temp_squad):
                    current_squad = temp_squad
    '''
    return current_squad

def optimize_greedy(players, teamsize=15):
    current_squad = players[:teamsize]
    for i in range(len(teamsize)):
        for j in range(teamsize,len(players)):
            temp_squad = current_squad[:]
            temp_squad[i], temp_squad[j] = temp_squad[i], temp_squad[j]

def headToHead(current_squad, temp_squad):
    #returns ture if a team is better than the other
    cur_avgs = averages(current_squad)
    temp_avgs = averages(temp_squad)
    win_counter = 0
    for category in cur_avgs:
        win_counter += battle(cur_avgs, temp_avgs, category)
    if win_counter >= 6:
        return True 
    return False


def battle(current, temp, category):
    return temp[category] > current[category]


def normalizedScore(squad):

    stats = averages(squad)
    min_FG_percent = 0
    max_FG_percent = 0.55
    
    min_ThreePt_percent = 0
    max_ThreePt_percent = 0.39
    
    min_REB = 0
    max_REB = 6500  # Assuming this is the upper limit for rebounds 
    min_AST = 0
    max_AST = 3800  # You'll need to determine the maximum possible value for AST based on your league settings
    min_STL = 0
    max_STL = 1400.0  # You'll need to determine the maximum possible value for STL based on your league settings
    min_BLK = 0
    max_BLK = 831.5999999999999  # You'll need to determine the maximum possible value for BLK based on your league settings
    min_AT = 0
    max_AT = 2.41  # You'll need to determine the maximum possible value for A/T based on your league settings
    min_PF = 0  # You'll need to determine the minimum possible value for PF based on your league settings
    max_PF = -1900
    # Normalize each statistic, each stat is also weighted by 0.125
    normalized_stats = []
    normalized_stats.append((stats["FG%"] - min_FG_percent) / (max_FG_percent - min_FG_percent)*0.125)
    normalized_stats.append((stats["3PT%"] - min_ThreePt_percent) / (max_ThreePt_percent - min_ThreePt_percent)*0.125)
    normalized_stats.append((stats["REB"] - min_REB) / (max_REB - min_REB)*0.125)
    normalized_stats.append((stats["AST"] - min_AST) / (max_AST - min_AST)*0.125)
    normalized_stats.append((stats["STL"] - min_STL) / (max_STL - min_STL)*0.125)
    normalized_stats.append((stats["BLK"] - min_BLK) / (max_BLK - min_BLK)*0.125)
    normalized_stats.append((stats["A/T"] - min_AT) / (max_AT - min_AT)*0.125)
    normalized_stats.append(( max_PF - stats["PF"]) / (max_PF - min_PF)*0.125)
    #we hardcap everything at 1
    for i in range(len(normalized_stats)):
        normalized_stats[i] = min(normalized_stats[i],1.0)
    return normalized_stats

def matchUp(opponent, squad):

    other_team = optimize(extractPlayers(opponent))
    enemy_avgs = averages((other_team))
    squad_avgs = averages(squad)
    print(f"Matchup vs {opponent[:-2]}")
    for category in enemy_avgs:
        print(f"{category}: My Squad: {squad_avgs[category]} Enemy Squad: {enemy_avgs[category]}")
    score = evaluateSquad(other_team, squad)
    print(f"is My Squad better? : {score > 6} , Expected Score of: {score}-{12- score}")
    return score


def extractPlayers(filename = "freeagents.csv"):
    players = []
    with open(filename, newline = '') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for player_info in csvdata:
            
            #format is:Player info,FGM,FGA,FG%,FTM,3PTM,3PTA,3PT%,PTS,REB,AST,STL,BLK,A/T,PF
            temp_player = {}
            standard_size = 15
            size_delta = len(player_info) - standard_size
            temp_player["Name"] = player_info[0]
            temp_player["FGM"] = float(player_info[1 + size_delta])
            temp_player["FGA"] = float(player_info[2 + size_delta])
            temp_player["FG%"] = float(player_info[3 + size_delta])
            temp_player["FTM"] = float(player_info[4 + size_delta]) 
            temp_player["3PM"] = float(player_info[5 + size_delta])
            temp_player["3PTA"] = float(player_info[6+ size_delta])
            temp_player["3PT%"] = float(player_info[7 + size_delta])
            temp_player["PTS"] = float(player_info[8 + size_delta])
            temp_player["REB"] = float(player_info[9 + size_delta])
            temp_player["AST"] = float(player_info[10 + size_delta])
            temp_player["STL"] = float(player_info[11 + size_delta])
            temp_player["BLK"] = float(player_info[12 + size_delta])
            temp_player["A/T"] = float(player_info[13 + size_delta])
            temp_player["TO"] = temp_player["AST"]/temp_player["A/T"]
            temp_player["PF"] = float(player_info[14 + size_delta])
            players.append(temp_player)
    return players

def freeAgents(cur_squad):

    freeAgents = extractPlayers()
    #add our players to the free agent pool
    for player in cur_squad:
        freeAgents.append(dict(player))
    hill_squad = hillClimb(freeAgents)
    cur_avgs = averages((cur_squad))
    optimized_averages = averages(hill_squad)
    for category in cur_avgs:
        print(f"{category}: Current Roster: {cur_avgs[category]} Optimized: {optimized_averages[category]}")
    print(f"Here is our original Squad")
    for player in cur_squad:
        print(f"{player["Name"]}")
    print(f"Here is our Optimized Squad")
    for player in hill_squad:
        print(f"{player["Name"]}")

    return hill_squad
def main():
    
    players = extractPlayers("currentroster.csv")
    roster = freeAgents(players)
    #roster = optimize(players)
    print("-----------------------------------------------------------------------------------------------")
    print(f"Now let's do some theoretical matchups:")
    for opp in ["Slim reaper.csv", "Jimmy's Buckets.csv", "Dunk Daddies.csv"]:

        matchUp(opp, roster)
if __name__ == '__main__':
    main()