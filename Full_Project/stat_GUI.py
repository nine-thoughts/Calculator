import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statistics_operations import Statistics

class StatisticsGUI:
    def __init__(self, root):
        self.stats = Statistics()
        self.root = root
        self.root.title("Statistics Calculator")
        # self.root.iconbitmap('calculator.ico')  # Uncomment if 'calculator.ico' is available  # Uncomment this line only if the .ico file exists  # Add a .ico file in the same directory
        self.root.geometry("1100x850")

        # Apply modern styles
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=4)
        self.root.configure(bg="#f4f4f4")

        # Style dropdowns and keypad buttons
        style.configure("TCombobox", padding=4)
        style.configure("Keypad.TButton", font=("Segoe UI", 10), padding=6, relief="flat")

        self.df = None
        self.column_selector = None

        self.tab_control = ttk.Notebook(root)
        self.input_tab = ttk.Frame(self.tab_control)
        self.input_tab.configure(style='TFrame')
        # self.input_tab.configure(background="#f4f4f4")  # ttk.Frame does not support 'background'
        self.graph_tab = ttk.Frame(self.tab_control)
        self.graph_tab.configure(style='TFrame')
        # self.graph_tab.configure(background="#f4f4f4")  # ttk.Frame does not support 'background'

        self.tab_control.add(self.input_tab, text='Input & Result')
        self.tab_control.add(self.graph_tab, text='Graph')
        self.tab_control.pack(expand=1, fill='both')

        self.back_button = tk.Button(root, text="Back to Main", command=self.root.destroy)
        self.back_button.pack(pady=5)

        self.create_input_tab()
                # Add dark mode toggle
        self.dark_mode = tk.BooleanVar()
        toggle = ttk.Checkbutton(self.input_tab, text="🌙 Dark Mode", variable=self.dark_mode, command=self.toggle_theme)
        toggle.pack(pady=5)

        self.create_graph_tab()

    def create_input_tab(self):
        ttk.Label(self.input_tab, text="Select Statistical Method:").pack(pady=5)
        self.method_selector = ttk.Combobox(self.input_tab, values=[
            "Mean", "Median", "Mode", "Standard Deviation", "Variance",
            "Z-Score", "Expected Value", "Permutations", "Combinations", "Moments"
        ])
        self.method_selector.pack()

        ttk.Label(self.input_tab, text="Enter data (comma-separated):").pack(pady=5)
        self.input_entry = ttk.Entry(self.input_tab, width=60)
        self.input_entry.pack(pady=5)

        self.extra_label = ttk.Label(self.input_tab, text="Extra value (if needed, e.g. r for nCr):")
        self.extra_label.pack(pady=5)
        self.extra_entry = ttk.Entry(self.input_tab, width=20)
        self.extra_entry.pack(pady=5)

        ttk.Button(self.input_tab, text="Load CSV File", command=self.load_csv).pack(pady=5)
        self.column_selector = ttk.Combobox(self.input_tab, values=[], state='readonly')
        self.column_selector.pack(pady=5)
        self.column_selector.bind("<<ComboboxSelected>>", self.select_column)

        ttk.Button(self.input_tab, text="Calculate", command=self.calculate).pack(pady=10)

        self.output_label = ttk.Label(self.input_tab, text="", font=("Arial", 14), wraplength=1000, justify="left")
        self.output_label.pack(pady=10)

        # Virtual Math Keypad
        keypad_frame = ttk.Frame(self.input_tab)
        keypad_frame.pack(pady=10)
        symbols = ["μ", "σ", "σ²", "∑", "x̄", "n", "P", "C"]
        for symbol in symbols:
            btn = ttk.Button(keypad_frame, text=symbol, command=lambda s=symbol: self.insert_symbol(s))
            btn.configure(style="Keypad.TButton")
            btn.pack(side=tk.LEFT, padx=2)

        ttk.Button(self.input_tab, text="Save Output as PNG", command=self.save_output).pack(pady=5)
        ttk.Button(self.input_tab, text="Save Report as PDF", command=self.save_pdf).pack(pady=5)

    def insert_symbol(self, symbol):
        self.input_entry.insert(tk.END, symbol)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                if not self.df.empty:
                    numeric_cols = self.df.select_dtypes(include='number').columns.tolist()
                    if numeric_cols:
                        self.column_selector['values'] = numeric_cols
                        self.column_selector.set(numeric_cols[0])
                        self.select_column()
                    else:
                        messagebox.showerror("Error", "No numeric columns found in file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def select_column(self, event=None):
        col = self.column_selector.get()
        if self.df is not None and col:
            values = self.df[col].dropna().tolist()
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, ','.join(map(str, values)))

    def create_graph_tab(self):
        ttk.Label(self.graph_tab, text="Select Graph Type:").pack(pady=5)
        self.graph_type = ttk.Combobox(self.graph_tab, values=["Histogram", "Boxplot", "Normal Curve"])
        self.graph_type.current(0)
        self.graph_type.pack(pady=5)

        self.figure = plt.Figure(figsize=(6, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_tab)
        self.canvas.get_tk_widget().pack()

    def calculate(self):
        method = self.method_selector.get()
        raw_data = self.input_entry.get()
      
      
        import re
        symbol_map = {
            "μ": "mu",
            "σ": "sigma",
            "σ²": "variance",
            "∑": "sum",
            "x̄": "mean",
            "n": "n",
            "P": "P",
            "C": "C"
        }
        symbolic_values = {}
        symbol_matches = re.findall(r'([μσ∑x̄nPC]|σ²)\s*=\s*([\d.]+)', raw_data)
        for sym, val in symbol_matches:
            try:
                symbolic_values[symbol_map[sym]] = float(val)
            except Exception:
                pass
        


        extra = self.extra_entry.get()
        latex = ""
        try:
            data = [float(x.strip()) for x in raw_data.split(',') if x.strip() and self.is_number(x.strip())]
            result = None
            if method == "Mean":
                result = self.stats.mean(data)
                latex = f"x̄ = {result}"
            elif method == "Median":
                result = self.stats.median(data)
                latex = f"Median = {result}"
            elif method == "Mode":
                result = self.stats.mode(data)
                latex = f"Mode = {result}"
            elif method == "Standard Deviation":
                result = self.stats.standard_deviation(data)
                latex = f"σ = {result}"
            elif method == "Variance":
                result = self.stats.variance(data)
                latex = f"σ² = {result}"
            elif method == "Z-Score":
                result = self.stats.z_score(data)
                mean = symbolic_values.get("mu") or symbolic_values.get("mean") or self.stats.mean(data)
                std = symbolic_values.get("sigma") or self.stats.standard_deviation(data)
                latex = f"z-scores = {result}\n μ = {mean}, σ = {std}"
            elif method == "Expected Value":
                result = self.stats.expected_value(data)
                latex = f"E(X) = {result}"
            elif method == "Permutations":
                if not extra.isdigit():
                    messagebox.showerror("Input Error", "Please enter a valid value for r (extra field)")
                    return
                result = self.stats.permutations(len(data), int(extra))
                latex = f"P({len(data)}, {extra}) = {result}"
            elif method == "Combinations":
                if not extra.isdigit():
                    messagebox.showerror("Input Error", "Please enter a valid value for r (extra field)")
                    return
                result = self.stats.combinations(len(data), int(extra))
                latex = f"C({len(data)}, {extra}) = {result}"
            elif method == "Moments":
                result = self.stats.moment(data, int(extra) if extra else 2)
                latex = f"Moment order {extra or 2} = {result}"

            self.output_label.config(text=f"Result: {latex}")
            self.update_graph(data)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def update_graph(self, data):
        graph = self.graph_type.get()
        self.ax.clear()
        if graph == "Histogram":
            self.ax.hist(data, bins=10, color='skyblue', edgecolor='black')
            self.ax.set_title("Histogram")
        elif graph == "Boxplot":
            self.ax.boxplot(data)
            self.ax.set_title("Boxplot")
        elif graph == "Normal Curve":
            mean = np.mean(data)
            std = np.std(data)
            x = np.linspace(min(data), max(data), 100)
            y = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean)/std)**2)
            self.ax.plot(x, y, color='green')
            self.ax.set_title("Normal Distribution Curve")
        self.canvas.draw()

    def save_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            self.figure.savefig(file_path)
            messagebox.showinfo("Saved", f"Graph saved as {file_path}")

    def save_pdf(self):
        from matplotlib.backends.backend_pdf import PdfPages
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from io import BytesIO
        import tempfile

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if file_path:
            try:
                tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                self.figure.savefig(tmp_img.name)

                c = canvas.Canvas(file_path, pagesize=letter)
                c.setFont("Helvetica", 12)
                c.drawString(72, 750, "Statistics Report")
                for i, line in enumerate(self.output_label.cget("text").split("")):
                    c.drawString(72, 730 - (i * 15), line)
                c.drawImage(tmp_img.name, 72, 400, width=450, preserveAspectRatio=True)
                c.save()

                messagebox.showinfo("Saved", f"Report saved as {file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


    def toggle_theme(self):
        if self.dark_mode.get():
            self.root.configure(bg="#2e2e2e")
            for widget in [self.input_tab, self.graph_tab]:
                try:
                    widget.tk.call("tk::unsupported::MacWindowStyle", "style", widget._w, "plain", "none")
                except:
                    pass
        else:
            self.root.configure(bg="#f4f4f4")
            for widget in [self.input_tab, self.graph_tab]:
                try:
                    widget.tk.call("tk::unsupported::MacWindowStyle", "style", widget._w, "plain", "none")
                except:
                    pass



def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x200+500+300")
    splash.configure(bg="#f4f4f4")
    tk.Label(splash, text="Statistics Calculator", font=("Segoe UI", 18, "bold"), bg="#f4f4f4").pack(expand=True)
    splash.after(2000, splash.destroy)















































# import tkinter as tk
# from tkinter import messagebox, simpledialog, scrolledtext, Toplevel
# import stats

# class StatisticsGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Statistics Calculator")
#         self.root.geometry("600x600")

#         self.label = tk.Label(root, text="Enter Data Below:", font=("Helvetica", 14))
#         self.label.pack(pady=10)

#         self.data_entry = tk.Entry(root, width = 30)
#         self.data_entry.pack(pady=5)
#         # Calculate button & output display
#         self.result = tk.StringVar()
#         self.result_label = tk.Label(root, textvariable=self.result, font=("Arial", 12))
#         self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
#         self.calculate_button.pack(pady=5)
#         self.result_label.pack(pady=5)

#         self.permutation_button = tk.Button(root, text="Permutations", command=self.permutation)
#         self.permutation_button.pack(pady=5)

#         self.combination_button = tk.Button(root, text="Combinations", command=self.combination)
#         self.combination_button.pack(pady=5)

#         self.help_button = tk.Button(root, text="Help/Instructions", command=self.show_help)
#         self.help_button.pack(pady=5)

#         self.back_button = tk.Button(root, text="Back to Main", command=self.root.destroy)
#         self.back_button.pack(pady=5)

#         self.output_area = scrolledtext.ScrolledText(root, height=8, width=40)
#         self.output_area.pack(pady=10)



#     def calculate(self):
#         try:
#             data = self.data_entry.get()
#             ans = stats.run(data)
#             self.result.set(str(ans))  
#         except Exception as e:
#             self.result.set("Error")


    
#     def permutation(self):
#         # Create a new pop-up window
#         self.popup = Toplevel(self.root)
#         self.popup.title("Permutation")
#         self.popup.geometry("400x300")
             
#         tk.Label(self.popup, text="Input Total Number of Elements (n):").pack(pady=5)
#         self.n = tk.Entry(self.popup)
#         self.n.pack(pady=5)
     
#         tk.Label(self.popup, text="Input Number of Elements Selected (r):").pack(pady=5)
#         self.r = tk.Entry(self.popup)
#         self.r.pack(pady=5)

#         self.operation = 0
        
#         # Create and pack the submit button
#         submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
#         submit_button.pack(pady=10)


    
#     def combination(self):
#         # Create a new pop-up window
#         self.popup = Toplevel(self.root)
#         self.popup.title("Combination")
#         self.popup.geometry("400x300")
             
#         tk.Label(self.popup, text="Input Total Number of Elements (n):").pack(pady=5)
#         self.n = tk.Entry(self.popup)
#         self.n.pack(pady=5)
     
#         tk.Label(self.popup, text="Input Number of Elements Selected (r):").pack(pady=5)
#         self.r = tk.Entry(self.popup)
#         self.r.pack(pady=5)

#         self.operation = 1
        
#         # Create and pack the submit button
#         submit_button = tk.Button(self.popup, text="Submit", command=self.submit)
#         submit_button.pack(pady=10)

#     def submit(self):
#         n = self.n.get()
#         n = int(n)
#         r = self.r.get()
#         r = int(r)
#         if self.operation == 0:
#             result = stats.permutation(n, r)
#         else:
#             result = stats.combination(n, r)
#         self.display_result(result)
#         self.popup.destroy()

#     def get_user_input(self, prompt):
#         return simpledialog.askstring("Input", prompt)

#     def display_result(self, result):
#         self.output_area.delete(1.0, tk.END)
#         self.output_area.insert(tk.END, result)

#     def show_help(self):
#         help_text = (
#             "Welcome to the Algebra Calculator!\n"
#             "Here’s how to use each function:\n\n"
#             "- Solve Linear Equation: Enter an equation like ax + b = 0\n"
#             "- Find Vertex: Enter a quadratic equation like ax^2 + bx + c\n"
#             "- Solve Inequality: Enter an inequality like ax + b > 0\n\n"
#             "Results will appear in the output box below."
#         )
#         messagebox.showinfo("Help", help_text)