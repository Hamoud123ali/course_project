import time
from utils.algorithms import branch_and_bound, greedy_algorithm, genetic_algorithm, linear_programming

class MatrixModel:
    def __init__(self):
        self.matrix = []  # Stores the matrix data.
        self.coverage_rows = {}  # Stores the rows that cover all columns, indexed by algorithm.
        self.execution_times = {}  # Stores the execution times, indexed by algorithm.

    def set_matrix(self, matrix):
        """
        Set or update the matrix data.

        :param matrix: List of lists with matrix data.
        """
        if self.validate_matrix(matrix):
            self.matrix = matrix
        else:
            raise ValueError("Invalid matrix data")

    def get_matrix(self):
        """
        Retrieve the stored matrix data.

        :return: List of lists with matrix data.
        """
        return self.matrix

    def set_coverage_rows(self, algorithm, rows):
        """
        Set or update the coverage rows data based on the algorithm used.

        :param algorithm: A string representing the algorithm used.
        :param rows: List of row indices.
        """
        self.coverage_rows[algorithm] = rows

    def get_coverage_rows(self, algorithm):
        """
        Retrieve the stored coverage rows data for a specific algorithm.

        :param algorithm: A string representing the algorithm used.
        :return: List of row indices.
        """
        return self.coverage_rows.get(algorithm, [])

    def set_execution_time(self, algorithm, execution_time):
        """
        Record the execution time of an algorithm.

        :param algorithm: A string representing the algorithm used.
        :param execution_time: The execution time of the algorithm.
        """
        self.execution_times[algorithm] = execution_time

    def get_execution_time(self, algorithm):
        """
        Retrieve the stored execution time for a specific algorithm.

        :param algorithm: A string representing the algorithm used.
        :return: Execution time.
        """
        return self.execution_times.get(algorithm)

    def run_algorithm(self, algorithm):
        """
        Execute the specified algorithm and record its results.

        :param algorithm: A string representing the algorithm to be used.
        """
        # Dictionary linking algorithm names to their corresponding functions
        algorithm_functions = {
            'Branch and Bound': branch_and_bound,
            'Greedy': greedy_algorithm,
            'Genetic Algorithm': genetic_algorithm,
            'Linear Programming': linear_programming
        }

        if algorithm not in algorithm_functions:
            raise ValueError("Unknown algorithm selected")

        algorithm_function = algorithm_functions[algorithm]

        start_time = time.time()
        result_rows = algorithm_function(self.matrix)  # Running the chosen algorithm
        end_time = time.time()

        self.set_coverage_rows(algorithm, result_rows)
        self.set_execution_time(algorithm, end_time - start_time)

    def validate_matrix(self, matrix):
        """
        Validates the provided matrix.

        :param matrix: List of lists representing the matrix.
        :return: Boolean indicating whether the matrix is valid.
        """
        # Check if matrix is not empty and if each row is a list
        if not matrix or not all(isinstance(row, list) for row in matrix):
            return False

        row_length = len(matrix[0])
        for row in matrix:
            # All rows must be of the same length
            if len(row) != row_length:
                return False

            # Each element must be an integer (for this context)
            if not all(isinstance(item, int) for item in row):
                return False

        return True

    # ... Any additional methods or logic required for the model should be implemented here.

# The rest of your model.py file...
