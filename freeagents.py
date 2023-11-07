import csv
import re

def extractPlayerInfo(player_str):

    pattern = r'"(.+?)\s([A-Z,]+)\s'
    match = re.search(pattern, player_str)
    if match:
        player_name = match.group(1)
        player_position = match.group(2).split(',')
        return player_name, player_position
    else:
        return None, None

def main():
    players = []
    with open('freeagents.csv', newline = '') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for row in csvdata:
            print(row[0])
            #format is:Player,GP,Pre-season Rank,Current Rank,Rostered %,MPG,FGM,FGA,FG%,FTM,3PTM,3PTA,3PT%,PTS,REB,AST,ST,BL,A/T,PF,
            #for player it has format of "New Player Note First Inital.Last Name TEAM - Position(s)"
            temp_player = {}
            name, position = extractPlayerInfo(row[0])
            print(f"Name:{name} Position: {position}")
    pg_list = []
    sg_list = []
    sf_list = []
    pf_list = []
    c_list = []
    for player in players:
        if player["position"] == "PG":
            pg_list.append(player)
        elif player["position"] == "SG":
            sg_list.append(player)
        elif player["position"] == "SF":
            sf_list.append(player)
        elif player["position"] == "PF":
            pf_list.append(player)
        else:
            c_list.append(player)
    g_list = pg_list + sg_list
    f_list = sf_list + pf_list
    print("top 15: Bang for Buck List PER POSITION then general List:")

    print("PG")
    for player in effiency(pg_list):
        print(player)
    print("SG")
    for player in effiency(sg_list):
        print(player)
    print("G")
    for player in effiency(g_list):
        print(player)
    print("SF")
    for player in effiency(sf_list):
        print(player)
    print("F")
    for player in effiency(f_list):
        print(player)
    print("PF")
    for player in effiency(pf_list):
        print(player)
    print("C")
    for player in effiency(c_list):
        print(player)
    print("UTIL")
    for player in effiency(players):
        print(player)


    
if __name__ == '__main__':
    main()