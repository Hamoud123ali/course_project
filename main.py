import tkinter as tk
from controller.controller import MatrixController

def main():
    # Create the main application window.
    root = tk.Tk()

    # Set the title for the application window.
    root.title("Minimum Row Coverage of a Matrix")

    # Set the geometry (size) of the main window here. You can adjust as necessary.
    root.geometry("700x700")  # width x height

    # Create the controller, which in turn initializes the model and view.
    controller = MatrixController(root)

    # The controller handles interactions between the model and view. We don't need
    # to do anything else with it here. The application logic is now driven by user
    # interactions with the GUI.

    # Start the main event loop. This is where the application waits for user input
    # and responds to events (e.g., button clicks, text entry).
    root.mainloop()

# This conditional is used to check whether this script is being run as a script
# or being imported as a module. It prevents code from being run if it's imported.
if __name__ == "__main__":
    main()



# import tkinter as tk
# from tkinter import messagebox

# class MatrixCoverageApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Matrix Coverage Problem")

#         # Initialize matrix (this is your input)
#         self.matrix = [
#             [0, 1, 0, 0],
#             [1, 1, 1, 0],
#             [0, 0, 1, 1]
#         ]

#         # Creating a simple interface
#         tk.Label(root, text="Matrix Row Coverage", font=('Helvetica', 16)).pack(pady=10)

#         # Display matrix to the user (for reference)
#         matrix_text = "\n".join([" ".join(map(str, row)) for row in self.matrix])
#         tk.Label(root, text=matrix_text, font=('Courier', 14)).pack(pady=10)

#         # Button to run the process
#         tk.Button(root, text="Find Minimum Rows", command=self.find_minimum_rows).pack(pady=10)

#     def find_minimum_rows(self):
#         """
#         Simplified function to find minimum row coverage.
#         This is a very basic approach; for larger matrices, you'd want a more efficient algorithm.
#         """
#         if not self.matrix:
#             messagebox.showinfo("Result", "No matrix available.")
#             return

#         # Find the total coverage, assuming each item is represented at least once in the matrix
#         total_coverage = set(j for i in self.matrix for j, val in enumerate(i) if val)

#         # Simple algorithm to identify rows that, together, cover all items
#         used_rows = []
#         while total_coverage:
#             # Find the row with the most coverage
#             coverage_counts = [(i, sum(1 for j in range(len(row)) if j in total_coverage and row[j])) for i, row in enumerate(self.matrix)]
#             best_row = max(coverage_counts, key=lambda x: x[1])
#             if best_row[1] == 0:
#                 break  # No more coverage to be found

#             # Add this row to the used rows
#             used_rows.append(best_row[0])

#             # Remove the covered items from the total coverage
#             total_coverage -= set(j for j, val in enumerate(self.matrix[best_row[0]]) if val)

#         # Display the result
#         result_message = "Minimum rows for full coverage: " + ", ".join(str(row + 1) for row in used_rows)
#         messagebox.showinfo("Result", result_message)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MatrixCoverageApp(root)
#     root.mainloop()
