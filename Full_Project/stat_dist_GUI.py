import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, Toplevel
import stat_dist

class StatDistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stat Distribution Calculator")
        self.root.geometry("400x700")

        self.operation = None

        self.label = tk.Label(root, text="Select a Stat Distribution", font=("Helvetica", 14))
        self.label.pack(pady=10)





        
        self.binomial_button = tk.Button(root, text="Binomial Distribution", command=self.binomial)
        self.binomial_button.pack(pady=5)

        self.geometric_button = tk.Button(root, text="Geometric Distribution", command=self.geometric)
        self.geometric_button.pack(pady=5)

        self.hypergeo_button = tk.Button(root, text="Hypergeometric Distribution", command=self.hypergeometric)
        self.hypergeo_button.pack(pady=5)

        self.poisson_button = tk.Button(root, text="Poisson Distribution", command=self.poisson)
        self.poisson_button.pack(pady=5)

        self.normalCDF_button = tk.Button(root, text="Normal Distribution (CDF)", command=self.CDF)
        self.normalCDF_button.pack(pady=5)

        self.normalPDF_button = tk.Button(root, text="Normal Distribution (PDF)", command=self.PDF)
        self.normalPDF_button.pack(pady=5)

        self.uni_dis_button = tk.Button(root, text="Discrete Uniform Distribution", command=self.discrete)
        self.uni_dis_button.pack(pady=5)

        self.uni_con_button = tk.Button(root, text="Continuous Uniform Distribution", command=self.continuous)
        self.uni_con_button.pack(pady=5)







        
        self.help_button = tk.Button(root, text="Help/Instructions", command=self.show_help)
        self.help_button.pack(pady=5)

        self.back_button = tk.Button(root, text="Back to Main", command=self.root.destroy)
        self.back_button.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(root, height=8, width=40)
        self.output_area.pack(pady=10)






    
    def binomial(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter Number of Trials:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Probability of Success:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        tk.Label(self.popup, text="Enter Number of Successes:").pack(pady=5)
        self.third = tk.Entry(self.popup)
        self.third.pack(pady=5)

        self.operation = 0
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)

    
    def geometric(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Enter Probability of Success:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)

        tk.Label(self.popup, text="Enter Success on Trial Number:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        self.operation = 1
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)


        
    def hypergeometric(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("400x400")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter Elements in Population:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Number of Elements Selected:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        tk.Label(self.popup, text="Enter Number of Successes in Population:").pack(pady=5)
        self.third = tk.Entry(self.popup)
        self.third.pack(pady=5)

        tk.Label(self.popup, text="Enter Number of Desired Successes:").pack(pady=5)
        self.fourth = tk.Entry(self.popup)
        self.fourth.pack(pady=5)
        
        self.operation = 2
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)


    def poisson(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields      
        tk.Label(self.popup, text="Enter Average/Lambda:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)

        tk.Label(self.popup, text="Enter Desired Observation:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        self.operation = 3
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)


    def CDF(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter Value of x:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Mean:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        tk.Label(self.popup, text="Enter Standard Deviation:").pack(pady=5)
        self.third = tk.Entry(self.popup)
        self.third.pack(pady=5)

        self.operation = 4
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)


    def PDF(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x300")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter Value of x:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Mean:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        tk.Label(self.popup, text="Enter Standard Deviation:").pack(pady=5)
        self.third = tk.Entry(self.popup)
        self.third.pack(pady=5)

        self.operation = 5
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)


    def discrete(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x500")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter Lower Range:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Upper Range:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        tk.Label(self.popup, text="Enter Beginning of Search Range:").pack(pady=5)
        self.third = tk.Entry(self.popup)
        self.third.pack(pady=5)

        tk.Label(self.popup, text="Enter End of Search Range:").pack(pady=5)
        self.fourth = tk.Entry(self.popup)
        self.fourth.pack(pady=5)

        tk.Label(self.popup, text="Enter Increment Value:").pack(pady=5)
        self.fifth = tk.Entry(self.popup)
        self.fifth.pack(pady=5)
        
        self.operation = 6
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)



    def continuous(self):
        # Create a new pop-up window
        self.popup = Toplevel(self.root)
        self.popup.title("Input Values")
        self.popup.geometry("300x400")
        
        # Create and pack labels and entry fields
        tk.Label(self.popup, text="Enter Lower Range:").pack(pady=5)
        self.first = tk.Entry(self.popup)
        self.first.pack(pady=5)
        
        tk.Label(self.popup, text="Enter Upper Range:").pack(pady=5)
        self.second = tk.Entry(self.popup)
        self.second.pack(pady=5)

        tk.Label(self.popup, text="Enter Beginning of Search Range:").pack(pady=5)
        self.third = tk.Entry(self.popup)
        self.third.pack(pady=5)

        tk.Label(self.popup, text="Enter End of Search Range:").pack(pady=5)
        self.fourth = tk.Entry(self.popup)
        self.fourth.pack(pady=5)
        
        self.operation = 7
        
        # Create and pack the submit button
        submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
        submit_button.pack(pady=10)

        

    
    def submit(self):
        # Retrieve inputs from the entry fields
        first = self.first.get()
        second = self.second.get()
        print(self.operation)
        if self.operation == 0:
            third = self.third.get()
            result = stat_dist.solve_binomial(first, second, third)
        elif self.operation == 1:
            result = stat_dist.solve_geometric(first, second)
        elif self.operation == 2:
            third = self.third.get()
            fourth = self.fourth.get()
            result = stat_dist.solve_hypergeometric(first, second, third, fourth)
        elif self.operation == 3:
            result = stat_dist.solve_poisson(first, second)
        elif self.operation == 4:
            third = self.third.get()
            result = stat_dist.solve_CDF(first, second, third)
        elif self.operation == 5: 
            third = self.third.get()
            result = stat_dist.solve_PDF(first, second, third)
        elif self.operation == 6:
            third = self.third.get()
            fourth = self.fourth.get()
            fifth = self.fifth.get()
            result = stat_dist.solve_discrete(first, second, third, fourth, fifth)
        elif self.operation == 7:
            third = self.third.get()
            fourth = self.fourth.get()
            result = stat_dist.solve_continuous(first, second, third, fourth)
        else:
            pass
        self.display_result(result)
        # Close the pop-up window
        self.popup.destroy()






    
    def get_user_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def display_result(self, result):
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, result)

    def show_help(self):
        help_text = (
            "Welcome to the Statistic Distribution Calculator!\n"
            "Each Function Asks for Required Inputs:\n\n"
            "- All probability inputs: 0 <= x <= 1\n"
            "- Binomial, Geometric, and Hypergeometric distributions must be integer values\n\n"
            "Results will appear in the output box below."
        )
        messagebox.showinfo("Help", help_text)

        