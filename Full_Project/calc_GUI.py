import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, Toplevel
import calculus

class CalculusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculus Calculator")
        self.root.geometry("400x700")

        self.label = tk.Label(root, text="Select a Calculus Operation", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.diff_button = tk.Button(root, text="Differentiate", command=self.diff)
        self.diff_button.pack(pady=5)

        self.int_ind_button = tk.Button(root, text="Integration (IND)", command=self.int_ind)
        self.int_ind_button.pack(pady=5)

        self.int_def_button = tk.Button(root, text="Integration (DEF)", command=self.int_def)
        self.int_def_button.pack(pady=5)

        self.min_max_button = tk.Button(root, text="Min and Max", command=self.min_max)
        self.min_max_button.pack(pady=5)

        self.POI_button = tk.Button(root, text="Point of Inflection", command=self.POI)
        self.POI_button.pack(pady=5)

        self.cross_button = tk.Button(root, text="Cross Product", command=self.cross)
        self.cross_button.pack(pady=5)

        self.dot_button = tk.Button(root, text="Dot Product", command=self.dot)
        self.dot_button.pack(pady=5)


        

        self.help_button = tk.Button(root, text="Help/Instructions", command=self.show_help)
        self.help_button.pack(pady=5)

        self.back_button = tk.Button(root, text="Back to Main", command=self.root.destroy)
        self.back_button.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(root, height=8, width=40)
        self.output_area.pack(pady=10)


    
    def diff(self):
        equation = self.get_user_input("Enter an equation using x:")
        if equation:
            result = calculus.deriv(equation)
            self.display_result(result)

    def int_ind(self):
        equation = self.get_user_input("Enter an equation using x:")
        if equation:
            result = calculus.integration(equation)
            self.display_result(result)

    def int_def(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter an equation using x:").pack(pady=5)
        self.equation_entry = tk.Entry(self.popup)
        self.equation_entry.pack(pady=5)
        
        tk.Label(self.popup, text="Lower Limit:").pack(pady=5)
        self.lower_entry = tk.Entry(self.popup)
        self.lower_entry.pack(pady=5)
        
        tk.Label(self.popup, text="Upper Limit:").pack(pady=5)
        self.upper_entry = tk.Entry(self.popup)
        self.upper_entry.pack(pady=5)
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_def)
        submit_button.pack(pady=10)

    def min_max(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter an equation using x:").pack(pady=5)
        self.equation_entry = tk.Entry(self.popup)
        self.equation_entry.pack(pady=5)
        
        tk.Label(self.popup, text="Lower Limit:").pack(pady=5)
        self.lower_entry = tk.Entry(self.popup)
        self.lower_entry.pack(pady=5)
        
        tk.Label(self.popup, text="Upper Limit:").pack(pady=5)
        self.upper_entry = tk.Entry(self.popup)
        self.upper_entry.pack(pady=5)
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_mm)
        submit_button.pack(pady=10)

    def POI(self):
        equation = self.get_user_input("Enter an equation using x:")
        if equation:
            result = calculus.solve_poi(equation)
            self.display_result(result)

    def cross(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter First Vector:").pack(pady=5)
        self.first_vec = tk.Entry(self.popup)
        self.first_vec.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Second Vector:").pack(pady=5)
        self.second_vec = tk.Entry(self.popup)
        self.second_vec.pack(pady=5)
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_cross)
        submit_button.pack(pady=10)

    def dot(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter First Vector:").pack(pady=5)
        self.first_vec = tk.Entry(self.popup)
        self.first_vec.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Second Vector:").pack(pady=5)
        self.second_vec = tk.Entry(self.popup)
        self.second_vec.pack(pady=5)
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit_dot)
        submit_button.pack(pady=10)
            
    

    def get_user_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def display_result(self, result):
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, result)

    def show_help(self):
        help_text = (
            "Welcome to the Calculus Calculator!\n"
            "Instructions:\n\n"
            "- Input required values as instructed\n"
            "- Many functions only compute across a given range (Min_Max, Integration, etc)\n"
            "- For vector operations, separate values with +/- and use i, j, and k for variables (Ex: 2i+3j-2k)\n\n"
            "Results will appear in the output box below."
        )
        messagebox.showinfo("Help", help_text)

    def submit_def(self):
        # Retrieve inputs from the entry fields
        equation = self.equation_entry.get()
        lower_limit = self.lower_entry.get()
        upper_limit = self.upper_entry.get()
        result = calculus.def_integration(lower_limit, upper_limit, equation, n=1000)
        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()

    
    def submit_mm(self):
        # Retrieve inputs from the entry fields
        equation = self.equation_entry.get()
        lower_limit = self.lower_entry.get()
        upper_limit = self.upper_entry.get()
        min, max = calculus.min_max(equation, lower_limit, upper_limit)
        result = (('min: ' + str(min)), ('max: ' + str(max)))
        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()

    def submit_cross(self):
        # Retrieve inputs from the entry fields
        first_vec = self.first_vec.get()
        second_vec = self.second_vec.get()
        result = calculus.solve_cross(first_vec, second_vec)
        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()

    def submit_dot(self):
        # Retrieve inputs from the entry fields
        first_vec = self.first_vec.get()
        second_vec = self.second_vec.get()
        result = calculus.solve_dot(first_vec, second_vec)
        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()



        