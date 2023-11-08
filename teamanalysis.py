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

def hillClimb(players, max_iterations = 10000, team_size = 15):

    best_squad = optimize(players, teamsize=10)
    all_squads = list(itertools.combinations(players, team_size))
    num_wins = []
    for i in range(len(all_squads)):
        num_wins.append(0)
        for j in range(len(all_squads)):
            battles_won = evaluateSquad(all_squads[j],all_squads[i])
            if battles_won > 0:
                num_wins[i] += 1

    max_wins = max(num_wins)
    winner = num_wins.index(max_wins)
    
    
    return all_squads[winner]


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

def main():
    
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


    team_averages = averages(players[:10])
    optimized_squad = optimize(players[:17], teamsize=10)
    hill_squad =   hillClimb(players[:17], team_size=10)
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
        print(f"{category}: Hill: {hill_averages[category]} Optimized: {optimized_averages[category]}-> Better? {hill_averages[category] > optimized_averages[category]}")
    print(f"is Hill better? : {evaluateSquad(optimized_squad, hill_squad)}")
    
    hyp_team = ["Ben Simmons BKN - PG","Gordon Hayward CHA - SF","Kentavious Caldwell-Pope DEN - SG","Josh Giddey OKC - SG","Kevon Looney GSW - PF","Mitchell Robinson NYK - C",
                  "Alperen Sengun HOU - C","No  Kyle Anderson MIN - SF","Dereck Lively II DAL - C", "J. Sochan SAS - PG"]
    my_picks = []
    for player in players[:13]:
        if player["Name"] in hyp_team:
            my_picks.append(player)
    my_pick_avgs = averages(my_picks)
    print("Now we compare my picks to the OPTIMAL")
    for category in team_averages:
        print(f"{category}: my Picks: {my_pick_avgs[category]} Hill: {hill_averages[category]} -> Better? {my_pick_avgs[category] > hill_averages[category]}")
    print(f"Are my Picks better Than Hill Squad? {evaluateSquad(hill_squad, my_picks)}")
if __name__ == '__main__':
    main()