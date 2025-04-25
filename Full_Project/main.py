import tkinter as tk
from tkinter import messagebox, Toplevel
from alg_GUI import AlgebraGUI
from calc_GUI import CalculusGUI
from stat_GUI import StatisticsGUI
from stat_dist_GUI import StatDistGUI
from matrix_GUI import MatrixGUI
import calculator

# Advanced calculator navigation functions:

# Function to open algebra calculator
def open_algebra_calculator():
    new_window = Toplevel(root)  
    AlgebraGUI(new_window)  

# Function to open calculus calculator
def open_calculus_calculator():
    new_window = Toplevel(root)  
    CalculusGUI(new_window)  
    
# Function to open statistics calculator
def open_statistics_calculator():
    new_window = Toplevel(root)  
    StatisticsGUI(new_window)  

# Function to open stat distribution calculator
def open_stat_dist_calculator():
    new_window = Toplevel(root)  
    StatDistGUI(new_window) 

# Function to open matrix calculator
def open_matrix_calculator():
    new_window = Toplevel(root)  
    MatrixGUI(new_window) 




# Function to evaluate expressions
def calculate():
    try:
        expression = entry.get()
        ans = calculator.compute(expression)
        result.set(str(ans))  # Evaluates the expression entered
    except Exception as e:
        result.set("Error")



# Function to display help information
def show_help():
    help_text = """How to use the Calculator:
1. Enter a mathematical expression in the text box.
2. Click 'Calculate' to evaluate it.
3. Use the advanced calculator buttons to perform specific calculations.
4. Click 'Help' for additional guidance."""
    messagebox.showinfo("Help", help_text)


# Initialize main window
root = tk.Tk()
root.title("Calculator")
root.geometry("500x500")

# Title Label
title_label = tk.Label(root, text="Calculator", font=("Arial", 18))
title_label.pack(pady=10)

# Input field
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Calculate button & output display
result = tk.StringVar()
result_label = tk.Label(root, textvariable=result, font=("Arial", 12))
calculate_button = tk.Button(root, text="Calculate", command=calculate)

calculate_button.pack(pady=5)
result_label.pack(pady=5)



# Advanced calculator buttons
calculus = tk.Button(root, text="Calculus", command=open_calculus_calculator)
calculus.pack(pady=2)

algebra = tk.Button(root, text="Algebra", command = open_algebra_calculator)
algebra.pack(pady=2)

statistics = tk.Button(root, text="Statistics", command = open_statistics_calculator)
statistics.pack(pady=2)

stat_dist = tk.Button(root, text="Stat Distribution", command = open_stat_dist_calculator)
stat_dist.pack(pady=2)

matrix = tk.Button(root, text="Matrix Operations", command = open_matrix_calculator)
matrix.pack(pady=2)



# Help button
help_button = tk.Button(root, text="Help", command=show_help)
help_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
