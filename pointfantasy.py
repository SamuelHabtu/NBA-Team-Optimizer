from itertools import combinations

def anycomb(items):
    'return combinations of any length from the items '
    return ( comb
             for r in range(1, len(items)+1)
             for comb in combinations(items, r)
             )

def totalvalue(comb):
    ' Totalise a particular combination of items'
    totwt = totval = 0
    for item, wt, val in comb:
        totwt  += wt
        totval += val
    return (totval, -totwt) if totwt <= 400 else (0, 0)





def main():
    # Example usage:
    players = [
    {"position": "C", "name": "Nikola Jokic", "salary": 56, "FPPG": 57.3},
    {"position": "C", "name": "Anthony Davis", "salary": 51, "FPPG": 52.7},
    {"position": "SF", "name": "LeBron James", "salary": 45, "FPPG": 50.3},
    {"position": "SG", "name": "Devin Booker", "salary": 45, "FPPG": 44.8},
    {"position": "PF", "name": "Kevin Durant", "salary": 44, "FPPG": 48.3},
    {"position": "SG", "name": "Stephen Curry", "salary": 43, "FPPG": 46.8},
    {"position": "PG", "name": "Jamal Murray", "salary": 37, "FPPG": 38.1},
    {"position": "PG", "name": "Bradley Beal", "salary": 32, "FPPG": 37.8},
    {"position": "PG", "name": "Chris Paul", "salary": 27, "FPPG": 36.1},
    {"position": "PF", "name": "Andrew Wiggins", "salary": 26, "FPPG": 31.2},
    {"position": "C", "name": "Draymond Green GTD", "salary": 25, "FPPG": 30.5},
    {"position": "SG", "name": "Austin Reaves", "salary": 21, "FPPG": 24.0},
    {"position": "PF", "name": "Aaron Gordon", "salary": 21, "FPPG": 30.8},
    {"position": "SF", "name": "Klay Thompson", "salary": 21, "FPPG": 31.3},
    {"position": "C", "name": "Jusuf Nurkic", "salary": 21, "FPPG": 31.2},
    {"position": "SF", "name": "Michael Porter Jr. GTD", "salary": 19, "FPPG": 27.8},
    {"position": "C", "name": "Kevon Looney", "salary": 19, "FPPG": 25.7},
    {"position": "PG", "name": "D'Angelo Russell", "salary": 16, "FPPG": 30.8},
    {"position": "SG", "name": "Kentavious Caldwell-Pope", "salary": 14, "FPPG": 22.3},
    {"position": "C", "name": "Christian Wood", "salary": 13, "FPPG": 30.9},
    {"position": "PF", "name": "Jarred Vanderbilt GTD", "salary": 13, "FPPG": 21.5},
    {"position": "PG", "name": "Gabe Vincent GTD", "salary": 13, "FPPG": 18.1},
    {"position": "SF", "name": "Keita Bates-Diop", "salary": 12, "FPPG": 18.5},
    {"position": "C", "name": "Drew Eubanks", "salary": 12, "FPPG": 19.7},
    {"position": "SF", "name": "Taurean Prince", "salary": 10, "FPPG": 15.3},
    {"position": "PF", "name": "Jaxson Hayes", "salary": 10, "FPPG": 11.4},
    {"position": "PF", "name": "Rui Hachimura", "salary": 10, "FPPG": 19.2},
    {"position": "SF", "name": "Cam Reddish", "salary": 10, "FPPG": 17.3},
    {"position": "SF", "name": "Max Christie", "salary": 10, "FPPG": 6.3},
    {"position": "SF", "name": "Maxwell Lewis", "salary": 10, "FPPG": 0.0},
    {"position": "PG", "name": "Jalen Hood-Schifino GTD", "salary": 10, "FPPG": 0.0},
    {"position": "SG", "name": "D'Moi Hodge", "salary": 10, "FPPG": 0.0},
    {"position": "C", "name": "Colin Castleton", "salary": 10, "FPPG": 0.0},
    {"position": "SF", "name": "Alex Fudge", "salary": 10, "FPPG": 0.0},
    {"position": "C", "name": "DeAndre Jordan", "salary": 10, "FPPG": 13.1},
    {"position": "PG", "name": "Reggie Jackson", "salary": 10, "FPPG": 17.1},
    {"position": "SF", "name": "Justin Holiday", "salary": 10, "FPPG": 9.2},
    {"position": "PF", "name": "Vlatko Cancar INJ", "salary": 10, "FPPG": 10.0},
    {"position": "C", "name": "Zeke Nnaji", "salary": 10, "FPPG": 9.8},
    {"position": "C", "name": "Jay Huff GTD", "salary": 10, "FPPG": 15.3},
    {"position": "SF", "name": "Braxton Key", "salary": 10, "FPPG": 1.7},
    {"position": "SG", "name": "Christian Braun GTD", "salary": 10, "FPPG": 10.1},
    {"position": "PF", "name": "Peyton Watson", "salary": 10, "FPPG": 6.4},
    {"position": "PG", "name": "Collin Gillespie", "salary": 10, "FPPG": 0.0},
    {"position": "PF", "name": "Hunter Tyson", "salary": 10, "FPPG": 0.0},
    {"position": "PG", "name": "Jalen Pickett", "salary": 10, "FPPG": 0.0},
    {"position": "SG", "name": "Julian Strawther GTD", "salary": 10, "FPPG": 0.0},
     {"position": "SG", "name": "Bryce Wills", "salary": 10, "FPPG": 0.0},
    {"position": "PG", "name": "Quinndary Weatherspoon", "salary": 10, "FPPG": 0.0},
    {"position": "SG", "name": "Eric Gordon", "salary": 10, "FPPG": 20.0},
    {"position": "SG", "name": "Damion Lee INJ", "salary": 10, "FPPG": 13.4},
    {"position": "SF", "name": "Josh Okogie", "salary": 10, "FPPG": 15.9},
    {"position": "C", "name": "Chimezie Metu", "salary": 10, "FPPG": 10.4},
    {"position": "PF", "name": "Yuta Watanabe", "salary": 10, "FPPG": 11.3},
    {"position": "PF", "name": "Bol Bol", "salary": 10, "FPPG": 20.8},
    {"position": "C", "name": "Udoka Azubuike", "salary": 10, "FPPG": 9.2},
    {"position": "PG", "name": "Saben Lee", "salary": 10, "FPPG": 13.7},
    {"position": "SG", "name": "Jordan Goodwin", "salary": 10, "FPPG": 17.7},
    {"position": "SF", "name": "Ish Wainright GTD", "salary": 10, "FPPG": 10.0},
    {"position": "PG", "name": "Cory Joseph", "salary": 10, "FPPG": 15.4},
    {"position": "C", "name": "Dario Saric", "salary": 10, "FPPG": 12.9},
    {"position": "SF", "name": "Gary Payton II", "salary": 10, "FPPG": 13.8},
    {"position": "PF", "name": "Jonathan Kuminga", "salary": 10, "FPPG": 16.9},
    {"position": "SG", "name": "Moses Moody", "salary": 10, "FPPG": 9.2},
    {"position": "PG", "name": "Lester Quinones", "salary": 10, "FPPG": 3.6},
    {"position": "PF", "name": "Trayce Jackson-Davis", "salary": 10, "FPPG": 0.0},
    {"position": "SG", "name": "Brandin Podziemski", "salary": 10, "FPPG": 0.0},
    {"position": "C", "name": "Usman Garuba", "salary": 10, "FPPG": 11.5},
    {"position": "SF", "name": "Rodney McGruder", "salary": 10, "FPPG": 11.1},
    {"position": "PF", "name": "Rudy Gay", "salary": 10, "FPPG": 11.6},
    {"position": "SG", "name": "Grayson Allen", "salary": 10, "FPPG": 19.8},
    {"position": "PF", "name": "Nassir Little", "salary": 10, "FPPG": 12.7},
    {"position": "SF", "name": "Keon Johnson", "salary": 10, "FPPG": 9.1},
    {"position": "SG", "name": "Jerome Robinson", "salary": 10, "FPPG": 0.0}
    ]
    items = tuple((player["name"], player["salary"],int(player["FPPG"])) for player in players)
    print(items)
    positions = ["PG", "SG", "G", "SF", "PF", "F", "C", "UTIL"]
    capacity = 200  # The salary cap for Yahoo Cup

    selected_players = max(anycomb(items),200)
    val, wt = totalvalue(selected_players)
    print("Selected Players:")
    for player in selected_players:
        print(player)


    
if __name__ == "__main__":
    main()