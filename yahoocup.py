import csv
import random
import multiprocessing

n_runs = 1
def randomStart(players):
    chosen_players = dict({})
    for position in players:
        pick = random.choice(players[position])
        #no duppies >:^)
        while pick in chosen_players.values():
            pick = random.choice(players[position])
        chosen_players[position] = pick
    return chosen_players

def salaryCheck(squad, cap = 200):

    for player in squad:
        cap -= squad[player]["Salary"]
    #this returns True or False aka 1 or 0
    return cap >= 0

def evaluateSquad(squad):
    score = 0
    for player in squad:
        score += squad[player]["FFPG"]
    return score * salaryCheck(squad)

def hillClimb(players,num_restarts = 6420, max_iterations = 500, num_processes = 4):
    print(f"searching through: {len(players)} players, with {num_restarts} restarts and {max_iterations} iterations split up into {num_processes} threads")
    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.starmap(hillClimbSingleRun, [(players,max_iterations) for _ in range(num_restarts)])
    pool.close()
    pool.join()
    best_squad = max(results, key=lambda squad: evaluateSquad(squad))    
    return best_squad

def hillClimbSingleRun(players, max_iterations):

    global n_runs

    cur_squad = randomStart(players)
    cur_score = evaluateSquad(cur_squad)
    best_squad = cur_squad
    best_score = cur_score
    for _ in range(max_iterations):
        neighbour_squad = dict(cur_squad) #make a shallow copy
        position_to_swap = random.choice(list(cur_squad.keys()))
        new_player = random.choice([p for p in players[position_to_swap] if p not in cur_squad.values()])  # Exclude players already in squad
        neighbour_squad[position_to_swap] = new_player
        neighbour_score = evaluateSquad(neighbour_squad)
        if neighbour_score > cur_score:
            cur_squad = dict(neighbour_squad)
            cur_score = neighbour_score
            if cur_score > best_score:
                best_squad = cur_squad
                best_score = cur_score
    print(f"This thread is on run #{(n_runs)}")
    n_runs += 1
    return best_squad

def geneticOptimization(players, population_size=5000, generations=200, mutation_rate= 0.5, crossover_rate=0.6, elitism_rate=0.05, min_max = False):

    best_individual = None
    population = initializePopulation(players)
    best_fitness = float("-inf")
    fitness_scores = []
    selected_parents = []
    num_elites = int(elitism_rate * population_size)
    for generation in range(generations):
        fitness_scores = [evaluateSquad(individual) for individual in population]
        selected_parents = [tournamentSelection(population) for _ in range(population_size)]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
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
        
        current_best_fitness = evaluateSquad(sorted_population[0])
        if current_best_fitness > best_fitness:
            print(f"Changing up best individual because: {current_best_fitness} > {best_fitness}")
            print(f"new best team with fitness: {current_best_fitness}")
            for slot in sorted_population[0]:
                print(f"{slot}: {sorted_population[0][slot]}")
            print("------------------------------------------------------------")
            best_fitness = current_best_fitness
            best_individual = sorted_population[0].copy()

        #add the best individual to the next generation
        new_population.extend([best_individual])
        population =  new_population[:]
        if(generation + 1)%1 == 0 or generation == 0:
            print(f"Generation: {generation + 1}")
            print(f"best of this generation: {current_best_fitness} VS {best_fitness}")
    '''
    print("getting the values for sorted population[0], population[0] and best_individual")
    for score in [sum(normalizedScore(sorted_population[0], True)), sum(normalizedScore(population[0])), sum(normalizedScore(best_individual))]:
        print(score)
    '''
    return best_individual

def initializePopulation(players, population_size = 100, team_size = 15):
    #create teams equal to the number of populations
    populations = []
    for i in range(population_size):
        populations.append(randomStart(players))
    return populations

def tournamentSelection(population, tournament_size = 3):
    participants = random.sample(population, tournament_size)

    fitness_scores = []
    for participant in participants:
        fitness_scores.append(evaluateSquad(participant))
    return participants[fitness_scores.index(max(fitness_scores))]
def commonPlayers(squada, squadb):
    common_players = []
    for slot in squada:
        if squada[slot] in squadb.values():
            common_players.append(squada[slot])
    return common_players
def crossOver(parent_1, parent_2):
    
    common_values = commonPlayers(parent_1, parent_2)
    swappable_positions = list(parent_1.keys())
    for value in common_values:
        for position in swappable_positions:
            if parent_1[position] == value or parent_2[position] == value:
                swappable_positions.remove(position)

    #first we choose a random number of positions to swap
    num_positions_to_swap = random.randint(0,len(swappable_positions))
    #we randomly pick which positions to swap(instead of taking a chunk since the positioning of the swaps doesnt matter too much)
    positions_to_Swap = random.sample(swappable_positions, num_positions_to_swap)
    # The crossover operation -> we just do a little swaparoo
    for position in positions_to_Swap:
        parent_1[position], parent_2[position] = parent_2[position], parent_1[position]
    #now we check for conflicts e.g: parent_one has mitchell robinson as Center, while parent_two has mitchell robinson as Util
    #which could potentially lead to a goated(but illegal) squad with 2 mitchell robinsons

    return (parent_1, parent_2)


def mutate(players, individual, min_max = False):
    #pick a random slot to mutate
    position_to_mutate = random.choice(sorted(players.keys()))
    #snag a random player that fits that position
    mutated_player = random.choice(players[position_to_mutate])
    #avoiding repeated players(we wouldnt want the GOATED squad of all mitchell robinsons afterall)
    while mutated_player in individual.values():
        mutated_player = random.choice(players[position_to_mutate])

    individual[position_to_mutate] = mutated_player
    return individual


def extractPlayers(filenames = ["Yahoo Cup PGs.csv", "Yahoo Cup SGs.csv", "Yahoo Cup SFs.csv", "Yahoo Cup PFs.csv", "Yahoo Cup Cs.csv"]):
    players = dict({})
    players["PG"] = []
    players["SG"] = []
    players["SF"] = []
    players["PF"] = []
    players["C"] = []

    for file in filenames:
        with open(file, newline = '') as csvfile:
            csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        
            for player in csvdata:
                new_player = dict({"Name": player[0], "FFPG": float(player[1]), "Salary": int(player[2])})
                new_player["Name"] = player[0]
                new_player["FFPG"] = float(player[1])
                new_player["Salary"] = int(player[2])
                players[file[10:-5]].append(new_player)
    

    #Gotta remove duplicate Lads
    forwards = list(players["SF"])
    forwards.extend(x for x in players["PF"] if x not in forwards)
    guards = list(players["PG"])
    guards.extend(x for x in players["SG"] if x not in guards)
    centers = list(players["C"])
    players["F"] = forwards
    players["G"] = guards
    util = list(centers)
    util.extend(x for x in players["F"])
    util.extend(x for x in players["G"])
    players["Util"] = util
    return players

def printSquad(squad):

    for slot in squad:
        print(f"{slot} {squad[slot]['Name']}")
    total_ffpg = evaluateSquad(squad)
    print(f"for a combined FFPG: {total_ffpg} or an average ffpg of :{total_ffpg/len(squad.keys())}")

def main():
    
    players = extractPlayers()

    #hill_squad = hillClimb(players)
    gene_squad = geneticOptimization(players)
    hill_squad = gene_squad
    print(f"Let's see compare our results!")
    squads = dict({'Hill Squad: ': hill_squad, 'Gene Squad: ': gene_squad})
    for squad in (squads):
        print(f"Here is {squad}")
        printSquad(squads[squad])
        print("-"*25)
if __name__ == '__main__':
    main()