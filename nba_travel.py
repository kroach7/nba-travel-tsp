import itertools
import random

random.seed(10)

def generate_dummy_distance_matrix(size):
    """Generate a symmetric distance matrix with random distances."""
    matrix = [[0 if i == j else random.randint(50, 3000) for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            matrix[j][i] = matrix[i][j]  # Ensuring symmetry
    return matrix

def calculate_total_distance(route, distance_matrix):
    """Calculate the total distance of a route."""
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    return total_distance

def generate_valid_routes(starting_team, max_away_games, teams):
    valid_routes = []
    team_indices = list(range(len(teams)))  # Create a list of team indices
    team_indices.remove(starting_team)  # Remove starting team from the list

    # Generate permutations of the remaining teams
    for perm in itertools.permutations(team_indices):
        # Insert the starting team at intervals defined by max_away_games
        route = [starting_team]
        for i, team in enumerate(perm, 1):
            route.append(team)
            if i % max_away_games == 0:
                route.append(starting_team)

        # Ensure the route ends with the starting team
        if route[-1] != starting_team:
            route.append(starting_team)

        print(route)
        valid_routes.append(route)

    return valid_routes

def brute_force_tsp(starting_team, max_away_games, teams, distance_matrix):
    """Find the shortest tour using brute-force."""
    shortest_route = None
    min_distance = float('inf')
    
    for route in generate_valid_routes(starting_team, max_away_games, teams):
        total_distance = calculate_total_distance(route, distance_matrix)
        if total_distance < min_distance:
            min_distance = total_distance
            shortest_route= route

    return shortest_route, min_distance

def create_initial_population(starting_team, max_away_games, team_count, population_size):
    population = []
    for _ in range(population_size):
        route = [starting_team] + random.sample([i for i in range(team_count) if i != starting_team], team_count - 1)
        for i in range(max_away_games, len(route), max_away_games + 1):
            route.insert(i, starting_team)
        population.append(route)
    return population

def calculate_fitness(route, distance_matrix):
    return 1 / calculate_total_distance(route, distance_matrix)

def select_parents(population, fitness):
    total_fitness = sum(fitness)
    selection_probs = [f / total_fitness for f in fitness]
    return random.choices(population, weights=selection_probs, k=2)

def ordered_crossover(parent1, parent2, starting_team, max_away_games):
    # Remove the starting team from parents
    parent1_filtered = [team for team in parent1 if team != starting_team]
    parent2_filtered = [team for team in parent2 if team != starting_team]

    start, end = sorted(random.sample(range(len(parent1_filtered)), 2))
    child_filtered = [None] * len(parent1_filtered)
    child_filtered[start:end] = parent1_filtered[start:end]

    filled = set(parent1_filtered[start:end])
    position = end
    for city in parent2_filtered:
        if city not in filled:
            if position >= len(child_filtered):
                position = 0
            child_filtered[position] = city
            position += 1

    # Re-insert the starting team at the required intervals
    child = [starting_team]
    for i, team in enumerate(child_filtered):
        child.append(team)
        if (i + 1) % max_away_games == 0:
            child.append(starting_team)
    if child[-1] != starting_team:
        child.append(starting_team)

    return child

def swap_mutation(route, mutation_rate):
    new_route = route[:]
    for i in range(len(new_route)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(new_route) - 1)
            new_route[i], new_route[swap_with] = new_route[swap_with], new_route[i]
    return new_route

def genetic_tsp(starting_team, max_away_games, teams, distance_matrix, population_size, generations, mutation_rate):
    team_count = len(teams)
    population = create_initial_population(starting_team, max_away_games, team_count, population_size)

    for _ in range(generations):
        fitness = [calculate_fitness(route, distance_matrix) for route in population]
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness)
            child = ordered_crossover(parent1, parent2, starting_team, max_away_games)
            child = swap_mutation(child, mutation_rate)
            print(child)
            new_population.append(child)
        population = new_population


    shortest_route = None
    min_distance = float('inf')
    for route in population:
        total_distance = calculate_total_distance(route, distance_matrix)
        if total_distance < min_distance:
            min_distance = total_distance
            shortest_route= route

    return shortest_route, min_distance

def main():
    teams = [
        "Toronto Raptors", "Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Indiana Pacers",
        "Chicago Bulls", "Miami Heat", "Atlanta Hawks", "Charlotte Hornets", "Cleveland Cavaliers", #"Detroit Pistons"
        # "Orlando Magic", "Washington Wizards", "Denver Nuggets",
        # "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz",
        # "Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns",
        # "Sacramento Kings", "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans",
        # "San Antonio Spurs"
    ]
    distance_matrix = generate_dummy_distance_matrix(len(teams))
    print(distance_matrix)

    starting_team = teams.index("Toronto Raptors")
    max_away_games = 5
    
    # shortest_tour, min_distance = brute_force_tsp(starting_team, max_away_games, teams, distance_matrix)
    
    population_size = 2000  # Increase population size
    generations = 200     # Increase number of generations
    mutation_rate = 0.5    # Adjust mutation rate as needed
    shortest_tour, min_distance = genetic_tsp(starting_team, max_away_games, teams, distance_matrix, population_size, generations, mutation_rate)
    
    print("Shortest Tour:", " -> ".join(teams[team] for team in shortest_tour))
    print("Minimum Total Distance:", min_distance)

if __name__ == '__main__':
    main()
