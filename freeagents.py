import csv

def main():
    players = []
    with open('freeagents.csv', newline = '') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for row in csvdata:
            print(row)
            temp_player = {}
            temp_player["Player"] = row[0]
            temp_player["GP"] = row[1]
            temp_player["FFPG"] = float(row[2][-4:])
            temp_player["std Dev"] = float(row[3])
            temp_player["Salary"] = int(row[4][1:])
            if temp_player["std Dev"]:
                #only add the player if they have a std. Dev-> basically rules out any one hit wonder players
                players.append(temp_player)

    #players = bangForBuck(players)
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