import tkinter as tk
from tkinter import messagebox
import random  # Needed for random matrix generation
from model import visualize_matrix, compare_algorithms_performance  # Importing the functions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MatrixView:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Row Coverage")
        
        padding = {'padx': 5, 'pady': 5}
        
        # Frame for algorithm selection with a label above the listbox
        algorithm_frame = tk.LabelFrame(self.root, text="Algorithms", padx=10, pady=10)
        algorithm_frame.pack(fill='x', **padding)

        # Multi-select Listbox for algorithm selection
        self.algorithm_options = ["Branch and Bound", "Greedy", "Genetic Algorithm", "Linear Programming"]
        self.algorithm_listbox = tk.Listbox(algorithm_frame, selectmode=tk.MULTIPLE, height=4)
        for algorithm in self.algorithm_options:
            self.algorithm_listbox.insert(tk.END, algorithm)
        self.algorithm_listbox.pack(fill='x', expand=True)

        # Inputs for random matrix generation
        matrix_frame = tk.Frame(self.root)
        matrix_frame.pack(fill='x', **padding)
        
        tk.Label( matrix_frame,text="Rows:").grid(row=0, column=0, sticky='w') # Label for rows input
        self.rows_input = tk.Entry(matrix_frame)  # Input for number of rows
        self.rows_input.grid(row=0, column=1, sticky='ew')

        tk.Label(matrix_frame, text="Columns:").grid(row=1, column=0, sticky='w') # Label for columns input
        self.columns_input = tk.Entry(matrix_frame)  # Input for number of columns
        self.columns_input.grid(row=1, column=1, sticky='ew')

        matrix_frame.grid_columnconfigure(1, weight=1)  
        # Button to generate a random matrix
        self.generate_button = tk.Button(matrix_frame, text="Generate Random Matrix", command=self.generate_random_matrix)
        self.generate_button.grid(row=2, column=0, columnspan=2, sticky='ew', **padding)
        
        
        matrix_input_frame = tk.Frame(self.root)
        matrix_input_frame.pack(fill='both', expand=True, **padding)
        # Text area for matrix input with a scrollbar
        self.matrix_input = tk.Text(matrix_input_frame, height=10)
        self.matrix_input.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(matrix_input_frame, command=self.matrix_input.yview)
        scrollbar.pack(side='right', fill='y')
        self.matrix_input['yscrollcommand'] = scrollbar.set

        action_button_frame = tk.Frame(self.root)
        action_button_frame.pack(fill='x', **padding)
        # Button to trigger calculation
        self.submit_button = tk.Button(action_button_frame, text="Calculate Coverage", command=None)  # The command is set by the controller.
        self.submit_button.pack(side='left', expand=True, **padding)

        self.visualize_button = tk.Button(action_button_frame, text="Visualize Matrix", command=self.on_visualize)
        self.visualize_button.pack(side='left', expand=True, **padding)
         # Add a button to trigger the performance comparison
        self.compare_performance_button = tk.Button(action_button_frame, text="Compare Performance" )
        self.compare_performance_button.pack(side='left', expand=True, **padding) # or grid() depending on your layout
        
        
       

        

    def generate_random_matrix(self):
        """
        Generates a random matrix based on the input dimensions and range.
        """
        try:
            rows = int(self.rows_input.get())
            cols = int(self.columns_input.get())
         

            if rows <= 0 or cols <= 0:
                raise ValueError("Number of rows and columns must be positive integers.")
  
            # Generate the random matrix
            matrix = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

            # Convert the matrix to a string format and set it in the matrix_input text field
            matrix_str = '\n'.join([' '.join(map(str, row)) for row in matrix])
            self.matrix_input.delete("1.0", tk.END)  # Clear the current content
            self.matrix_input.insert("1.0", matrix_str)  # Insert the new random matrix

        except ValueError as e:
            # Handle cases where input values are invalid.
            messagebox.showerror("Error", str(e))


    def get_matrix_input(self):
        """
        Retrieves and processes the matrix input from the GUI.
        """
        try:
            # Get input from Text widget and convert to 2D list (matrix).
            matrix_str = self.matrix_input.get("1.0", tk.END).strip()
            matrix = [list(map(int, row.split())) for row in matrix_str.split('\n') if row]
            return matrix
        except ValueError:
            # Handle cases where input cannot be converted to integer.
            messagebox.showerror("Error", "Matrix must only contain integers.")
            return None

    def get_selected_algorithms(self):
        """
        Retrieves the selected algorithms from the listbox.
        """
        return [self.algorithm_options[index] for index in self.algorithm_listbox.curselection()]

    def show_result(self, message):
        """
        Displays the result message to the user.
        """
        messagebox.showinfo("Result", message)

    def show_error(self, message):
        """
        Displays an error message to the user.
        """
        messagebox.showerror("Error", message)

    def on_visualize(self, matrix, coverage_rows):
        """
        Trigger the visualization for the current matrix and its coverage rows.

        :param matrix: The matrix data to visualize.
        :param coverage_rows: The rows in the matrix that are part of the coverage.
        """
        visualize_matrix(matrix, coverage_rows)  # Call the visualization function with the provided data
    # You might also have a function to trigger the performance comparison visualization
  

    def display_performance_plot(self, names, values):
        # Create a new top-level window for the plot
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Performance Comparison")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(names, values, color=['red', 'green', 'blue', 'cyan'])
        ax.set_ylabel('Execution Time (s)')
        ax.set_xlabel('Algorithms')
        ax.set_title('Performance Comparison')

        canvas = FigureCanvasTkAgg(fig, master=plot_window)  # Creating the canvas to embed the plot in the tkinter window
        canvas.draw()
        canvas.get_tk_widget().pack()