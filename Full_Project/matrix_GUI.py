import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, Toplevel
import matrix

class MatrixGUI:
    def __init__(self, root):
        self.operation = None
        self.root = root
        self.root.title("Matrix Calculator")
        self.root.geometry("400x500")

        self.label = tk.Label(root, text="Select a Matrix Operation", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="Matrix Addition", command=self.add)
        self.add_button.pack(pady=5)

        self.sub_button = tk.Button(root, text="Matrix Substraction", command=self.subtract)
        self.sub_button.pack(pady=5)

        self.mult_button = tk.Button(root, text="Matrix Multiplication", command=self.multiply)
        self.mult_button.pack(pady=5)

        self.inverse_button = tk.Button(root, text="Matrix Inverse", command=self.inverse)
        self.inverse_button.pack(pady=5)
                
        self.eigen_button = tk.Button(root, text="Matrix Eigen Profile", command=self.eigen)
        self.eigen_button.pack(pady=5)

        self.help_button = tk.Button(root, text="Help/Instructions", command=self.show_help)
        self.help_button.pack(pady=5)

        self.back_button = tk.Button(root, text="Back to Main", command=self.root.destroy)
        self.back_button.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(root, height=8, width=40)
        self.output_area.pack(pady=10)



    


    def submit_dimension(self):
        if self.operation == 0 or self.operation == 1:
            rows = int(self.rows.get())
            cols = int(self.cols.get())
            self.rows = rows
            self.cols = cols
        elif self.operation == 3 or self.operation == 4: 
            rows = int(self.dimension.get())
            cols = int(self.dimension.get())
            self.rows = rows
            self.cols = cols
            
        self.popup.destroy()

        
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        tk.Label(self.popup, text=f"Enter first {rows}x{cols} Matrix", font=("Arial", 12)).pack(pady=5)
    
        # Create grid of Entry widgets
        self.matrix_one = []
        
        # Create a frame inside the popup window to use grid layout
        matrix_frame = tk.Frame(self.popup)
        matrix_frame.pack(pady=10)  # Use pack for the frame itself
        
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = tk.Entry(matrix_frame, width=5, justify="center")  # Use matrix_frame as the parent
                entry.grid(row=i, column=j, padx=5, pady=5)  # Use grid within the frame
                row_entries.append(entry)
            self.matrix_one.append(row_entries)

        
        # Create and pack the submit button
        if self.operation == 0 or self.operation == 1:
            submit_button = tk.Button(self.popup, text="Submit", command=self.submit_first)
            submit_button.pack(pady=10)
        else:
            submit_button = tk.Button(self.popup, text="Submit", command=self.submit_second)
            submit_button.pack(pady=10)
            


    def submit_first(self):

        # Retrieve input values from the Entry widgets
        self.first = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                value = self.matrix_one[i][j].get()
                try:
                    row.append(float(value))  
                except ValueError:
                    row.append(value)  
            self.first.append(row)
        
        rows = int(self.rows)
        cols = int(self.cols)
        self.popup.destroy()
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        tk.Label(self.popup, text=f"Enter second {rows}x{cols} Matrix", font=("Arial", 12)).pack(pady=5)
    
        # Create grid of Entry widgets
        self.matrix_two = []
        
        # Create a frame inside the popup window to use grid layout
        matrix_frame = tk.Frame(self.popup)
        matrix_frame.pack(pady=10)  # Use pack for the frame itself
        
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = tk.Entry(matrix_frame, width=5, justify="center")  # Use matrix_frame as the parent
                entry.grid(row=i, column=j, padx=5, pady=5)  # Use grid within the frame
                row_entries.append(entry)
            self.matrix_two.append(row_entries)

        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_second)
        submit_button.pack(pady=10)


    
    def submit_second(self):
        # Retrieve input values from the Entry widgets
        self.second = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.operation == 0 or self.operation == 1:
                    value = self.matrix_two[i][j].get()
                else:
                    value = self.matrix_one[i][j].get()
                try:
                    row.append(float(value))  
                except ValueError:
                    row.append(value)  
            self.second.append(row)
        if self.operation == 0:
            result = matrix.solve_addition(self.first, self.second)
        if self.operation == 1:
            result = matrix.solve_subtraction(self.first, self.second)
        if self.operation == 3:
            result = matrix.solve_inverse(self.second)
        if self.operation == 4:
            result = matrix.solve_eigen(self.second)

        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()
    


    def get_second_dimension(self):
        rows = int(self.rows.get())
        cols = int(self.cols.get())
        self.first_rows = rows
        self.first_cols = cols
        self.second_rows = cols
        self.popup.destroy()
        
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension of Second Matrix:")
        self.popup.geometry("300x300")

        tk.Label(self.popup, text="Columns:").pack(pady=5)
        self.cols = tk.Entry(self.popup)
        self.cols.pack(pady=5)

        self.operation = 1
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_dimension_mult)
        submit_button.pack(pady=10)

    
    def submit_dimension_mult(self):
        cols = int(self.cols.get())
        self.second_cols = cols
        self.popup.destroy()
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        tk.Label(self.popup, text=f"Enter first {self.first_rows}x{self.first_cols} Matrix", font=("Arial", 12)).pack(pady=5)
    
        # Create grid of Entry widgets
        self.matrix_one = []
        
        # Create a frame inside the popup window to use grid layout
        matrix_frame = tk.Frame(self.popup)
        matrix_frame.pack(pady=10)  # Use pack for the frame itself
        
        for i in range(self.first_rows):
            row_entries = []
            for j in range(self.first_cols):
                entry = tk.Entry(matrix_frame, width=5, justify="center")  # Use matrix_frame as the parent
                entry.grid(row=i, column=j, padx=5, pady=5)  # Use grid within the frame
                row_entries.append(entry)
            self.matrix_one.append(row_entries)

        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_first_mult)
        submit_button.pack(pady=10)



    def submit_first_mult(self):

        # Retrieve input values from the Entry widgets
        self.first = []
        for i in range(self.first_rows):
            row = []
            for j in range(self.first_cols):
                value = self.matrix_one[i][j].get()
                try:
                    row.append(float(value))  
                except ValueError:
                    row.append(value)  
            self.first.append(row)
        
        rows = int(self.second_rows)
        cols = int(self.second_cols)
        self.popup.destroy()
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        tk.Label(self.popup, text=f"Enter second {self.second_rows}x{self.second_cols} Matrix", font=("Arial", 12)).pack(pady=5)
    
        # Create grid of Entry widgets
        self.matrix_two = []
        
        # Create a frame inside the popup window to use grid layout
        matrix_frame = tk.Frame(self.popup)
        matrix_frame.pack(pady=10)  # Use pack for the frame itself
        
        for i in range(self.second_rows):
            row_entries = []
            for j in range(self.second_cols):
                entry = tk.Entry(matrix_frame, width=5, justify="center")  # Use matrix_frame as the parent
                entry.grid(row=i, column=j, padx=5, pady=5)  # Use grid within the frame
                row_entries.append(entry)
            self.matrix_two.append(row_entries)

        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_second_mult)
        submit_button.pack(pady=10)


    def submit_second_mult(self):
        # Retrieve input values from the Entry widgets
        self.second = []
        for i in range(self.second_rows):
            row = []
            for j in range(self.second_cols):
                value = self.matrix_two[i][j].get()
                try:
                    row.append(float(value))  
                except ValueError:
                    row.append(value)  
            self.second.append(row)
        result = matrix.solve_multiplication(self.first, self.second)
            
        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()



    
    
    def add(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Rows:").pack(pady=5)
        self.rows = tk.Entry(self.popup)
        self.rows.pack(pady=5)

        tk.Label(self.popup, text="Columns:").pack(pady=5)
        self.cols = tk.Entry(self.popup)
        self.cols.pack(pady=5)

        self.operation = 0
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_dimension)
        submit_button.pack(pady=10)

    
    
    def subtract(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Rows:").pack(pady=5)
        self.rows = tk.Entry(self.popup)
        self.rows.pack(pady=5)

        tk.Label(self.popup, text="Columns:").pack(pady=5)
        self.cols = tk.Entry(self.popup)
        self.cols.pack(pady=5)

        self.operation = 1
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_dimension)
        submit_button.pack(pady=10)

        
    def multiply(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Rows:").pack(pady=5)
        self.rows = tk.Entry(self.popup)
        self.rows.pack(pady=5)

        tk.Label(self.popup, text="Columns:").pack(pady=5)
        self.cols = tk.Entry(self.popup)
        self.cols.pack(pady=5)

        self.operation = 2
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.get_second_dimension)
        submit_button.pack(pady=10)

    def inverse(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Input Square Dimension:").pack(pady=5)
        self.dimension = tk.Entry(self.popup)
        self.dimension.pack(pady=5)

        self.operation = 3
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_dimension)
        submit_button.pack(pady=10)

    def eigen(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Dimension")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Input Square Dimension:").pack(pady=5)
        self.dimension = tk.Entry(self.popup)
        self.dimension.pack(pady=5)

        self.operation = 4
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_dimension)
        submit_button.pack(pady=10)





    
    def get_user_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def display_result(self, result):
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, result)

    def show_help(self):
        help_text = (
            "Welcome to the Matrix Calculator!\n"
            "Instructions:\n\n"
            "- Input Matrix Dimensions\n"
            "- The matrix boxes are made according to the input dimensions\n"
            "- Fill in each box of the matrix as instructed, using only numerical values\n\n"
            "Results will appear in the output box below."
        )
        messagebox.showinfo("Help", help_text)