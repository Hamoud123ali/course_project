# utils/algorithms.py
import random
import pulp
import numpy as np


def covers_all_columns(matrix, rows, num_cols):
    """
    Check if the selected rows cover all columns.

    :param matrix: The original matrix.
    :param rows: Rows selected as a potential solution.
    :param num_cols: The total number of columns in the matrix.
    :return: True if all columns are covered, False otherwise.
    """
    covered = [False] * num_cols

    for row in rows:
        for col in range(num_cols):
            if matrix[row][col] == 1:  # or some condition to check coverage
                covered[col] = True

    return all(covered)


def branch_and_bound(matrix):
    """
    Solve the minimum row coverage problem using the Branch and Bound method.

    :param matrix: A 2D list of integers representing the matrix.
    :return: A list of row indices indicating the rows that form the minimum coverage.
    """
    if not matrix:
        return []

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Initial solutions (each row by itself)
    solutions = [[i] for i in range(num_rows)]

    # Placeholder for the final result
    final_rows = []

    while solutions:
        # Get a candidate solution
        candidate = solutions.pop(0)

        # Check if this combination covers all columns
        if covers_all_columns(matrix, candidate, num_cols):
            if not final_rows or len(candidate) < len(final_rows):
                final_rows = candidate
            continue  # We don't branch on full coverage sets

        # If we haven't covered all columns and the candidate has fewer rows than the best solution so far
        if not final_rows or len(candidate) < len(final_rows) - 1:
            # Branch: create new candidate solutions by adding each of the other rows
            for i in range(num_rows):
                if i not in candidate:
                    new_candidate = candidate + [i]
                    solutions.append(new_candidate)

    return final_rows


def greedy_algorithm(matrix):
    # Assuming 1s in the matrix indicate the presence of a required element
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    covered = set()
    selected_rows = []

    while len(covered) < num_cols:
        # Find the row that covers the most uncovered elements
        most_effective_row = None
        coverage = set()
        #For each row, it calculates how many uncovered columns it can cover.
        for i in range(num_rows):
            current_coverage = {j for j, cell in enumerate(matrix[i]) if cell == 1 and j not in covered}
            if len(current_coverage) > len(coverage):
                coverage = current_coverage
                most_effective_row = i

        # Update the sets of covered elements and selected rows
        covered |= coverage
        if most_effective_row is not None:  # Check in case of an empty row
            selected_rows.append(most_effective_row)

    return selected_rows


#make rondom list of true or false lengh if list is rows 
def initialize_population(population_size, num_rows):
    population = []
    for _ in range(population_size):
        individual = [random.choice([True, False]) for _ in range(num_rows)]
        population.append(individual)
    return population

def select_parents(scored_population, num_parents=2):
    # Simple roulette wheel selection
    total_fitness = sum(score for _, score in scored_population)  # sum of all scores
    selection_probs = [score / total_fitness for _, score in scored_population]

    parents = random.choices(scored_population, weights=selection_probs, k=num_parents)
    return [individual for individual, _ in parents]


def crossover(parents):
    # For simplicity, let's assume there are always two parents
    parent_a, parent_b = parents
    print(parent_a , parent_b)
    child = []

    for gene_a, gene_b in zip(parent_a, parent_b):
        child.append(random.choice([gene_a, gene_b]))

    return [child]  # Returns a list of one child; in reality, you might have more than one child


# flip the value of some silutions rondmly
def mutate(population, mutation_rate):
    # Randomly flip the 'gene' with a chance of 'mutation_rate'
    for individual in population:
        if random.random() < mutation_rate:
            mutate_at = random.randint(0, len(individual) - 1)
            individual[mutate_at] = not individual[mutate_at]  # Flip the value
    return population




# Fitness function
def fitness(individual, matrix):
    covered = set()
    for row_selected, row in zip(individual, matrix):
        if row_selected:
            covered.update(col_index for col_index, cell in enumerate(row) if cell)
    score = len(covered) - sum(individual)
    return score if len(covered) == len(matrix[0]) else -1

def genetic_algorithm(matrix):
    POPULATION_SIZE = 100
    GENERATIONS = 1000
    MUTATION_RATE = 0.01  # Adjust mutation rate if necessary

    population = initialize_population(POPULATION_SIZE, len(matrix))
    best_solution = None
    best_fitness = float('-inf')

    for _ in range(GENERATIONS):
        scored_population = [(individual, fitness(individual, matrix)) for individual in population]
        
        # Update the best solution if a new best is found
        for individual, score in scored_population:
            if score > best_fitness:
                best_solution = individual
                best_fitness = score

        # If a perfect solution is found, stop early
        if best_fitness == len(matrix[0]) - sum(best_solution):
            break
        
        parents = select_parents(scored_population)
        children = crossover(parents)
        population = mutate(children + population, MUTATION_RATE)  # Keep old population and new children
        
        # Keep the best solution in the population
        population = [best_solution] + sorted(population, key=lambda ind: fitness(ind, matrix), reverse=True)[:POPULATION_SIZE-1]

    if best_solution is not None:
        best_solution_indices = [i for i, selected in enumerate(best_solution) if selected]
    else:
        best_solution_indices = None

    return best_solution_indices





def linear_programming(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Create a Linear Program
    lp_problem = pulp.LpProblem("Minimize_Row_Coverage", pulp.LpMinimize)

    # Create decision variables
    row_vars = [pulp.LpVariable(f"row_{i}", cat='Binary') for i in range(num_rows)]

    # Objective function: Minimize the number of rows used
    lp_problem += pulp.lpSum(row_vars)

    # Constraints: Each column j must be covered by at least one row
    for j in range(num_cols):
        lp_problem += pulp.lpSum(row_vars[i] for i in range(num_rows) if matrix[i][j] == 1) >= 1

    # Solve the problem
    lp_problem.solve()

    # Extract the rows selected in the optimal solution
    selected_rows = [i for i, row_var in enumerate(row_vars) if row_var.value() == 1]
    return selected_rows




