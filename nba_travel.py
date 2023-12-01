import itertools
import random
import csv

# random.seed(10)

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

def create_initial_population(starting_team, max_away_games, team_count, population_size, distance_matrix):
    population = []

    for _ in range(population_size):
        route = [starting_team]
        remaining_teams = set(range(team_count)) - {starting_team}

        while remaining_teams:
            if len(route) % (max_away_games + 1) == 0:
                # Time to return to the starting team
                route.append(starting_team)
            else:
                # Choose the next team based on proximity
                last_team = route[-1]
                closest_teams = sorted(remaining_teams, key=lambda x: distance_matrix[last_team][x])
                
                # Introduce some randomness in selecting the next team
                next_team = random.choice(closest_teams[:3])  # Choose among the three closest teams
                route.append(next_team)
                remaining_teams.remove(next_team)

        # Ensure the route ends with the starting team
        if route[-1] != starting_team:
            route.append(starting_team)

        population.append(route)

    return population


def calculate_fitness(route, distance_matrix):
    return 1 / calculate_total_distance(route, distance_matrix)

def select_parents(population, fitness):
    total_fitness = sum(fitness)
    selection_probs = [f / total_fitness for f in fitness]
    return random.choices(population, weights=selection_probs, k=2)

def ordered_crossover(parent1, parent2, starting_team, max_away_games):
    # Create a template for the child that places the starting team at the correct positions
    child_template = [starting_team if i % (max_away_games + 1) == 0 else None for i in range(len(parent1))]

    # Create a set of all teams except the starting team
    teams = set(range(len(parent1)))
    teams.remove(starting_team)

    # Fill in the child template with teams from parents, ensuring no duplicates
    for i in range(1, len(parent1) - 1):
        if child_template[i] is None:
            if parent1[i] in teams:
                child_template[i] = parent1[i]
                teams.remove(parent1[i])
            elif parent2[i] in teams:
                child_template[i] = parent2[i]
                teams.remove(parent2[i])

    # Fill any remaining positions with leftover teams
    for i in range(1, len(parent1) - 1):
        if child_template[i] is None:
            child_template[i] = teams.pop()

    # Return parent if theres an issue
    for i in range(len(child_template)):
        if child_template[i] is None:
            return parent1

    return child_template

def swap_mutation(route, mutation_rate, starting_team, max_away_games):
    new_route = route[:]
    for _ in range(len(new_route) * 2):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(1, len(new_route) - 1), 2)
            # Ensure these are not starting_team positions
            if new_route[idx1] != starting_team and new_route[idx2] != starting_team:
                new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
    return new_route

def genetic_tsp(starting_team, max_away_games, teams, distance_matrix, population_size, generations, mutation_rate):
    team_count = len(teams)
    population = create_initial_population(starting_team, max_away_games, team_count, population_size, distance_matrix)
    best_route_overall = None
    min_distance_overall = float('inf')

    for generation in range(generations):
        fitness = [calculate_fitness(route, distance_matrix) for route in population]
        new_population = []
        
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness)
            child = ordered_crossover(parent1, parent2, starting_team, max_away_games)
            child = swap_mutation(child, mutation_rate, starting_team, max_away_games)
            new_population.append(child)

        population = new_population

        # Check for the best route in this generation
        for route in population:
            total_distance = calculate_total_distance(route, distance_matrix)
            if total_distance < min_distance_overall:
                best_route_overall = route
                min_distance_overall = total_distance

        print(f"Generation {generation + 1}: Best Route = {best_route_overall}, Distance = {min_distance_overall}")

    return best_route_overall, min_distance_overall

def read_arena_mapping(file_name):
    team_to_arena = {}
    with open(file_name, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team_name = row['teamname']
            arena_name = row['arena_name']
            team_to_arena[team_name] = arena_name
    return team_to_arena

def read_distance_matrix(file_name, arenas):
    # Initialize the distance matrix with zeros
    size = len(arenas)
    distance_matrix = [[0 for _ in range(size)] for _ in range(size)]

    # Read the CSV file and populate the distance matrix
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stadium1 = row['Stadium 1']
            stadium2 = row['Stadium 2']
            distance = float(row['Distance (km)'])

            s1index, s2index = -1, -1
            for i, stadium in enumerate(arenas):
                if stadium1 == stadium:
                    s1index = i
                elif stadium2 == stadium:
                    s2index = i

                i, j = s1index, s2index
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance 

    return distance_matrix


def main():
    team_to_arena = read_arena_mapping('arenas_list.csv')
    teams = [
        "Toronto Raptors", "Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Indiana Pacers",
        "Chicago Bulls", "Miami Heat", "Atlanta Hawks", "Charlotte Hornets", "Cleveland Cavaliers", "Detroit Pistons",
        "Orlando Magic", "Washington Wizards", "Denver Nuggets", "Milwaukee Bucks",
        "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz",
        "Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns",
        "Sacramento Kings", "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans",
        "San Antonio Spurs"
    ]
    arenas = [team_to_arena[team] for team in teams]
    print(teams)
    print(arenas)

    # distance_matrix = generate_dummy_distance_matrix(len(teams))

    distance_matrix = read_distance_matrix('nba_stadium_distances.csv', arenas)
    print(distance_matrix)

    starting_team = teams.index("Toronto Raptors")
    max_away_games = 5
    
    # shortest_tour, min_distance = brute_force_tsp(starting_team, max_away_games, teams, distance_matrix)
    
    population_size = 2000  # population size
    generations = 1000     # number of generations
    mutation_rate = 0.2    # mutation rate
    shortest_tour, min_distance = genetic_tsp(starting_team, max_away_games, teams, distance_matrix, population_size, generations, mutation_rate)
    
    print("Shortest Tour:", " -> ".join(teams[team] for team in shortest_tour))
    print("Minimum Total Distance:", min_distance)

if __name__ == '__main__':
    main()
