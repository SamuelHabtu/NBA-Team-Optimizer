import csv
import itertools
import random
import multiprocessing
n_starts = 0

def randomStart(players, teamsize = 15):
    return random.sample(players,teamsize)

def evaluateSquad(cur_squad, potential_squad):
    avgs = averages(potential_squad)
    cur_avgs = averages(cur_squad)
    win_counter = 0
    for category in cur_avgs:
        win_counter += battle(cur_avgs, avgs, category)
    return win_counter

def geneticOptimization(players, population_size=50, generations=16000, mutation_rate=0.6, crossover_rate=0.5, elitism_rate=0.1):


    best_individual = []
    population = initializePopulation(players)
    best_fitness = float("-inf")
    for generation in range(generations):
        fitness_scores = [sum(normalizedScore(individual)) for individual in population]
        selected_parents = [tournamentSelection(population) for _ in range(population_size)]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
        num_elites = int(elitism_rate * population_size)
        #always yoink the best lads
        new_population = sorted_population[:num_elites]

        for i in range(0, population_size, 2):
            parent_one = selected_parents[i]
            parent_two = selected_parents[i + 1]
            if random.uniform(0, 1) < crossover_rate:
                child_one = crossOver(parent_one, parent_two)
                child_two = crossOver(parent_one, parent_two)
                if random.uniform(0, 1) < mutation_rate:
                    child_one = mutate(players, child_one)
                    child_two = mutate(players, child_two)
                new_population.extend([child_one, child_two])
            else:
                if random.uniform(0, 1) < mutation_rate:
                    new_population.extend([mutate(players, parent_one), mutate(players, parent_two)])
                else:
                    new_population.extend([parent_one, parent_two])
        
        current_best_fitness = sum(normalizedScore(sorted_population[0]))
        if current_best_fitness > best_fitness:
            print(f"Changing up best individual because: {current_best_fitness} > {best_fitness}")
            print(f"new best team with fitness: {current_best_fitness}")
            for player in sorted_population[0]:
                print(player['Name'])
            print("------------------------------------------------------------")
            best_fitness = current_best_fitness
            best_individual = sorted_population[0].copy()
        new_population.extend([best_individual])
        population =  new_population[:]
        if(generation + 1)%100 == 0 or generation == 0:
            print(f"Generation: {generation + 1}")
            print(f"best of this generation: {current_best_fitness} VS {best_fitness}")
    print("getting the values for sorted population[0], population[0] and best_individual")
    for score in [sum(normalizedScore(sorted_population[0])), sum(normalizedScore(population[0])), sum(normalizedScore(best_individual))]:
        print(score)
            

    return population[0]

def initializePopulation(players, population_size = 100, team_size = 15):
    #create teams equal to the number of populations
    populations = []
    for i in range(population_size):
        populations.append(randomStart(players))
    return populations

def tournamentSelection(population, tournament_size = 3):
    participants = random.sample(population, tournament_size)
    return max(participants, key = normalizedScore)

def crossOver(parent_1, parent_2):
    crossover_point = random.randint(1, len(parent_1) - 1)
    
    # The crossover operation
    child = parent_1[:crossover_point] + [player for player in parent_2 if player not in parent_1[:crossover_point]]
    
    # Adjust the child size if it's too large
    if len(child) > len(parent_1):
        child = child[:len(parent_1)]

    return child
def mutate(players, individual):
    mutated_player = random.choice(players)
    #avoiding repeated players(we wouldnt want the GOATED squad of all mitchell robinsons afterall)
    while mutated_player in individual:
        mutated_player = random.choice(players)
    index_to_mutate = random.randint(0, len(individual) - 1)

    individual[index_to_mutate] = mutated_player
    return individual


def hillClimb(players, num_restarts=6420, max_iterations=400, team_size=15, num_processes=4):
    print(f"searching through: {len(players)} players, with {num_restarts} restarts and {max_iterations} iterations split up into {num_processes} threads")
    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.starmap(hillClimbSingleRun, [(players, team_size, max_iterations) for _ in range(num_restarts)])
    pool.close()
    pool.join()
    best_squad = max(results, key=lambda squad: sum(normalizedScore(squad)))    
    return best_squad

n_runs = 1

def hillClimbSingleRun(players, team_size, max_iterations):
    global n_runs
    print(f"run #{n_runs}")
    n_runs += 1
    cur_squad = randomStart(players, team_size)
    cur_score = sum(normalizedScore(cur_squad))
    for _ in range(max_iterations):
        neighbour_squad = cur_squad[:]
        index_to_swap = random.randint(0, team_size - 1)
        new_player = random.choice([p for p in players if p not in cur_squad])
        neighbour_squad[index_to_swap] = new_player
        neighbor_score = sum(normalizedScore(neighbour_squad))
        if neighbor_score > cur_score:
            cur_squad = neighbour_squad[:]
            cur_score = neighbor_score
    return cur_squad

def altHillClimb(players,num_restarts = 10000, max_iterations = 5000, team_size = 15):
    
    best_squad = optimize(extractPlayers("Jimmy's Buckets.csv"))
    for _ in range(num_restarts): 
        print(f"Start #{_ + 1}") 
        cur_squad = randomStart(players, team_size)
        for _ in range(max_iterations):
            neighbour_squad = cur_squad.copy()
            index_to_swap = random.randint(0, team_size - 1)
            new_player = new_player = random.choice([p for p in players if p not in cur_squad])  # Exclude players already in squad
            neighbour_squad[index_to_swap] = new_player
            cur_score = evaluateSquad(cur_squad, neighbour_squad)
            if evaluateSquad(cur_squad, neighbour_squad) > evaluateSquad(neighbour_squad, cur_squad):
                cur_squad = neighbour_squad[:]
                if evaluateSquad(best_squad, cur_squad) > evaluateSquad(cur_squad, best_squad):
                    best_squad = cur_squad[:]
                
    return best_squad

    

def averages(team):

    averages = {}
    if not team:
        print(f"None got sent into averages? LOL")
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

    if not total_3pa:
        total_3pa = float("0.000000000000000002")
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

def bruteForce(players, teamsize=15):
    best_squad = None
    best_score = float("-inf")
    for squad in (itertools.combinations(players, 15)):
        score = sum(normalizedScore(squad))
        if score > best_score:
            best_squad = squad[:]
            best_score = score
    return list(best_squad)

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
    max_FG_percent = 0.6
    
    min_ThreePt_percent = 0
    max_ThreePt_percent =  0.4
    
    min_REB = 0
    max_REB = 7553.0# Assuming this is the upper limit for rebounds 
    min_AST = 0
    max_AST = 5033.8  # You'll need to determine the maximum possible value for AST based on your league settings
    min_STL = 0
    max_STL = 948.9000000000001 # You'll need to determine the maximum possible value for STL based on your league settings
    min_BLK = 0
    max_BLK = 937.8 # You'll need to determine the maximum possible value for BLK based on your league settings
    min_AT = 0
    max_AT = 2.1169155231733954 # You'll need to determine the maximum possible value for A/T based on your league settings
    min_PF = 0  # You'll need to determine the minimum possible value for PF based on your league settings
    max_PF = -2240.5
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
        normalized_stats[i] = min(normalized_stats[i],0.15)
    
    return normalized_stats

def matchUp(opponent, squad): 

    other_team = (extractPlayers(opponent))
    enemy_avgs = averages((other_team))
    print("Succesfully got enemies")

    squad_avgs = averages(squad)
    print(f"Matchup vs {opponent[:-2]}")
    for category in enemy_avgs:
        print(f"{category}: My Squad: {squad_avgs[category]} Enemy Squad: {enemy_avgs[category]}")
    score = evaluateSquad(other_team, squad)
    print(f"is My Squad better? : {score > 6} , Expected Score of: {score}-{12- score}")


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

def greedyAlgo(players, team_size = 15):
    result = []
    for player in players:
        result.append((player,sum(normalizedScore([player]))))
    result = sorted(result, key = lambda info: info[1], reverse= True)
    for i in range(team_size):
        result[i] = result[i][0]
    return result[:team_size]

def freeAgents():

    freeAgents = extractPlayers()
    hill_squad = geneticOptimization(freeAgents)
    print("---------------------------------------------------------------------")
    print(f"Here is our Optimized Squad")
    for player in hill_squad:
        print(f"{player['Name']}")
    print("---------------------------------------------------------------------")
    return hill_squad

def main():
    
    roster = extractPlayers("currentroster.csv")  
    roster = bruteForce(roster)
    print("Optimized version of our roster")
    for player in roster:
        print(player['Name'])
    print("-"*30)
    hill_squad = freeAgents()
    #roster = bruteForce(players)
    print("-----------------------------------------------------------------------------------------------")
    print(f"Now let's do some theoretical matchups:")
    for opp in ["Slim reaper.csv", "Jimmy's Buckets.csv", "Dunk Daddies.csv", "Free throw merchants.csv"]:

        matchUp(opp, hill_squad)
    print("---------------------------------------------------------------------------------------------------")
    print("Now let's see if we've found the global maximum in this small squad")
    hill_avg = averages(hill_squad)
    roster_avg = averages(roster)
    for category in hill_avg:
        print(f"Category: {category } hill Squad: {hill_avg[category]} Brute force: {roster_avg[category]}")
    print(f"Hill squad Score: {sum(normalizedScore(hill_squad))} Brute force Score: {sum(normalizedScore(roster))}")
    print("Hill SQUAD:")
    for player in hill_squad:
        print(player['Name'])

if __name__ == '__main__':
    main()
