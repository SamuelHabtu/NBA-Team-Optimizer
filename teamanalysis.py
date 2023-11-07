import csv
import itertools

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
    averages["REB"] = total_reb/len(team)
    averages["AST"] = total_ast/len(team)
    averages["STL"] = total_stl/len(team)
    averages["BLK"] = total_blk/len(team)
    averages["A/T"] = total_ast/total_to
    averages["PF"] = -total_pf/len(team) 
    
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

def headToHead(current_squad, temp_squad):
    #returns ture if a team is better than the other
    cur_avgs = averages(current_squad)
    temp_avgs = averages(temp_squad)
    win_counter = 0
    for category in cur_avgs:
        win_counter += battle(cur_avgs, temp_avgs, category)
    if win_counter >= 3:
        return True
    return False


def battle(current, temp, category):
    if temp[category] > current[category]:
        return 1
    else:
        return -1

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


    team_averages = averages(players[:15])
    print("Here is the optimized SQUAD:")
    optimized_squad = optimize(players)
    optimized_averages = averages(optimized_squad)
    for player in optimized_squad:
        print(f"{player["Name"]}")
    print(f"{len(optimized_squad)} Players selected!")
    print("Now let's compare the team Averages!")
    for category in team_averages:
        print(f"{category}: Before: {team_averages[category]} After: {optimized_averages[category]}")
    
if __name__ == '__main__':
    main()