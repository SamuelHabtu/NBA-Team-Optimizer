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

def hillClimb(players,num_restarts = 50, max_iterations = 10000, team_size = 15):

    best_squad = None
    best_score = float("-inf")
    for _ in range(num_restarts):
        print(f"Start #{_ + 1}")
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
    delta_contribution = 0
    for i in range(len(current_squad)):
        for j in range(teamsize, len(players)):
            if players[j] not in current_squad:
                temp_squad = []
                temp_squad = current_squad[:i]
                temp_squad.append(players[j])
                temp_squad += current_squad[i + 1:]
                if headToHead(current_squad, temp_squad):
                    current_squad = temp_squad
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
    if win_counter > 0:
        return True
    return False


def battle(current, temp, category):
    if temp[category] > current[category]:
        return 1
    elif temp[category] < current[category]:
        return -1
    return 0

def normalizedScore(squad):

    stats = averages(squad)
    min_FG_percent = 0
    max_FG_percent = .75
    
    min_ThreePt_percent = 0
    max_ThreePt_percent = .65
    
    min_REB = 0
    max_REB = 4970.0  # Assuming this is the upper limit for rebounds 
    min_AST = 0
    max_AST = 2849.0  # You'll need to determine the maximum possible value for AST based on your league settings
    min_STL = 0
    max_STL = 853.8000000000001  # You'll need to determine the maximum possible value for STL based on your league settings
    min_BLK = 0
    max_BLK = 621.0999999999999  # You'll need to determine the maximum possible value for BLK based on your league settings
    min_AT = 0
    max_AT = 2.5145437779101742  # You'll need to determine the maximum possible value for A/T based on your league settings
    min_PF = 0  # You'll need to determine the minimum possible value for PF based on your league settings
    max_PF = -1958.2999999999997
    # Normalize each statistic, each stat is also weighted by 0.125
    normalized_stats = []
    normalized_stats.append((stats["FG%"] - min_FG_percent) / (max_FG_percent - min_FG_percent)*(1/7))#0.125)
    normalized_stats.append((stats["3PT%"] - min_ThreePt_percent) / (max_ThreePt_percent - min_ThreePt_percent)*(1/7))#0.125)
    normalized_stats.append((stats["REB"] - min_REB) / (max_REB - min_REB)*(1/7))#0.125)
    normalized_stats.append((stats["AST"] - min_AST) / (max_AST - min_AST)*(1/7))#0.125)
    normalized_stats.append((stats["STL"] - min_STL) / (max_STL - min_STL)*(1/7))#0.125)
    normalized_stats.append((stats["BLK"] - min_BLK) / (max_BLK - min_BLK)*(1/7))#0.125)
    normalized_stats.append((stats["A/T"] - min_AT) / (max_AT - min_AT)*(1/7))#0.125)
    normalized_stats.append(( max_PF - stats["PF"]) / (max_PF - min_PF)*0)#0.125)
    return normalized_stats

def matchUp(opponent, squad):

    other_team = extractPlayers(opponent)
    enemy_avgs = averages(other_team)
    squad_avgs = averages(squad)
    print(f"Matchup vs {opponent[:-2]}")
    for category in enemy_avgs:
        print(f"{category}: My Squad: {squad_avgs[category]} Enemy Squad: {enemy_avgs[category]}")
    score = evaluateSquad(other_team, squad)
    print(f"is My Squad better? : {score > 0} Score was: {score}")
    return score


def extractPlayers(filename = "freeagents.csv"):
    players = []
    with open('freeagents.csv', newline = '') as csvfile:
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

def main():
    
    players = extractPlayers()

    team_averages = averages(players[:15])
    optimized_squad = optimize(players, teamsize=15)
    hill_squad =   hillClimb(players, team_size=15)
    optimized_averages = averages(optimized_squad)
    hill_averages = averages(hill_squad)
    print("Optimized squad:")
    for player in optimized_squad:
        print(f"{player['Name']}")
    print("HILL SQUAD:")
    for player in hill_squad:
        print(f"{player['Name']}")
    print("Now let's compare the Hill vs brute force averages!")
    for category in team_averages:
        print(f"{category}: Hill: {hill_averages[category]} Optimized: {optimized_averages[category]}")
    print(f"is Hill better? : {evaluateSquad(optimized_squad, hill_squad)}")
    print("-----------------------------------------------------------------------------------------------")
    print(f"Now let's do some theoretical matchups:")
    for opp in ["Slim reaper.csv", "Jimmy's Buckets", "Dunk Daddies"]:

        matchUp(opp, hill_squad)
    
if __name__ == '__main__':
    main()