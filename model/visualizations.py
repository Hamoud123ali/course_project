import matplotlib.pyplot as plt
import numpy as np

def visualize_matrix(matrix, coverage_rows=None):
    """
    Visualize the matrix with coverage rows highlighted.
    """
    # Create a figure and a subplot
    fig, ax = plt.subplots()

    # Using matshow to create a heatmap representation of the matrix
    cax = ax.matshow(matrix, cmap='gray_r')  # _r in 'gray_r' indicates reversed grayscale (optional)

    # Highlight the coverage rows if provided
    if coverage_rows is not None:
        for row in coverage_rows:
            ax.add_patch(plt.Rectangle((0, row), len(matrix[0]), 1, fill=False, edgecolor='blue', lw=2))

    fig.colorbar(cax)  # Adding a colorbar for reference
    plt.show()


def compare_algorithms_performance(performance_metrics):
    """
    Compare algorithm performances with a bar chart.
    """
    # Assuming performance_metrics is a dictionary like 
    # {'Algorithm1': metric1, 'Algorithm2': metric2, ...}
    labels = list(performance_metrics.keys())
    values = list(performance_metrics.values())

    fig, ax = plt.subplots()

    # Creating a bar chart
    ax.bar(labels, values, color='skyblue')

    ax.set_ylabel('Performance metric (e.g., time)')
    ax.set_title('Performance comparison of different algorithms')
    plt.xticks(rotation=45)  # Rotating axis labels for better spacing

    plt.tight_layout()  # Ensuring everything fits into the figure
    plt.show()