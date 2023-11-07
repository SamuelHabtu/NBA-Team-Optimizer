import csv

def bangForBuck(players):
    #sorts players by bang for buck -> FFPG/ (salary)
    for i, player in enumerate(players):
        player["bang for buck"] = player["FFPG"]/ player["Salary"]

    print(len(players))
    players = sorted(players, key = lambda p:p["bang for buck"], reverse= True)
    return players

def adjBangforBuck(players):
    #sorts players by adjusted bang for buck -> FFPG/ (salary * std.deviation )
    for player in players:
        if not player["std Dev"]:
            player["std Dev"] = 99999999999999999999999999999999999
        player["adjusted bang for buck"] = player["FFPG"]/ (player["Salary"] * player["std Dev"])

    players = sorted(players, key = lambda p:p["adjusted bang for buck"], reverse = True)
    return players

def effiency(players):
    #given a list of players it returns the best players 15 if we compare change in FFPG/change in price
    #if the change in FFPG/change in price is less than 1, then swapping the players is ideal
    #we will then pop the winner into the winners list so we have an ordered list of winners 
    winners = []
    while(len(winners) < 15):
        cur_winner = 0
        for i in range(len(players)):
            player = players[i]
            leader = players[cur_winner]
            delta_ffpg = leader["FFPG"] - player["FFPG"]
            delta_price = leader["Salary"] - player["Salary"]
            if( delta_price == 0):
                if delta_ffpg < 0:
                    #higher ffpg wins in this case
                    cur_winner = i
            else:
                ratio = abs(delta_ffpg/delta_price)
            
                #if the ratio is < 1 then we SHOULD swap
                #if it is 1 then it's a draw and whoever should win is subjective, I am listing a top 15 so hopefully this isnt a problem
                if(ratio < 1):
                    cur_winner = i

        #we take whoever won the guantlet out of the list, so they dont influence future guantlets -> prevents duplicate answers
        winners.append(players.pop(cur_winner))
    return winners

def main():
    players = []
    with open('Yahoo cup - Sheet1.csv', newline = '') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvdata:
            temp_player = {}
            temp_player["position"] = row[0]
            temp_player["Name"] = row[1]
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