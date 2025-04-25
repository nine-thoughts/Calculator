from sympy import symbols, integrate, sympify, simplify, expand
import re
import math


def validate(arg):
    # This function validates the user's input as being a valid input
    
    is_valid = True
    arg = arg.replace(" ", "")
    allowed_txt = "0123456789^()*/xX+-e." # All allowed mathematical characters
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"] # All basic trig functions
    inverse_trig_functions = ["arcsin", "arccos", "arctan", "arcsec", "arccsc", "arccot"] # All complex (inverse) trig functions
    
    i = 0 # Counter variable
    
    while i < len(arg):
        # Check if a substring matches any trigonometric function
        if arg[i:i+3] in trig_functions and i + 3 < len(arg) and arg[i+3] == "(":
            i += 3  # Skip the trig function
        elif arg[i] in allowed_txt:
            i += 1  # Proceed to the next character if valid
        else:
            is_valid = False
            break
            # Stop and return false when something is not valid
    
    return is_valid



def validate_vec(arg):
    is_valid = True
    allowed_txt = "0123456789^()*/xX+-eijk."  # All allowed mathematical characters
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]  # All basic trig functions
    inverse_trig_functions = ["arcsin", "arccos", "arctan", "arcsec", "arccsc", "arccot"]  # All inverse trig functions
    
    # Remove spaces from the input
    arg = arg.replace(" ", "")
    
    i = 0  # Counter variable
    
    while i < len(arg):
        # Check if a substring matches any trigonometric function
        if (arg[i:i+3] in trig_functions or arg[i:i+6] in inverse_trig_functions) and i + 3 < len(arg) and arg[i+3] == "(":
            func_len = 3 if arg[i:i+3] in trig_functions else 6
            i += func_len
            if i < len(arg) and arg[i] == "(":
                i += 1
                while i < len(arg) and arg[i] != ")":
                    if arg[i] not in allowed_txt:
                        is_valid = False
                        break
                    i += 1
                if i < len(arg) and arg[i] == ")":
                    i += 1
                else:
                    is_valid = False
                    break
            else:
                is_valid = False
                break
        elif arg[i] in allowed_txt:
            i += 1  # Proceed to the next character if valid
        else:
            is_valid = False
            break
    
    return is_valid



def parse_vector(vector_str):
    # Remove all spaces from the input string
    vector_str = vector_str.replace(" ", "")
    
    vector_dict = {'i': '0', 'j': '0', 'k': '0'}  # Initialize coefficients as strings
    term = ""  # Accumulator for the current term

    i = 0  # Pointer to iterate through the string
    while i < len(vector_str):
        char = vector_str[i]

        if char in 'ijk':  # Check if current character is i, j, or k
            # Check if it is valid (followed by +, -, or the end of the string)
            next_char = vector_str[i + 1] if i + 1 < len(vector_str) else ""
            if next_char in "+-" or next_char == "":  # Valid i, j, or k
                term = term.strip()  # Clean up the term

                # Remove a leading "+" if present
                if term.startswith("+"):
                    term = term[1:]

                # Handle cases where the term is empty, "+" or "-"
                if term == "":
                    term = "1"
                elif term == "-":
                    term = "-1"

                # Assign the term to the corresponding direction
                vector_dict[char] = term
                term = ""  # Reset accumulator for the next term
            else:
                term += char  # If invalid (e.g., part of sin), continue adding to term
        else:
            term += char  # Continue accumulating characters for the current term

        i += 1  # Move to the next character

    # Final cleanup for leftover term (if the string ends without a final i, j, or k)
    term = term.strip()
    if term:
        if term.startswith("+"):
            term = term[1:]
        if term == "+":
            term = "1"
        elif term == "-":
            term = "-1"

        # Assign the leftover term to a missing direction
        for key in vector_dict:
            if vector_dict[key] == '0':
                vector_dict[key] = term
                break

    # Return the coefficients as a list in the order [i, j, k]
    return [vector_dict['i'], vector_dict['j'], vector_dict['k']]



def term_division(arg):
    # This function goes through the input and separates the string of math into individual terms (Based on +/- signs)
    
    terms = []
    term = ""
    paren_level = 0
    for char in arg:
        if char == "(":
            paren_level += 1
            term += char
        elif char == ")":
            paren_level -= 1
            term += char
        elif (char == "+" or char == "-") and paren_level == 0:
            if term:  # Ensure term is not empty
                terms.append(term)
            if char == "-":
                term = char  # Include the minus sign in the new term
            else:
                term = ""
        else:
            term += char
    if term:  # Add the last term if it's not empty
        terms.append(term)
    return terms



def exponent_mark_base(term):
    # This is one of two function pairs
    # This one goes through an individual term and returns the base (part without the exponent)
    
    base = ""
    exponent = ""
    term = term.replace("**", "^")
    found_x = False
    for char in term:
        if char != "^" and not found_x:
            if char != "x":
                base += char
            else:
                found_x = True
                if base == "" or base == "-":  # If no base is found or base is just a negative sign, set base to 1 or -1
                    base += "1"
        elif found_x:
            if char == "^":
                continue
            else:
                exponent += char
    if exponent == "":  # If no exponent is found, set exponent to 1
        exponent = "1"
    if base == "" and not found_x:  # If term is just a constant, set base to term
        base = term
    base = base.replace("(", "")
    base = base.replace(")", "")
    return base



def exponent_mark_exponent(term):
    # This is the second function in the family and returns the exponent portion of a term without its base
    # This is the same function as above, but with a different return variable
    
    base = ""
    exponent = ""
    term = term.replace("**", "^")
    found_x = False
    for char in term:
        if char != "^" and not found_x:
            if char != "x":
                base += char
            else:
                found_x = True
                if base == "" or base == "-":  # If no base is found or base is just a negative sign, set base to 1 or -1
                    base += "1"
        elif found_x:
            if char == "^":
                continue
            else:
                exponent += char
    if exponent == "" and found_x:  # If no exponent is found, set exponent to 1
        exponent = "1"
    elif exponent == "" and not found_x:
        exponent = "0"
    if base == "" and not found_x:  # If term is just a constant, set base to term
        base = term
    exponent = exponent.replace("(", "")
    exponent = exponent.replace(")", "")
    return exponent



def differentiate(base, exponent):
    # This is the differentiation function for basic terms (non-trig functions / terms)
    
    base = int(base)
    exponent = int(exponent)
    if base == 0:
        ans = 0
        ans = str(ans)
        return(ans)
    elif exponent == 0:
        ans = 0
        ans = str(ans)
        return(ans)
    ans = base*exponent
    if exponent - 1 == 0:
        ans = str(ans)
        return(ans)
    else:
        ans = str(ans)
        return(ans + "x" + "^" + str(exponent - 1))



def trig(term):
    # This function checks to determine if a term is a trig term
    
    # List of trigonometric functions
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]
    
    # Remove outer parentheses if present
    while term.startswith("(") and term.endswith(")"):
        term = term[1:-1]
    
    # Check if any trig function exists in the term followed by "("
    for func in trig_functions:
        if func in term:
            # Ensure it's followed by '(' to confirm it's a trig function
            index = term.find(func)
            if index != -1 and len(term) > index + len(func) and term[index + len(func)] == "(":
                return True
    
    return False



def trig_term_coefficient(term):
    # This function is apart of a family of functions
    # This goes through trig terms and outputs the coefficient of the trig term

    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]
    coefficient = ""
    trig_function = ""
    base = ""

    # Step 1: Find the trig function
    for func in trig_functions:
        if func in term:
            trig_function = func
            break

    if not trig_function:
        return "Error: No trigonometric function found."

    # Split into parts (coefficient and base)
    func_start = term.find(trig_function)
    before_func = term[:func_start]  # Everything before the trig function
    after_func = term[func_start + len(trig_function):]  # Everything after the trig function

    # Handle the coefficient
    if before_func == "" or before_func == "+":
        coefficient = "1"
    elif before_func == "-":
        coefficient = "-1"
    else:
        coefficient = before_func

    # Step 4: Extract the base
    if after_func.startswith("(") and after_func.endswith(")"):
        base = after_func[1:-1]  # Remove the surrounding parentheses
    else:
        return "Error: Invalid format, base must be enclosed in parentheses."

    return coefficient



def trig_term_function(term):
    # This function is apart of a family of functions
    # This goes through trig terms and outputs the trig function of the trig term
    # This is the same function as above

    
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]
    coefficient = ""
    trig_function = ""
    base = ""

    # Find the trig function
    for func in trig_functions:
        if func in term:
            trig_function = func
            break

    if not trig_function:
        return "Error: No trigonometric function found."

    # Split into parts (coefficient and base)
    func_start = term.find(trig_function)
    before_func = term[:func_start]  # Everything before the trig function
    after_func = term[func_start + len(trig_function):]  # Everything after the trig function

    # Handle the coefficient
    if before_func == "" or before_func == "+":
        coefficient = "1"
    elif before_func == "-":
        coefficient = "-1"
    else:
        coefficient = before_func

    # Extract the base
    if after_func.startswith("(") and after_func.endswith(")"):
        base = after_func[1:-1]  # Remove the surrounding parentheses
    else:
        return "Error: Invalid format, base must be enclosed in parentheses."

    return trig_function



def trig_term_base(term):
    # This function is apart of a family of functions
    # This goes through trig terms and outputs the base of the trig term (what's inside parenthesis)
    # Same function as above

    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]
    coefficient = ""
    trig_function = ""
    base = ""

    # Find the trig function
    for func in trig_functions:
        if func in term:
            trig_function = func
            break

    if not trig_function:
        return "Error: No trigonometric function found."

    # Split into parts (coefficient and base)
    func_start = term.find(trig_function)
    before_func = term[:func_start]  # Everything before the trig function
    after_func = term[func_start + len(trig_function):]  # Everything after the trig function

    # Handle the coefficient
    if before_func == "" or before_func == "+":
        coefficient = "1"
    elif before_func == "-":
        coefficient = "-1"
    else:
        coefficient = before_func

    # Extract the base
    if after_func.startswith("(") and after_func.endswith(")"):
        base = after_func[1:-1]  # Remove the surrounding parentheses
    else:
        return "Error: Invalid format, base must be enclosed in parentheses."

    return base



def differentiate_trig(term):
    # This function differentiates a trigonometric term using the chain rule and product rule
    
    terms = term_division(term)  # Split the input into individual terms
    result = []  # Store the terms for u * v' and u' * v
    
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]

    for single_term in terms:
        # Check if the term contains a trig function
        for func in trig_functions:
            if func in single_term:
                # Split the term into outer and trig parts
                index = single_term.find(func)
                outer_part = single_term[:index].strip()  # Coefficient or outer term
                trig_part = single_term[index:].strip()  # Trigonometric function part

                # Automatically assume a coefficient of 1 if none is present
                if not outer_part:
                    outer_part = "1"

                # Extract the inner function of the trig part
                inner_function = trig_part[len(func) + 1:-1]  # Inside parentheses

                # Differentiate the trig part using the chain rule
                if func == "sin":
                    trig_derivative = "cos"
                    trig_multiplier = 1
                elif func == "cos":
                    trig_derivative = "sin"
                    trig_multiplier = -1
                elif func == "tan":
                    trig_derivative = "sec^2"
                    trig_multiplier = 1
                elif func == "cot":
                    trig_derivative = "csc^2"
                    trig_multiplier = -1
                elif func == "sec":
                    trig_derivative = "sec * tan"
                    trig_multiplier = 1
                elif func == "csc":
                    trig_derivative = "-csc * cot"
                    trig_multiplier = -1

                # Differentiate the inner function
                inner_base = exponent_mark_base(inner_function)
                inner_exponent = exponent_mark_exponent(inner_function)
                inner_derivative = differentiate(inner_base, inner_exponent)

                # Format the derivative of the trig part
                trig_term_derivative = f"{trig_multiplier} * {inner_derivative} * {trig_derivative}({inner_function})"

                # Differentiate the outer part
                if outer_part:
                    outer_base = exponent_mark_base(outer_part)
                    outer_exponent = exponent_mark_exponent(outer_part)
                    outer_derivative = differentiate(outer_base, outer_exponent)

                    # First term: u * v'
                    first_term = f"{outer_part} * ({trig_term_derivative})"
                    # Second term: u' * v
                    second_term = f"{outer_derivative} * {trig_part}"
                else:
                    # If there is no outer part, the first term is just the trig term derivative
                    first_term = trig_term_derivative
                    second_term = trig_part  # No differentiation for the second term

                # Append the terms to the result list
                result.append(first_term)
                result.append(second_term)
                break
        else:
            # If it's not a trig function, just differentiate the term directly
            base = exponent_mark_base(single_term)
            exponent = exponent_mark_exponent(single_term)
            result.append(differentiate(base, exponent))

    solution = ""
    count = 0  # Use a counter to track the number of valid terms added
    
    for term in result:
        # Extract non-trigonometric components
        factor = extract_non_trig_components(term)
        
        # Get the coefficient and simplify the term
        ans = multiply_terms(factor.replace("*", ""))
    
        # Check the value of the coefficient returned by multiply_terms
        if ans == "0":
            # Skip the term entirely if the coefficient is 0
            continue
        elif ans == "1":
            # If the coefficient is 1, only add the trigonometric function
            simplified_term = extract_trig_function(term)
        else:
            # Otherwise, include the coefficient and the trigonometric function
            simplified_term = ans + extract_trig_function(term)
    
        # Append the term to the solution string
        if count > 0:
            # Add a `+` only after the first valid term
            solution += "+"
        solution += simplified_term
        count += 1
        
    solution = solution.replace("+-", "-")
    solution = solution.replace("-+", "-")
    solution = solution.replace("++", "+")
    solution = solution.replace("--", "+")
    return solution



def extract_trig_function(term):
    # This function extracts the trigonometric function and its argument from a given term.

    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]
    
    # Loop through possible trigonometric functions to find a match
    for func in trig_functions:
        if func in term:
            # Find where the trig function starts
            index = term.find(func)
            
            # Extract the trig function and its argument
            start = index
            end = term.find(")", index) + 1  # Find the closing parenthesis
            return term[start:end]  # Return only the trig function and its argument
    
    # If no trig function is found, return None or an appropriate message
    return None



def multiply_terms(expression):
    # This function multiplies terms containing powers of x and coefficients
    # Separate terms with a space
    
    terms = expression.split()  # Split the input by spaces
    total_coefficient = 1  # Start with neutral coefficient for multiplication
    total_power = 0  # Start with zero power for 'x'

    for term in terms:
        # Separate coefficient and power
        if "x" in term:
            if "^" in term:  # Handle terms like "4x^2"
                coeff, exp = term.split("x^")
                coeff = int(coeff) if coeff else 1  # Default coefficient to 1 if empty
                exp = int(exp)
            else:  # Handle terms like "4x"
                coeff = int(term.split("x")[0]) if term.split("x")[0] else 1
                exp = 1
        else:  # Handle constants without 'x'
            coeff = int(term)
            exp = 0

        # Multiply coefficients and add powers
        total_coefficient *= coeff
        total_power += exp

    # Format the result
    if total_power == 0:  # If no power of x is present
        return str(total_coefficient)
    elif total_power == 1:  # If x^1, omit the exponent
        return f"{total_coefficient}x"
    else:  # General case
        return f"{total_coefficient}x^{total_power}"



def extract_non_trig_components(term):
    # This function takes a trig function and returns the argument without the trig component
    
    # Split the term by the multiplication symbol
    components = term.split(" * ")
    non_trig_components = []  # To store non-trigonometric components

    # Define trigonometric functions
    trig_functions = ["sin", "cos", "tan", "cot", "sec", "csc"]

    # Identify and keep only non-trigonometric components
    for component in components:
        # Check if the component contains any trig function
        if not any(trig in component for trig in trig_functions):
            # Keep the component as a string without evaluating it
            non_trig_components.append(component.strip("() "))  # Remove unnecessary parentheses/whitespace

    # Return the non-trigonometric components joined with " * "
    return " * ".join(non_trig_components)



def def_integration(lower_limit, upper_limit, equation, n=1000):
    # This function computes the answer to the definite integration of a function given limits
    
    # Replace constants in the limits
    constants = {
        "pi": math.pi,
        "e": math.e
    }
    
    def process_limit(limit):
        # Process integration limits to handle strings like 'pi', 'e', or numerical values.
        if isinstance(limit, (float, int)):  # If it's already numeric, use it directly
            return limit
        elif isinstance(limit, str):
            limit = limit.lower().strip()
            return constants.get(limit, None) if limit in constants else float(limit)
        else:
            raise ValueError(f"Invalid limit: {limit}")

    # Process the limits using the helper function
    try:
        lower_limit = process_limit(lower_limit)
        upper_limit = process_limit(upper_limit)
    except ValueError as e:
        raise ValueError(f"Error in processing limits: {e}")

    # Replace constants and symbols in the equation
    equation = equation.replace("e", str(math.e))
    equation = equation.replace("pi", str(math.pi))
    equation = equation.replace("^", "**")  # Replace caret operator with Python power operator

    # Use regular expressions to insert '*' for implicit multiplication (e.g., 2x -> 2*x)
    equation = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", equation)  # Number followed by variable
    equation = re.sub(r"(\))(\d)", r"\1*\2", equation)  # Closing parenthesis followed by number

    # Define the width of each subinterval
    width = (upper_limit - lower_limit) / n

    # Function to safely evaluate the equation for a given value of x
    def f(x):
        try:
            # Use eval with math functions explicitly passed in the globals context
            return eval(equation, {"x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                                   "exp": math.exp, "log": math.log, "sqrt": math.sqrt})
        except Exception as e:
            raise ValueError(f"Error in evaluating the equation: {e}")

    # Apply the trapezoidal rule
    total_area = 0
    for i in range(n + 1):
        x = lower_limit + i * width
        weight = 1 if i == 0 or i == n else 2  # Endpoints get a weight
        total_area += weight * f(x)
        
    # Multiply the total sum by width/2 to get the integral approximation
    # Round the result to 6 decimal places
    return round((total_area * width) / 2, 6)



def double_dif(arg, depth = 1):
    terms = term_division(arg)          
    output_terms = []
    for term in terms:
        if not trig(term): 
            output_terms.append(differentiate(exponent_mark_base(term), exponent_mark_exponent(term)))
        elif trig(term):
            output_terms.append(differentiate_trig(term))
        else:
            return("Error during calculation")
            
    
    output = ""
    counter = 0
    for terms in output_terms:
        if counter == 0:
            output = terms
            counter = counter + 1
        elif counter != 0:
            output = output + "+" + terms
    
    output = output.replace("+-", "-")
    output = output.replace("-+", "-")

    if depth == 2:
            return output
        
    # Recursive call, incrementing the depth
    return double_dif(output, depth + 1)



def preprocess_expression(expression):
    # Define a mapping of shorthand terms to their `math` module equivalents
    replacements = {
        "sin(": "math.sin(",
        "cos(": "math.cos(",
        "tan(": "math.tan(",
        "cot(": "1/math.tan(",  # cot(x) = 1/tan(x)
        "sec(": "1/math.cos(",  # sec(x) = 1/cos(x)
        "csc(": "1/math.sin(",  # csc(x) = 1/sin(x)
        "arcsin(": "math.asin(",
        "arccos(": "math.acos(",
        "arctan(": "math.atan(",
        "arccot(": "math.pi/2 - math.atan(",  # arccot(x) = pi/2 - atan(x)
        "ln(": "math.log(",
        "log(": "math.log10(",
        "pi": "math.pi",
        "e": "math.e",
        "^": "**"  # Handle caret for exponentiation
    }

    # Replace shorthand terms with their `math` equivalents
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



def has_log(function_str):
    # This function checks if an equation contains a log function
    
    # Bank of logarithmic terms to check for
    log_bank = ["log", "log10", "ln"]
    
    # Loop through the bank to check for any matches in the input string
    for term in log_bank:
        if term in function_str:
            return True
    return False



def log_roots(equation, low, high):
    # This function finds the zeros of a log-based equation

    equation = preprocess_expression(equation)
    # Preprocess the equation to handle logarithmic terms
    equation = preprocess_expression(equation)

    # Define the function for evaluating the equation
    def func(x):
        try:
            equation_with_x = equation.replace("x", str(x))
            return eval(equation_with_x, {"math": math}, {})
        except (ValueError, ZeroDivisionError, OverflowError):
            # If the function is undefined for x, return None
            return None
    
    # Domain settings
    resolution = 1000  # Number of sample points
    step = (high - low) / resolution
    
    # Root searching
    roots = []
    x = low
    while x <= high:
        try:
            # Evaluate the function at the current x
            y1 = func(x)
            if y1 is None:  # Skip undefined parts of the domain
                x += step
                continue
            
            # Check if the function value is zero within tolerance
            if abs(y1) < 1e-6:
                if not roots or all(abs(x - r) > 0.01 for r in roots):  # Avoid duplicate roots
                    roots.append(round(x, 6))
            
            # Evaluate at the next step
            y2 = func(x + step)
            if y2 is None:  # Skip undefined parts
                x += step
                continue
            
            # Detect sign change for a root
            if y1 * y2 < 0:  # Sign change detected
                left, right = x, x + step
                # Refine root using bisection method
                while right - left > 1e-6:
                    mid = (left + right) / 2
                    mid_value = func(mid)
                    if mid_value is None:  # Skip undefined midpoints
                        break
                    if func(left) * mid_value < 0:
                        right = mid
                    else:
                        left = mid
                root = round((left + right) / 2, 6)
                if not roots or all(abs(root - r) > 0.01 for r in roots):  # Avoid duplicate roots
                    roots.append(root)
        except:
            pass
        x += step
    
    return sorted(roots)



def trig_roots(equation, low, high):
    equation = preprocess_expression(equation)
    print(low)
    low = float(low)
    high = float(high)
    def func(x):
        equation_with_x = equation.replace("x", str(x))
        return eval(equation_with_x, {"math": math}, {})

    # Domain settings
    domain_start = low
    domain_end = high
    resolution = 1000  # Maintain optimized sampling resolution
    step = (float(domain_end) - float(domain_start)) / resolution
    
    # Root searching
    roots = []
    x = domain_start
    while x <= domain_end:
        try:
            # Explicitly check zero and avoid clusters
            if abs(func(x)) < 1e-8:  # Stricter tolerance for zero detection
                if not roots or all(abs(x - r) > 0.15 for r in roots):  # Wider spacing for duplicates
                    roots.append(round(x, 8))  # Increased rounding precision     
            # Detect sign change for root
            y1 = func(x)
            y2 = func(x + step)
            if y1 * y2 < 0:
                left, right = x, x + step
                # Refine root using higher-precision bisection
                while right - left > 1e-8:  # Increased refinement precision
                    mid = (left + right) / 2
                    if func(left) * func(mid) < 0:
                        right = mid
                    else:
                        left = mid
                root = round((left + right) / 2, 8)
                if not roots or all(abs(root - r) > 0.15 for r in roots):  # Wider spacing for duplicates
                    roots.append(root)
        except Exception as e:
            print(f"Error occurred at x={x}: {e}")
        x += step
    
    # Explicitly add zero if it's missed but should exist
    if low < 0 < high and abs(func(0)) < 1e-8 and 0.0 not in roots:
        roots.append(0.0)
    
    return sorted(roots)



def poly_roots(func_str, low, high, tolerance=1e-6):
    func_str = preprocess_expression(func_str)
    func = lambda x: eval(func_str)

    # Special case for linear functions
    if func(0) == 0:  # Check if x = 0 is a root
        return [0.0]

    # Existing code for other functions
    num_intervals = 10
    step = (high - low) / num_intervals
    roots = []

    for i in range(num_intervals):
        interval_low = low + i * step
        interval_high = interval_low + step

        if func(interval_low) * func(interval_high) > 0:
            continue
        
        while (interval_high - interval_low) > tolerance:
            mid = (interval_low + interval_high) / 2
            if func(mid) == 0:
                roots.append(mid)
                break
            elif func(interval_low) * func(mid) < 0:
                interval_high = mid
            else:
                interval_low = mid

        root = (interval_low + interval_high) / 2
        if not any(abs(root - r) < tolerance for r in roots):
            roots.append(root)

    verified_roots = [r for r in roots if abs(func(r)) < tolerance]
    return sorted([round(r, 6) for r in verified_roots])



def apply_syntax(equation):
    # This function adds the * signs as required for proper functioning of the below function
    
    equation = re.sub(r'(\d)([a-zA-Z])', r'\1 * \2', equation)
    
    equation = re.sub(r'([a-zA-Z])(?=(sin|cos|tan|arcsin|arccos|arctan|sec|csc|cot))', r'\1 * ', equation)

    # Return the preprocessed equation
    return equation

def function_at_point(equation, x_value):
    # Computes the solution to an equation at a given x_value
    
    # Preprocess the equation to correct formatting
    equation = apply_syntax(equation)
    
    # Replace terms with their equivalents in the math module
    replacements = {
            "sin(": "math.sin(",
            "cos(": "math.cos(",
            "tan(": "math.tan(",
            "cot(": "1/math.tan(",  # cot(x) = 1/tan(x)
            "sec(": "1/math.cos(",  # sec(x) = 1/cos(x)
            "csc(": "1/math.sin(",  # csc(x) = 1/sin(x)
            "arcsin(": "math.asin(",
            "arccos(": "math.acos(",
            "arctan(": "math.atan(",
            "arccot(": "math.pi/2 - math.atan(",  # arccot(x) = pi/2 - atan(x)
            "ln(": "math.log(",  # ln(x) = log(x) in base e
            "log(": "math.log10(",  # log(x) = log(x) in base 10
            "pi": "math.pi",
            "e": "math.e",
            "^": "**"
        }
    
    for key, value in replacements.items():
        equation = equation.replace(key, value)
    
    try:
        evaluated_equation = equation.replace("x", f"({x_value})")
        
        # Use eval with an explicit reference to the math module
        result = eval(evaluated_equation, {"__builtins__": None, "math": math})
        return result
    except Exception as e:
        return f"Error evaluating the function: {e}"



def deriv(arg):
    terms = term_division(arg)            
    output_terms = []
    for term in terms:
        if not trig(term): 
            output_terms.append(differentiate(exponent_mark_base(term), exponent_mark_exponent(term)))
        elif trig(term):
            output_terms.append(differentiate_trig(term))
        else:
            print("Error during calculation")
    
    output = ""
    counter = 0
    for terms in output_terms:
        if counter == 0:
            output = terms
            counter = counter + 1
        elif counter != 0:
            output = output + "+" + terms
    
    output = output.replace("+-", "-")
    output = output.replace("-+", "-")
    return output



def min_max(function, lower, upper):
    deriv_2 = double_dif(function)
    deriv_1 = deriv(function)
    if not trig(function):
        points = poly_roots(deriv_1, lower, upper)
    elif trig(function):
        points = trig_roots(deriv_1, lower, upper)
    elif has_log(function):
        points = log_roots(deriv_1, lower, upper)
    min = []
    max = []
    
    for numbers in points:
        if function_at_point(deriv_2, numbers) < 0:
            max.append(numbers)
        elif function_at_point(deriv_2, numbers) > 0:
            min.append(numbers)
        else:
            return "Error"
    return min, max



def poly_integral(arg):
    base = eval(exponent_mark_base(arg)) / (float(exponent_mark_exponent(arg)) + 1)
    exponent = float(exponent_mark_exponent(arg)) + 1
    
    if base == int(base):
        base = str(base).replace(".0", "")
        if base == "1":
            base = base.replace("1", "")

    if exponent == int(exponent):
        exponent = str(exponent).replace(".0", "")
    
    return str(base) + "x^" + str(exponent)



def integration(function_str, variable_str='x'):
    function_str = function_str.replace("^", "**")
    
    # Insert multiplication symbols where missing
    function_str = re.sub(r"(?<=\d)([a-zA-Z])", r"*\1", function_str)
    function_str = re.sub(r"([a-zA-Z])(?=\d)", r"\1*", function_str)
    
    # Define the variable
    x = symbols(variable_str)
    
    # Parse the function string into a symbolic expression
    try:
        func = sympify(function_str)
    except SympifyError as e:
        return f"Error: Could not parse the function string '{function_str}'. {e}"
    
    # Compute the indefinite integral
    integral_result = integrate(func, x)
    
    # Expand and simplify the result to make it easier to format
    simplified_result = expand(simplify(integral_result))
    
    # Format terms to explicitly show division with parentheses
    formatted_result = str(simplified_result).replace("**", "^")
    formatted_result = re.sub(r"(\d+)\*([a-zA-Z])\^(\d+)/(\d+)", r"(\1/\4)\2^\3", formatted_result)
    formatted_result = re.sub(r"([a-zA-Z])\^(\d+)/(\d+)", r"(1/\3)\1^\2", formatted_result)
    formatted_result = formatted_result.replace("*x", "x")
    
    return formatted_result



def compute_derivative():
    print('You are now performing differentiation.')
    exit_flag = True
    while exit_flag:
        print('Please input the function you wish to differentiate using only "x" for the variable and "^" for exponents')
        print('Type "exit" at any time to return to the calculus page')
        arg = input()
        arg = arg.replace(" ", "").lower()
        
        if arg == "exit":
            print("Returning to calculus page")
            exit_flag = False
            break

        if validate(arg):
            print(deriv(arg))
        else:
            print('Invalid input. Try again or type "exit" to return to mainpage.')



def compute_integration():
    print("You are now performing integration.")
    exit_flag = True
    while exit_flag:
        end_flag = True
        print("Would you like Indefinite (IND) or Definite (DFN) Integration?")
        arg = input()
        arg = arg.replace(" ", "").lower()
       
        if arg == "ind":
            while end_flag:
                print('Now performing indefinite integration. Input an equation')
                print('Type "exit" to return to the calculus page, or type "end" to return to integration setting.')
                arg = input()
                arg = arg.replace(" ", "").lower()
                if arg == "exit":
                    print('Returning to calculus page')
                    end_flag = False
                    exit_flag = False
                    break
                elif arg == "end":
                    print('Returning to Integration Settings')
                    end_flag = False
                    break
                if validate(arg):
                    result = integration(arg)
                    print(result)
                else:
                    print('Invalid input. Try again or type "exit" to return to the calculus mainpage')
            if exit_flag == False:
                break

        elif arg == "dfn":
            print('Now performing definite integration. Input an equation')
            print('Type "exit" to return to the calculus page, or type "end" to return to integration setting.')
            while end_flag:
                arg = input()
                arg = arg.replace(" ", "").lower()
                if arg == "exit":
                    print('Returning to calculus page')
                    end_flag = False
                    exit_flag = False
                    break
                elif arg == "end":
                    print('Returning to Integration Settings')
                    end_flag = False
                    break
                elif validate(arg):
                    print("Input lower bound: ")
                    lower = input()
                    print("Inpute upper bound: ")
                    upper = input()
                    print(def_integration(lower, upper, arg, n=1000))
        
                else: 
                    print('Invalid input. Try again or type "exit" to return to calculus page')
            if exit_flag == False:
                break

        elif arg == "exit":
            print("Returning to calculus page.")
            break
        else:
            print('Invalid input. Try again or type "exit" to return to calculus page.')



def compute_poi():
    print("Now solving for an equation's POI in a given range.")
    exit_flag = True
    while exit_flag:
        print('Please enter the equation using on x for the variable or type "exit" to return to the calculus page')
        arg = input()
        arg = arg.replace(" ", "")
        if arg.lower() == "exit":
            print("Returning to calculus page")
            exit_flag = False
            break

        if validate(arg):
            dif_2 = double_dif(arg)
            if trig(dif_2):
                poi = trig_roots(dif_2, -1000, 1000)
            elif has_log(dif_2):
                poi = log_roots(dif_2, -1000, 1000)
            else:
                poi = poly_roots(dif_2, -1000, 1000)

            if not poi:
                print("This function does not have a point of inflection")
            for num in poi:
                print(f"{arg} has a POI at x = {num}")



def solve_poi(arg):
    arg = arg.replace(" ", "")
    if validate(arg):
        dif_2 = double_dif(arg)
        if trig(dif_2):
            poi = trig_roots(dif_2, -1000, 1000)
        elif has_log(dif_2):
            poi = log_roots(dif_2, -1000, 1000)
        else:
            poi = poly_roots(dif_2, -1000, 1000)
        if not poi:
            return "This function does not have a point of inflection"
        return poi
    else:
        return "Invalid user input"


def compute_min_max():
    print("Now solving for an equation's min and max value.")
    exit_flag = True
    while exit_flag:
        print('Please input the equation using only x for the variable or type "exit" to return to the calculus page')
        arg = input()
        arg = arg.replace(" ", "").lower()
        
        if arg == "exit":
            print("Returning to calculus page")
            exit_flag = False
            break

        if validate(arg):
            print("Minimum Domain: ")
            min = input()
            if min.lower() == "exit":
                print("Returning to calculus page")
                exit_flag = False
                break
        
            print("Maximum Domain: ")
            max = input()
            if max.lower() == "exit":
                print("Returning to calculus page")
                exit_flag = False
                break
    
            mnm = min_max(arg, float(min), float(max))
            minimum = mnm[0]
            maximum = mnm[1]
        
            for num in minimum:
                print("Minimum: " + str(num))
    
            for num in maximum:
                print("Maximum: " + str(num))



def compute_dot():
    print("Now computing vector dot products")
    exit_flag = True
    while exit_flag:
        print('Please enter the first vector using i, j, and k with +/- separating each value or type "exit" to return to the calculus page')
        vec_1 = input()
        vec_1 = vec_1.replace(" ", "")
        vec_1 = vec_1.lower()
        
        if vec_1.lower() == "exit":
            print("Returning to the calculus page")
            exit_flag = False
            break
        elif validate_vec(vec_1):
            vec_coeff = parse_vector(vec_1)
        else:
            print('Invalid vector input. Try again or type "exit" to quit')

        print("Please enter the second vector: ")
        vec_2 = input()
        vec_2 = vec_2.replace(" ", "")
        vec_2 = vec_2.lower()
        
        if vec_2.lower() == "exit":
            print("Returning to the calculus page")
            exit_flag = False
            break
        
        elif validate_vec(vec_2):
            vec_coeff2 = parse_vector(vec_2)
        
        else:
            print('Invalid vector input. Try again or type "exit" to quit')

        ans_i = float(eval(preprocess_expression(vec_coeff[0]))) * float(eval(preprocess_expression(vec_coeff2[0])))
        ans_j = float(eval(preprocess_expression(vec_coeff[1]))) * float(eval(preprocess_expression(vec_coeff2[1])))
        ans_k = float(eval(preprocess_expression(vec_coeff[2]))) * float(eval(preprocess_expression(vec_coeff2[2])))
        ans = ans_i + ans_j + ans_k
        print("The scalar result is " + str(ans))



def solve_dot(vec_1, vec_2):
    vec_1 = vec_1.replace(" ", "")
    vec_1 = vec_1.lower()
    
    if validate_vec(vec_1):
        vec_coeff = parse_vector(vec_1)
    else:
        return 'Invalid vector input'

    vec_2 = vec_2.replace(" ", "")
    vec_2 = vec_2.lower()
        
    if validate_vec(vec_2):
        vec_coeff2 = parse_vector(vec_2)
    else:
        return 'Invalid vector input.'

    ans_i = float(eval(preprocess_expression(vec_coeff[0]))) * float(eval(preprocess_expression(vec_coeff2[0])))
    ans_j = float(eval(preprocess_expression(vec_coeff[1]))) * float(eval(preprocess_expression(vec_coeff2[1])))
    ans_k = float(eval(preprocess_expression(vec_coeff[2]))) * float(eval(preprocess_expression(vec_coeff2[2])))
    ans = ans_i + ans_j + ans_k
    return str(ans)



def compute_cross():
    print("Now computing vector cross products")
    exit_flag = True
    while exit_flag:
        print('Please enter the first vector using i, j, and k with +/- separating each value or type "exit" to return to the calculus page')
        vec_1 = input()
        vec_1 = vec_1.replace(" ", "")
        vec_1 = vec_1.lower()
        
        if vec_1.lower() == "exit":
            print("Returning to the calculus page")
            exit_flag = False
            break
        
        elif validate_vec(vec_1):
            vec_coeff = parse_vector(vec_1)
        
        else:
            print('Invalid vector input. Try again or type "exit" to quit')

        print("Please enter the second vector: ")
        vec_2 = input()
        vec_2 = vec_2.replace(" ", "")
        vec_2 = vec_2.lower()
        if vec_2.lower() == "exit":
            print("Returning to the calculus page")
            exit_flag = False
            break
        
        elif validate_vec(vec_2):
            vec_coeff2 = parse_vector(vec_2)
        
        else:
            print('Invalid vector input. Try again or type "exit" to quit')

        ans_i = (float(eval(preprocess_expression(vec_coeff[1]))) * float(eval(preprocess_expression(vec_coeff2[2])))) - (float(eval(preprocess_expression(vec_coeff[2]))) * float(eval(preprocess_expression(vec_coeff2[1]))))  
        ans_j = (float(eval(preprocess_expression(vec_coeff[0]))) * float(eval(preprocess_expression(vec_coeff2[2])))) - (float(eval(preprocess_expression(vec_coeff[2]))) * float(eval(preprocess_expression(vec_coeff2[0]))))
        ans_k = (float(eval(preprocess_expression(vec_coeff[0]))) * float(eval(preprocess_expression(vec_coeff2[1])))) - (float(eval(preprocess_expression(vec_coeff[1]))) * float(eval(preprocess_expression(vec_coeff2[0]))))
        ans = str(ans_i) + "i " + "- " + str(ans_j) + "j " + "+ " + str(ans_k) + "k"
        ans = ans.replace("+ -", "- ")
        ans = ans.replace("- +", "- ") 
        print("The resultant vector is " + str(ans))


        
def solve_cross(vec_1, vec_2):
    vec_1 = vec_1.replace(" ", "")
    vec_1 = vec_1.lower()
    
    if validate_vec(vec_1):
        vec_coeff = parse_vector(vec_1)
    else:
        return 'Invalid vector input'

    vec_2 = vec_2.replace(" ", "")
    vec_2 = vec_2.lower()

    if validate_vec(vec_2):
        vec_coeff2 = parse_vector(vec_2)
    else:
        return 'Invalid vector input. Try again or type "exit" to quit'

    ans_i = (float(eval(preprocess_expression(vec_coeff[1]))) * float(eval(preprocess_expression(vec_coeff2[2])))) - (float(eval(preprocess_expression(vec_coeff[2]))) * float(eval(preprocess_expression(vec_coeff2[1]))))  
    ans_j = (float(eval(preprocess_expression(vec_coeff[0]))) * float(eval(preprocess_expression(vec_coeff2[2])))) - (float(eval(preprocess_expression(vec_coeff[2]))) * float(eval(preprocess_expression(vec_coeff2[0]))))
    ans_k = (float(eval(preprocess_expression(vec_coeff[0]))) * float(eval(preprocess_expression(vec_coeff2[1])))) - (float(eval(preprocess_expression(vec_coeff[1]))) * float(eval(preprocess_expression(vec_coeff2[0]))))
    ans = str(ans_i) + "i " + "- " + str(ans_j) + "j " + "+ " + str(ans_k) + "k"
    ans = ans.replace("+ -", "- ")
    ans = ans.replace("- +", "- ") 
    return str(ans)


def help():
    print("Differentiation = dif")
    print("Integration = int")
    print("Point of Inflection = poi")
    print("Minimum and Maximum = mnm")
    print("Vector Dot Products = dpx")
    print("Vector Cross Products = cpx")



def calculus_page():
    while True:
        print('Welcome to the Calculus Page')
        print('You can type "exit" to quit to main page or "help" for the list of usable codes')
    
        arg = input()
        arg = arg.replace(" ", "").lower()
    
        if arg == "help":
            help()
        
        elif arg == "exit":
            print("Returning to mainpage")
            break
        
        elif arg == "dif":
            compute_derivative()
        
        elif arg == "int":
            compute_integration()
                        
        elif arg == "poi":
            compute_poi()
        
        elif arg == "mnm":
            compute_min_max()
        
        elif arg == "dpx":
            compute_dot()
                    
        elif arg.lower() == "cpx":
            compute_cross() 