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

def generate_valid_routes(starting_team, ending_team, max_away_games, teams):
    validRoutes = []
    permutations = itertools.permutations(range(len(teams)))
    for route in permutations:
        route = list(route)
        valid = True
        trip = 0
        if(route[trip] != starting_team):
            valid = False

        for trip in range(1, (len(teams))):
            if trip % (max_away_games + 1) == 0:
                dest = route[trip]
                route[trip] = starting_team
                route.append(dest)


        if valid == True:
            if(route[-1] != ending_team):
                route.append(ending_team)
            print(route)
            validRoutes.append(route)

    return validRoutes

def brute_force_tsp(starting_team, ending_team, max_away_games, teams, distance_matrix):
    """Find the shortest tour using brute-force."""
    shortest_route = None
    min_distance = float('inf')
    
    for route in generate_valid_routes(starting_team, ending_team, max_away_games, teams):
        total_distance = calculate_total_distance(route, distance_matrix)
        if total_distance < min_distance:
            min_distance = total_distance
            shortest_route= route

    return shortest_route, min_distance

def main():
    teams = [
        "Toronto Raptors", "Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Indiana Pacers",
        "Chicago Bulls", "Miami Heat", "Atlanta Hawks", "Charlotte Hornets", "Cleveland Cavaliers"
        # "Detroit Pistons", "Orlando Magic", "Washington Wizards", "Denver Nuggets",
        # "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz",
        # "Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns",
        # "Sacramento Kings", "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans",
        # "San Antonio Spurs"
    ]
    distance_matrix = generate_dummy_distance_matrix(len(teams))
    print(distance_matrix)

    starting_team = teams.index("Toronto Raptors")
    max_away_games = 5
    ending_team = starting_team
    
    shortest_tour, min_distance = brute_force_tsp(starting_team, ending_team, max_away_games, teams, distance_matrix)
    
    print("Shortest Tour:", " -> ".join(teams[team] for team in shortest_tour))
    print("Minimum Total Distance:", min_distance)

if __name__ == '__main__':
    main()
