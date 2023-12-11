import tkinter as tk
from model.model import MatrixModel
from utils.algorithms import branch_and_bound, greedy_algorithm, genetic_algorithm, linear_programming
from view.view import MatrixView
import matplotlib.pyplot as plt
import time
class MatrixController:
    def __init__(self, root):
        self.model = MatrixModel()
        self.view = MatrixView(root)
        self.view.submit_button['command'] = self.main_logic 
        self.view.visualize_button.config(command=self.handle_visualize)

        self.view.compare_performance_button['command'] = self.handle_compare_performance


    def main_logic(self):
        try:
            matrix = self.view.get_matrix_input()
            if matrix is None:
                return

            self.model.set_matrix(matrix)
            selected_algorithms = self.view.get_selected_algorithms()

            # Run each selected algorithm and collect results
            all_results = []
            for algorithm in selected_algorithms:
                self.model.run_algorithm(algorithm)
                coverage_rows = self.model.get_coverage_rows(algorithm)
                result_message = f"{algorithm}: Minimum rows for full coverage: " + ", ".join(str(row + 1) for row in coverage_rows)
                all_results.append(result_message)

            # Show a consolidated result.
            final_message = '\n'.join(all_results)
            self.view.show_result(final_message)

        except Exception as e:
            self.view.show_error(str(e))

    def determine_coverage(self, matrix, algorithm):
        start_time = time.time()

        if algorithm == "Branch and Bound":
            result = branch_and_bound(matrix)
        elif algorithm == "Greedy":
            result = greedy_algorithm(matrix)
        elif algorithm == "Genetic Algorithm":
            result = genetic_algorithm(matrix)
        elif algorithm == "Linear Programming":
            result = linear_programming(matrix)
        else:
            raise ValueError(f"Unknown algorithm selected: {algorithm}")

        end_time = time.time()
        execution_time = end_time - start_time

        # Record the execution time in the model
        self.model.set_execution_time(algorithm, execution_time)

        return result

    def handle_visualize(self):
        matrix = self.model.get_matrix()
        # NOTE: This would visualize the result of the last algorithm in the list.
        # You might want to change this behavior.
        last_algorithm = self.view.get_selected_algorithms()[-1] if self.view.get_selected_algorithms() else None
        coverage_rows = self.model.get_coverage_rows(last_algorithm) if last_algorithm else None
        if coverage_rows:
            self.view.on_visualize(matrix, coverage_rows)

    def handle_compare_performance(self):
        selected_algorithms = self.view.get_selected_algorithms()

        if len(selected_algorithms) != 2:
            self.view.show_error("Please select exactly two algorithms for comparison.")
            return

        algorithm1, algorithm2 = selected_algorithms

        performance_metrics = {
        algorithm1: self.model.get_execution_time(algorithm1),
        algorithm2: self.model.get_execution_time(algorithm2)
        }

        # Check for None values and handle them
        for algorithm, time in performance_metrics.items():
            if time is None:
                self.view.show_error(f"Execution time for {algorithm} is not available.")
                return

        names = list(performance_metrics.keys())
        values = list(performance_metrics.values())

        # Call the view method to display the plot
        self.view.display_performance_plot(names, values)



if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixController(root)
    root.mainloop()
