import csv
import itertools
import random
import multiprocessing
n_starts = 0

def rankPlayers(min_max = True):
    
    players = extractPlayers()
    individual_contribution = [sum(normalizedScore([individual]*15, min_max)) for individual in players]
    ranked_players = [x for _, x in sorted(zip(individual_contribution, players), key=lambda pair: pair[0], reverse=True)]
    return ranked_players

def randomStart(players, teamsize = 15):
    return random.sample(players,teamsize)

def evaluateSquad(cur_squad, potential_squad):
    avgs = averages(potential_squad)
    cur_avgs = averages(cur_squad)
    win_counter = 0
    for category in cur_avgs:
        win_counter += battle(cur_avgs, avgs, category)
    return win_counter

def geneticOptimization(players, population_size=200, generations=500, mutation_rate= 0.7, crossover_rate=0.8, elitism_rate=0.05, min_max = False):

    best_individual = None
    population = initializePopulation(players, population_size)
    best_fitness = float("-inf")
    fitness_scores = []
    selected_parents = []
    num_elites = int(elitism_rate * population_size)
    stagnation_counter = 0
    generation = 0
    while(stagnation_counter <= generations):

        fitness_scores = [sum(normalizedScore(individual, min_max)) for individual in population]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
        #elites wont have to compete, no mutations or crossover for them either >:^)
        selected_parents = [tournamentSelection(sorted_population[num_elites:],narrow_categories=min_max) for _ in range(population_size)]

        #always yoink the best lads
        new_population = sorted_population[:num_elites].copy()

        for i in range(0, population_size, 2):
            parent_one = selected_parents[i].copy()
            parent_two = selected_parents[i + 1].copy()
            if random.uniform(0, 1) < crossover_rate:
                child_one, child_two = crossOver(parent_one, parent_two)
                if random.uniform(0, 1) < mutation_rate:
                    child_one = mutate(players, child_one).copy()
                    child_two = mutate(players, child_two).copy()
                new_population.extend([child_one.copy(), child_two.copy()])
            else:
                if random.uniform(0, 1) < mutation_rate:
                    new_population.extend([mutate(players, parent_one, min_max), mutate(players, parent_two, min_max)])
                else:
                    new_population.extend([parent_one.copy(), parent_two.copy()])
        narrow_cats = min_max
        current_best_fitness = sum(normalizedScore(sorted_population[0], min_max=narrow_cats))
        if current_best_fitness > best_fitness:
            print(f"Changing up best individual because: {current_best_fitness} > {best_fitness}")
            if current_best_fitness - best_fitness >= 0.01:
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            print(f"new best team with fitness: {current_best_fitness}")
            for player in sorted_population[0]:
                print(player['Name'])
            print("------------------------------------------------------------")
            best_fitness = current_best_fitness
            best_individual = sorted_population[0].copy()
        else:
            stagnation_counter += 1
        #add the best individual to the next generation
        new_population.extend([best_individual])
        population =  new_population[:]
        if(generation + 1)%100 == 0 or generation == 0:
            print(f"Generation: {generation + 1}")
            print(f"best of this generation: {current_best_fitness} Overall best:{best_fitness}")
        generation += 1
    '''
    print("getting the values for sorted population[0], population[0] and best_individual")
    for score in [sum(normalizedScore(sorted_population[0], True)), sum(normalizedScore(population[0])), sum(normalizedScore(best_individual))]:
        print(score)
    '''
    for val in normalizedScore(best_individual, min_max):
        print(val)
    return best_individual

def initializePopulation(players, population_size = 100, team_size = 15):
    #create teams equal to the number of populations
    populations = []
    for i in range(population_size):
        populations.append(randomStart(players))
    return populations

def tournamentSelection(population, tournament_size = 3, narrow_categories = False):
    participants = random.sample(population, tournament_size)
    fitness_scores = []
    for participant in participants:
        fitness_scores.append(normalizedScore(participant, narrow_categories))
    return participants[fitness_scores.index(max(fitness_scores))]

def crossOver(parent_1, parent_2):
    crossover_point = random.randint(1, len(parent_1) - 1)
    
    # The crossover operation
    child_one = parent_1[:crossover_point]
    child_two = parent_2[:crossover_point]
    for player in parent_2[crossover_point:]:
        while player in child_one:
            player = random.choice(parent_2)
        child_one.append(player)    
    for player in parent_1[crossover_point:]:
        while player in child_two:
            player = random.choice(parent_1)
        child_two.append(player)
    return (child_one, child_two)

def positiveMutation(players, individual, narrow_categories = False):
    
    cur_score = sum(normalizedScore(individual, narrow_categories))
    index_to_mutate = random.randint(0, len(individual) - 1)
    temp_score = sum(normalizedScore(individual, narrow_categories))
    #keep picking a new random player to swap into our chosen spot until score improves
    n_attempts = 0
    while cur_score >= temp_score and n_attempts < len(players):
        mutant = random.choice(players)
        temp_squad = individual[:]
        if mutant not in temp_squad:
            temp_squad[index_to_mutate] = mutant
            temp_score = sum(normalizedScore(temp_squad, narrow_categories))
            n_attempts += 1

    return temp_squad

def BruteMutation(players, individual):
    cur_score = sum(normalizedScore(individual))
    temp_score = float("-inf")
    #keep picking a new random player to swap into our chosen spot until score improves
    n_attempts = 0
    while cur_score >= temp_score and n_attempts < len(players):
        mutants = random.sample(players, 3)
        temp_squad = individual[:]
        temp_squad.extend(player for player in mutants if player not in temp_squad)
        temp_squad = bruteForce(temp_squad)
        temp_score = sum(normalizedScore(temp_squad))
        n_attempts += 1
    return temp_squad

def mutate(players, individual, min_max = False):
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
    best_squad = max(results, key=lambda squad: sum(normalizedScore(squad, True)))    
    return best_squad

n_runs = 1

def hillClimbSingleRun(players, team_size, max_iterations):
    global n_runs
    print(f"run #{n_runs}")
    n_runs += 1
    cur_squad = randomStart(players, team_size)
    cur_score = sum(normalizedScore(cur_squad, True))
    for _ in range(max_iterations):
        neighbour_squad = cur_squad[:]
        index_to_swap = random.randint(0, team_size - 1)
        new_player = random.choice([p for p in players if p not in cur_squad])
        neighbour_squad[index_to_swap] = new_player
        neighbor_score = sum(normalizedScore(neighbour_squad, True))
        if neighbor_score > cur_score:
            cur_squad = neighbour_squad[:]
            cur_score = neighbor_score
    return cur_squad


    

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
    total_ftm = 0
    for player in team:
        total_pts += player["PTS"]
        total_fga += player["FGA"]
        total_3pa += player["3PTA"]
        total_fgm += player["FGM"]
        total_3pm += player["3PM"]
        total_ftm += player["FTM"]
        total_pts += player["PTS"]
        total_reb += player["REB"]
        total_ast += player["AST"]
        total_stl += player["STL"]
        total_blk += player["BLK"]
        total_to += player["TO"]
        total_pf += player["PF"]

    averages["PTS"] = total_pts
    averages["FGM"] = total_fgm
    averages["3PTM"] = total_3pm
    averages["FG%"] = total_fgm/total_fga
    if total_3pa:
        averages["3PT%"] = total_3pm/total_3pa
    else:
        averages["3PT%"] = 0
    averages["FTM"] = total_ftm
    averages["REB"] = total_reb#/len(team)
    averages["AST"] = total_ast#/len(team)
    averages["STL"] = total_stl#/len(team)
    averages["BLK"] = total_blk#/len(team)
    if total_to:
        averages["A/T"] = total_ast/total_to
    else:
        averages["A/T"] = total_ast

    averages["PF"] = -total_pf#/len(team) 
    
    return averages

def bruteForce(players, teamsize=15, Optimize = False):
    best_squad = None
    best_score = float("-inf")
    for squad in (itertools.combinations(players, teamsize)):
        score = sum(normalizedScore(squad), Optimize)
        if score > best_score:
            best_squad = squad[:]
            best_score = score
    if not best_squad:
        return players[:teamsize]
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


def normalizedScore(squad, min_max = False):

    stats = averages(squad)
    #MY USUAL DUMP STATS: 
    min_Pts = 27522.0
    max_Pts = 34444.0
    min_fgm = 5129.0
    max_fgm = 6132.0
    min_3ptm = 1400.1
    max_3ptm = 1688.8
    min_ftm =  2093.7000000000003
    maX_ftm = 3322.2000000000003

    #the handsome non dump stats below:
    min_FG_percent =0.4680916030534351
    max_FG_percent =  0.4969110035064285
    min_ThreePt_percent =  0.36287005192528154
    max_ThreePt_percent =  0.38920660491341114
    min_REB =  4600.0
    max_REB =  5524.0
    min_AST = 3329.9
    max_AST = 4068.2
    min_STL = 765.4999999999999
    max_STL = 932.6000000000003
    min_BLK = 610.5
    max_BLK = 718.8000000000001
    min_AT =  1.997520314538518
    max_AT = 2.125717081989732
    min_PF =  -2112.8
    max_PF =  -1812.6
    # Normalize each statistic, each stat is also weighted by 1/Number of categories
    normalized_stats = []
    n_categories = 12
    category_cap = 1.05
    if min_max:
        n_categories = 5
#dump categories
    normalized_stats.append((stats["PTS"] - min_Pts)/(max_Pts - min_Pts)*(1/n_categories))
    normalized_stats.append((stats["FGM"] - min_fgm)/(max_fgm - min_fgm)*(1/n_categories))
    normalized_stats.append((stats["FTM"] - min_ftm)/(maX_ftm - min_ftm)*(1/n_categories))
    normalized_stats.append((stats["3PTM"] - min_3ptm)/(max_3ptm - min_3ptm)*(1/n_categories))



#category used in calculation
    normalized_stats.append((stats["A/T"] - min_AT) / (max_AT - min_AT)*(1/n_categories))
    normalized_stats.append((stats["PF"]- min_PF) / (max_PF - min_PF)*(1/n_categories))

    normalized_stats.append((stats["AST"] - min_AST) / (max_AST - min_AST)*(1/n_categories))
    normalized_stats.append((stats['BLK'] - min_BLK)/ (max_BLK - min_BLK)*(1/n_categories))

    normalized_stats.append((stats["STL"] - min_STL) / (max_STL - min_STL)*(1/n_categories)) 
    normalized_stats.append((stats["3PT%"] - min_ThreePt_percent) / (max_ThreePt_percent - min_ThreePt_percent)*(1/n_categories))
    normalized_stats.append((stats["FG%"] - min_FG_percent) / (max_FG_percent - min_FG_percent)*(1/n_categories))




    normalized_stats.append((stats["REB"] - min_REB) / (max_REB - min_REB)*(1/n_categories)) 


    best_stats = []
    #weight everything AND then we also cap the values at 15% higher because realistically 10% should be a good enough margin
    #if you're ahead of the maximum by more than that you're over investing in a category
    #I can make this more fancy later for now the first 4 cat's are my dumps
    if min_max:

        for i in range(12 - n_categories):
            normalized_stats[i] = normalized_stats[i]*0
        #normalized_stats[12 - n_categories] = normalized_stats[12 - n_categories]/2

    #let's enforce our cap >:^)
    for i in range(len(normalized_stats)):
        normalized_stats[i] = min(normalized_stats[i],category_cap *(1/n_categories))


    
    return normalized_stats

def matchUp(opponent, squad): 

    other_team = (extractPlayers(opponent))
    other_team = bruteForce(other_team)
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
            #print(player_info)
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
            if not temp_player["A/T"]:
                temp_player["A/T"] += 1
            temp_player["TO"] = temp_player["AST"]/temp_player["A/T"]
            temp_player["PF"] = float(player_info[14 + size_delta])
            players.append(temp_player)

    return players

def greedyAlgo(players, team_size = 15, min_max = True):
    result = rankPlayers(min_max)
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

def weeklyFreeAgents():

    players = extractPlayers("weeklyFAs.csv")
    for player in players:
        print(player['Name'])

    hill_squad = geneticOptimization(players)
    print("---------------------------------------------------------------------")
    print(f"Here is our Optimized Squad")
    for player in hill_squad:
        print(f"{player['Name']}")
    print("---------------------------------------------------------------------")
    return hill_squad    



def main():

    narrow_Categories = True
    roster = extractPlayers("currentroster.csv")  
    roster = bruteForce(roster, 15, narrow_Categories)
    players = extractPlayers()
    print("Optimized version of our roster")
    for player in roster:
        print(player['Name'])
    print(f"With a score of {sum(normalizedScore(roster, narrow_Categories))}")
    print("-"*30)
    optimized_squad = geneticOptimization(players, min_max=narrow_Categories)
    print(f"Now let's do some theoretical matchups:")
    for opp in ["Slim reaper.csv", "Jimmy's Buckets.csv", "Dunk Daddies.csv", "Year of the Timberwolf.csv"]:

        matchUp(opp, optimized_squad)
    print("---------------------------------------------------------------------------------------------------")
    print("Now let's compare our optimized squad to our bruteforced roster -> is it worth getting free agents?")
    optimized_avg = averages(optimized_squad)
    roster_avg = averages(roster)
    for category in optimized_avg:
        print(f"Category: {category } Optimized Squad: {optimized_avg[category]} Brute force: {roster_avg[category]}")
    
    print(f"Optimized squad Score: {sum(normalizedScore(optimized_squad, narrow_Categories))} Brute force Score: {sum(normalizedScore(roster, narrow_Categories))}")
    print("Optimized SQUAD:")
    for player in optimized_squad:
        print(f"{player['Name']}")
    ranked_players = rankPlayers(narrow_Categories)
    print("the TOP 20 Players Ranked and their individual contribution:")
    for player in ranked_players[:20]:
        print(player['Name'], sum(normalizedScore([player]*15,narrow_Categories)))
    
if __name__ == '__main__':
    main()
