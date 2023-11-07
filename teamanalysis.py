import csv


def averages(team):

    averages = {}
    total_fga = 0
    total_3pa = 0
    total_fgm = 0
    total_3pm = 0
    total_pts = 0
    total_reb = 0
    total_apg = 0
    total_stl = 0
    total_blk = 0
    total_pf = 0

    for player in team:
        total_fga += player["FGA"]
        total_3pa += player["3PA"]
        total_fgm += player["FGM"]
        total_3pm += player["3PM"]
        total_pts += player["PTS"]
        total_reb += player["REB"]
        total_apg += player["AST"]
        total_stl += player["STL"]
        total_blk += player["BLK"]
        total_pf += player["PF"]

    averages["FG%"] = total_fgm/total_fga
    averages["3PT%"] = total_3pm/total_3pa
    averages["REB"] = total_reb/len(team)
    averages["AST"] = total_apg/len(team)
    averages["STL"] = total_stl/len(team)
    averages["BLK"] = total_blk/len(team)
    averages["PF"] = total_pf/len(team) 
    
    return averages
    

def main():
    players = []
    with open('currentroster.csv', newline = '') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for player_info in csvdata:
            
            #format is:Player info,FGM,FG%,FTM,3PM,3P%,PTS,REB,AST,STL,BLK,A/T,PF
            #for player it has format of "New Player Note First Inital.Last Name TEAM - Position(s)"
            temp_player = {}
            print(len(player_info))
            temp_player["Name and Position"] = player_info[0]
            temp_player["FGM"] = float(player_info[1])
            temp_player["FG%"] = float(player_info[2])
            temp_player["FGA"] = temp_player["FGM"]/temp_player["FG%"]
            temp_player["FTM"] = float(player_info[3])
            temp_player["3PM"] = float(player_info[4])
            temp_player["3PT%"] = float(player_info[5])
            if temp_player["3PT%"] == 0:
                if temp_player["3PM"] == 0:
                    #never even shot one >:^)
                    temp_player["3PA"] = 0
            else:
                temp_player["3PA"] = temp_player["3PM"]/ temp_player["3PT%"]
            temp_player["PTS"] = float(player_info[6])
            temp_player["REB"] = float(player_info[7])
            temp_player["AST"] = float(player_info[8])
            temp_player["STL"] = float(player_info[9])
            temp_player["BLK"] = float(player_info[10])
            temp_player["PF"] = float(player_info[11])
            players.append(temp_player)

    for player in players:
        print(player)
    team_averages = averages(players)
    print(team_averages)
if __name__ == '__main__':
    main()