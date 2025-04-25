import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from algebra import Algebra

class AlgebraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algebra Calculator")
        self.root.geometry("400x400")
        self.alg = Algebra()

        self.label = tk.Label(root, text="Select an Algebra Operation", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.linear_button = tk.Button(root, text="Solve Linear Equation", command=self.linear_equation)
        self.linear_button.pack(pady=5)

        self.vertex_button = tk.Button(root, text="Find Vertex", command=self.find_vertex)
        self.vertex_button.pack(pady=5)

        self.inequality_button = tk.Button(root, text="Solve Inequality", command=self.solve_inequality)
        self.inequality_button.pack(pady=5)

        self.help_button = tk.Button(root, text="Help/Instructions", command=self.show_help)
        self.help_button.pack(pady=5)

        self.back_button = tk.Button(root, text="Back to Main", command=self.root.destroy)
        self.back_button.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(root, height=8, width=40)
        self.output_area.pack(pady=10)

    def linear_equation(self):
        equation = self.get_user_input("Enter a linear equation (ax + b = 0):")
        if equation:
            result = self.alg.solve_linear_system(equation)
            self.display_result(result)

    def find_vertex(self):
        equation = self.get_user_input("Enter a quadratic equation (ax^2 + bx + c):")
        if equation:
            result = self.alg.find_vertex(equation)
            self.display_result(result)

    def solve_inequality(self):
        inequality = self.get_user_input("Enter an inequality (e.g., ax + b > 0):")
        if inequality:
            result = self.alg.solve_inequality(inequality)
            self.display_result(result)

    def get_user_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def display_result(self, result):
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, result)

    def show_help(self):
        help_text = (
            "Welcome to the Algebra Calculator!\n"
            "Here’s how to use each function:\n\n"
            "- Solve Linear Equation: Enter an equation like ax + b = 0\n"
            "- Find Vertex: Enter a quadratic equation like ax^2 + bx + c\n"
            "- Solve Inequality: Enter an inequality like ax + b > 0\n\n"
            "Results will appear in the output box below."
        )
        messagebox.showinfo("Help", help_text)