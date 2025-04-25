import math
from scipy.integrate import quad
import re



def validate(arg):
    # This function validates the user's input as being a valid input
    
    is_valid = True
    arg = arg.replace(" ", "")
    arg = arg.lower()
    allowed_txt = "0123456789^()*/+-e."  # All allowed mathematical characters
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]  # All basic trig functions
    inverse_trig_functions = ["arcsin", "arccos", "arctan", "arcsec", "arccsc", "arccot"]  # All complex trig functions
    
    i = 0  # Counter variable
    
    while i < len(arg):
        # Check if it matches any trigonometric function
        matched = False
        for func in trig_functions + inverse_trig_functions:
            if arg[i:i+len(func)] == func and i + len(func) < len(arg) and arg[i+len(func)] == "(":
                i += len(func)  # Skip the matched function
                matched = True
                break  # Exit the loop once a match is found
        
        if not matched:
            if arg[i] in allowed_txt:
                i += 1  # Proceed to the next character if valid
            else:
                is_valid = False
                break  # Stop and return false when something is not valid
    
    return is_valid



def preprocess_expression(expression):
    # This function takes an expression and does the appropriate substitions for the math module
    
    replacements = {
        "sin(": "math.sin(",
        "cos(": "math.cos(",
        "tan(": "math.tan(",
        "cot(": "1/math.tan(",
        "sec(": "1/math.cos(",
        "csc(": "1/math.sin(",
        "arcsin(": "math.asin(",
        "arccos(": "math.acos(",
        "arctan(": "math.atan(",
        "arccot(": "math.pi/2 - math.atan(",
        "ln(": "math.log(",
        "log(": "math.log10(",
        "pi": "math.pi",
        "e": "math.e",
        "^": "**" 
    }

    expression = expression.replace(" ", "")
    expression = expression.lower()

    for shorthand, full_form in replacements.items():
        expression = expression.replace(shorthand, full_form)

    # Add multiplication between a number and a math function or variable
    expression = re.sub(r'(\d)(math\.|[a-zA-Z])', r'\1*\2', expression)  # Number followed by math function or variable
    expression = re.sub(r'(\))(math\.|[a-zA-Z])', r'\1*\2', expression)  # Closing parenthesis followed by math function or variable

    # Add multiplication between a closing parenthesis and a number
    expression = re.sub(r'(\))(\d)', r'\1*\2', expression)  # ')' followed by a number

    expression = expression.replace("log10*(x)", "log10(x)")
    expression = expression.replace("xmath.", "x*math.")

    return expression



def choose(a, b):
    # This function computes the value of aCb (a choose b)
    
    if a - b < 0:
        return "Error: Invalid numerical order"
   
    else:
        if a == int(a) and b == int(b):
            numerator = factorial(a)
            denominator = (factorial(b)) * (factorial(a - b))
            return numerator / denominator
        else:
            return "Error"



def factorial(a):
    # This function computes the factorial value of a
    
    ans = 1
    
    if a == int(a):
        
        if a == 0 or a == 1:
            return 1
        else:
            ans = a * factorial(a - 1)
            return ans

    else:
        return "Error: Factorial must be a whole number"



def binomial(n, p, k):
    # This function computes the binomial probability given necessary inputs
    
    if p <= 1 and p >= 0:
        if n == int(n) and k == int(k):
            if n >= 0 and k >= 0:
                q = 1 - p
                prob = choose(n, k) * (p**k) * (q ** (n-k))
                return prob
            else:
                return "Error: Must have a non-negative number of trials"
        else:
            return "Error: Must have an integer number of trials"
    else:
        return "Error: Probability must be between 0 and 1"



def geometric(p, k):
    # This function computes the geometric probability with necessary inputs
    
    if p >= 0 and p <= 1:
        if k == int(k):
            if k >= 0:
                q = 1 - p
                prob = (q ** (k - 1)) * (p)
                return prob
            else: 
                return "Error: Must have a non-negative success trial"
        else:
            return "Error: Must have an integer value for success trial"
    else:
        return "Error: Probability of success must be between 0 and 1"



def hypergeometric(N, n, K, k):
    # This function computes the hypergeometric probability given necessary inputs
    
    if N == int(N) and n == int(n) and K == int(K) and k == int(k):
        if N >= 0 and n >= 0 and K >= 0 and k >= 0:
            if N > n and K > k:
                numerator = choose(K, k) * choose(N - K, n - k)
                denominator = choose(N, n)
                return numerator / denominator
            else: 
                return "Error: Total trial range is smaller than selected trial range"
        else:
            return "Error: All values must be positive"
    else:
        return "Error: All values must be integers"



def poisson(k, lam):
    # This function computes the poisson probability given necessary inputs
    
    if k == int(k):
        if k >= 0:
            numerator = (lam ** k) * (math.e ** (-1*lam))
            denominator = factorial(k)
            return numerator / denominator
        else:
            return "Error: Must have a positive value for observations"
    else:
        return "Error: Must have an integer value for observations"



def normalpdf(x, mean, sd):
    # This function computes the PDF value of a normal distribution
    
    fraction = 1 / (sd * math.sqrt(2 * math.pi))
    exponent = -0.5 * (((x - mean) / sd) ** 2)
    return fraction * (math.e ** exponent)



def normalcdf(x, mean, sd):
    # This function computes the CDF value of a normal distribution
    
    # Define the PDF of the normal distribution
    def normal_pdf(t, mean, sd):
        fraction = 1 / (sd * math.sqrt(2 * math.pi))
        exponent = -0.5 * ((t - mean) / sd) ** 2
        return fraction * math.exp(exponent)
    
    # Use integration to compute the CDF
    result, _ = quad(normal_pdf, -math.inf, x, args=(mean, sd))
    return result



def discrete_uniform(beg, end, a, b, unit):
    # This function computes the probability given necessary inputs of a discrete, unformly distributed item including endpoints
    
    # Total number of discrete steps in the range [beg, end]
    total_steps = int((end - beg) / unit) + 1  # Include both beg and end
    
    # Align 'a' and 'b' to the valid range [beg, end]
    lower_bound = max(beg, a)  # Ensure 'a' is not below the start
    upper_bound = min(end, b)  # Ensure 'b' is not above the end
    
    # Check if there are valid steps
    if lower_bound > upper_bound:
        return 0  # No valid range
    
    # Number of valid steps within [a, b]
    valid_steps = int((upper_bound - lower_bound) / unit) + 1  # Include both bounds
    
    # Probability of being within [a, b]
    prob = valid_steps / total_steps
    return prob



def continuous_uniform(a, b, c, d):
    # This function computes the probability given necessary inputs of a discrete, unformly distributed item
    
    if b < a:
        return "Error: Max Range is less than Min Range"
    elif b == a:
        return "Error: No usable range"
    else:
        if c > d:
            if c > b:
                return "Error: Searching outside of range"
            elif d > b:
                return "Error: Searching outside of range"
            elif c < a:
                return "Error: Searching outside of range"
            elif d < a:
                return "Error: Searching outside of range"
            else:
                return (c - d) / (b - a)
        
        elif d > c:
            if c > b:
                return "Error: Searching outside of range"
            elif d > b:
                return "Error: Searching outside of range"
            elif c < a:
                return "Error: Searching outside of range"
            elif d < a:
                return "Error: Searching outside of range"
            else:
                return (d - c) / (b - a)
        
        else:
            return 0



def compute_binomial():
    print("Computing binomial distributions")
    exit_flag = True
    while exit_flag:
        print('Number of Trials (or type "exit" to quit): ')
        trials = input()
        if trials.replace(" ", "").lower() == "exit":
            print("Returning to main page")
            exit_flag = False
            break
        if validate(trials): 
            print('Probability of Success (or type "exit" to quit): ')
            success = input()
            if success.replace(" ", "").lower() == "exit":  
                print("Returning to main page")
                exit_flag = False
                break
            if validate(success): 
                print('Number of Successes (or type "exit" to quit): ')
                num_success = input()
                if num_success.replace(" ", "").lower() == "exit": 
                    print("Returning to main page")
                    exit_flag = False
                    break
                if validate(num_success):
                    result = (binomial(float(trials), float(success), float(num_success)))
                    rounded = round(result, 15)
                    print("Probability = " + str(rounded))
                elif exit_flag == False:
                    break
                else:
                    print("Invalid input. Please try again.")
            
            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")


    
def solve_binomial(trials, success, num_success):
    if validate(trials): 
        if validate(success): 
            if validate(num_success):
                result = (binomial(float(trials), float(success), float(num_success)))
                rounded = round(result, 15)
                return "Probability = " + str(rounded)
            else:
                return "Invalid Input"
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_geometric():
    print("Computing geometric distributions")
    
    while True:
        print('Probability of success (or type "exit" to quit): ')
        prob = input()
        if prob.replace(" ", "").lower() == "exit": 
            print("Returning to distribution page")
            break
        if validate(prob):
            print('Success on trial number (or type "exit" to quit): ')
            success = input()
            if success.replace(" ", "").lower() == "exit": 
                print("Returning to distribution page")
                break
            if validate(success): 
                result = (geometric(float(prob), float(success)))
                rounded = round(result, 15)
                print("Probability = " + str(rounded))
            else:
                print("Invalid input. Please try again.")
        else:
            print("Invalid input. Please try again.")



def solve_geometric(prob, success):
    if validate(prob): 
        if validate(success): 
            result = (geometric(float(prob), float(success)))
            rounded = round(result, 15)
            return "Probability = " + str(rounded)
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_hypergeometric():
    print("Computing hypergeometric distributions")
    exit_flag = True
    while exit_flag:
        print('Number of elements in population (or type "exit" to quit): ')
        population = input()
        if population.replace(" ", "").lower() == "exit":
            print("Returning to distribution page")
            exit_flag = False
            break
        if validate(population): 
            print('Number of elements selected (or type "exit" to quit): ')
            trials = input()
            if trials.replace(" ", "").lower() == "exit":  
                print("Returning to distribution page")
                exit_flag = False
                break
            if validate(trials): 
                print('Number of successes in population (or type "exit" to quit): ')
                num_success = input()
                if num_success.replace(" ", "").lower() == "exit": 
                    print("Returning to distribution page")
                    exit_flag = False
                    break
                if validate(num_success):
                    print('Number of desired successes (or type "exit" to quit): ')
                    desired = input()
                    if desired.replace(" ", "").lower() == "exit":
                        print("Returning to distribution page")
                        exit_flag = False
                        break
                    if validate(desired):
                        result = (hypergeometric(float(population), float(trials), float(num_success), float(desired)))
                        rounded = round(result, 15)
                        print("Probability = " + str(rounded))
                    elif exit_flag == False:
                        break
                    else:
                        print("Invalid input. Please try again.")
                
                elif exit_flag == False:
                    break
                else:
                    print("Invalid input. Please try again.")
            
            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")



def solve_hypergeometric(population, trials, num_success, desired):
    if validate(population): 
        if validate(trials): 
            if validate(num_success):
                if validate(desired):
                    result = (hypergeometric(float(population), float(trials), float(num_success), float(desired)))
                    rounded = round(result, 15)
                    return "Probability = " + str(rounded)
                else:
                    return "Invalid Input"
            else:
                return "Invalid Input"
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_poisson():
    print("Computing poisson distributions")
    exit_flag = True
    while exit_flag:
        print('Average observation / lambda (or type "exit" to quit): ')
        lam = input()
        if lam.replace(" ", "").lower() == "exit": 
            print("Returning to distribution page")
            exit_flag = False
            break
        if validate(lam):
            print('Number of desired observations (or type "exit" to quit): ')
            success = input()
            if success.replace(" ", "").lower() == "exit": 
                print("Returning to distribution page")
                exit_flag = False
                break
            if validate(success): 
                result = (poisson(float(lam), float(success)))
                rounded = round(result, 15)
                print("Probability = " + str(rounded))
            
            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")



def solve_poisson(lam, success):
    if validate(lam): 
        if validate(success): 
            result = (poisson(float(lam), float(success)))
            rounded = round(result, 15)
            return "Probability = " + str(rounded)
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_normal_pdf():
    print("Computing normal distributions (PDF)")
    exit_flag = True
    while exit_flag: 
        print('Value of x (or type "exit" to quit): ')
        x = input()
        if x.replace(" ", "").lower() == "exit":
            print("Returning to distribution page")
            exit_flag = False
            break
        if validate(x): 
            print('Mean (or type "exit" to quit): ')
            mean = input()
            if mean.replace(" ", "").lower() == "exit":  
                print("Returning to distribution page")
                exit_flag = False
                break
            if validate(mean): 
                print('Standard deviation (or type "exit" to quit): ')
                sd = input()
                if sd.replace(" ", "").lower() == "exit": 
                    print("Returning to distribution page")
                    exit_flag = False
                    break
                if validate(sd):
                    result = (normalpdf(float(x), float(mean), float(sd)))
                    rounded = round(result, 15)
                    print("Probability = " + str(rounded))
                
                elif exit_flag == False:
                    break
                else:
                    print("Invalid input. Please try again.")
            
            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")



def solve_PDF(x, mean, sd):
    if validate(x): 
        if validate(mean): 
            if validate(sd):
                result = (normalpdf(float(x), float(mean), float(sd)))
                rounded = round(result, 15)
                return "Probability = " + str(rounded)
            else:
                return "Invalid Input"
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_normal_cdf():
    print("Computing normal distributions (CDF)")
    exit_flag = True
    while exit_flag:
        print('Value of x (or type "exit" to quit): ')
        x = input()
        if x.replace(" ", "").lower() == "exit":
            print("Returning to distribution page")
            exit_flag = False
            break
        if validate(x): 
            print('Mean (or type "exit" to quit): ')
            mean = input()
            if mean.replace(" ", "").lower() == "exit":  
                print("Returning to distribution page")
                exit_flag = False
                break
            if validate(mean): 
                print('Standard deviation (or type "exit" to quit): ')
                sd = input()
                if sd.replace(" ", "").lower() == "exit": 
                    print("Returning to distribution page")
                    exit_flag = False
                    break
                if validate(sd):
                    result = (normalcdf(float(x), float(mean), float(sd)))
                    rounded = round(result, 15)
                    print("Probability = " + str(rounded))
                
                elif exit_flag == False:
                    break
                else:
                    print("Invalid input. Please try again.")

            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")



def solve_CDF(x, mean, sd):
    if validate(x): 
        if validate(mean): 
            if validate(sd):
                result = (normalcdf(float(x), float(mean), float(sd)))
                rounded = round(result, 15)
                return "Probability = " + str(rounded)
            else:
                return "Invalid Input"
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_uniform_discrete():
    print("Computing uniform discrete distributions")
    exit_flag = True
    while exit_flag:    
        print('Beginning of range (or type "exit" to quit): ')
        beg = input()
        if beg.lower() == "exit":
            print("Returning to distribution page")
            exit_flag = False
            break
        if validate(beg): 
            print('End of range (or type "exit" to quit): ')
            end = input()
            if end.lower() == "exit":  
                print("Returning to distribution page")
                exit_flag = False
                break
            if validate(end): 
                print('Beginning of search range (or type "exit" to quit): ')
                a = input()
                if a.lower() == "exit": 
                    print("Returning to distribution page")
                    exit_flag = False
                    break
                if validate(a):
                    print('End of search range (or type "exit" to quit): ')
                    b = input()
                    if b.lower() == "exit":
                        print("Returning to distribution page")
                        exit_flag = False
                        break
                    if validate(b):
                        print('Incriment value through search range (or type "exit" to quit): ')
                        unit = input()
                        if unit.lower() == "exit":
                            print("Returning to distribution page")
                            exit_flag = False
                            break
                        if validate(unit):
                            result = (discrete_uniform(float(beg), float(end), float(a), float(b), float(unit)))
                            rounded = round(result, 15)
                            print("Probability = " + str(rounded))
                        elif exit_flag == False:
                            break
                        else:
                            print("Invalid input. Please try again.")
                    
                    elif exit_flag == False:
                        break
                    else:
                        print("Invalid input. Please try again.")
                
                elif exit_flag == False:
                    break
                else:
                    print("Invalid input. Please try again.")
            
            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")



def solve_discrete(beg, end, a, b, unit):
    if validate(beg): 
        if validate(end): 
            if validate(a):
                if validate(b):
                    if validate(unit):
                        result = (discrete_uniform(float(beg), float(end), float(a), float(b), float(unit)))
                        rounded = round(result, 15)
                        return "Probability = " + str(rounded)
                    else:
                        return "Invalid Input"
                else:
                    return "Invalid Input"
            else:
                return "Invalid Input"
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def compute_uniform_continuous():
    print("Computing uniform continuous distributions")
    exit_flag = True
    while exit_flag:
        print('Beginning of total range (or type "exit" to quit): ')
        a = input()
        if a.replace(" ", "").lower() == "exit":
            print("Returning to distribution page")
            exit_flag = False
            break
        if validate(a): 
            print('End of total range (or type "exit" to quit): ')
            b = input()
            if b.replace(" ", "").lower() == "exit":  
                print("Returning to distribution page")
                exit_flag = False
                break
            if validate(b): 
                print('Beginning of search range (or type "exit" to quit): ')
                c = input()
                if c.replace(" ", "").lower() == "exit": 
                    print("Returning to distribution page")
                    exit_flag = False
                    break
                if validate(c):
                    print('End of search range (or type "exit" to quit): ')
                    d = input()
                    if d.replace(" ", "").lower() == "exit":
                        print("Returning to distribution page")
                        exit_flag = False
                        break
                    if validate(d):
                        result = (continuous_uniform(float(a), float(b), float(c), float(d)))
                        rounded = round(result, 15)
                        print("Probability = " + str(rounded))
                    elif exit_flag == False:
                        break
                    else:
                        print("Invalid input. Please try again.")
                
                elif exit_flag == False:
                    break
                else:
                    print("Invalid input. Please try again.")
            
            elif exit_flag == False:
                break
            else:
                print("Invalid input. Please try again.")
        
        elif exit_flag == False:
            break
        else:
            print("Invalid input. Please try again.")


def solve_continuous(beg, end, a, b):
    if validate(beg): 
        if validate(end): 
            if validate(a):
                if validate(b):
                    result = (continuous_uniform(float(beg), float(end), float(a), float(b)))
                    rounded = round(result, 15)
                    return "Probability = " + str(rounded)
                else:
                    return "Invalid Input"
            else:
                return "Invalid Input"
        else:
            return "Invalid Input"
    else:
        return "Invalid Input"



def help():
    print("Binomial: bin")
    print("Geometric: geo")
    print("Hypergeometric: hgm")
    print("Poisson: psd")
    print("Normal PDF: npd")
    print("Normal CDF: ncd")
    print("Discrete Uniform: dud")
    print("Continuous Uniform: cud")



def stat_distribution_page():
    while True:
        print("Welcome to the Statistical Distributions Page")
        print('You can type "exit" to quit to main page or "help" for the list of usable codes')
        
        arg = input()
        arg = arg.replace(" ", "").lower()
        
        if arg == "help":
            help()
            
        elif arg == "exit":
            print("Returning to main page")
            break
    
        elif arg == "bin":
            compute_binomial()
        
        elif arg == "geo":
            compute_geometric()
            
        elif arg == "hgm":
            compute_hypergeometric()
    
        elif arg == "psd":
            compute_poisson()
    
        elif arg == "npf":
            compute_normal_pdf()
    
        elif arg == "ncf":
            compute_normal_cdf()
    
        elif arg == "dud":
            compute_uniform_discrete()
    
        elif arg == "cud":
            compute_uniform_coninuous()