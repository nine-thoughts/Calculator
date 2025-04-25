import math
import re
def validate(arg):
    is_valid = True
    arg = arg.replace(" ", "")
    arg = arg.lower()
    allowed_txt = "0123456789^()*/+-e.%!"  # All allowed mathematical characters
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



def replace_factorial(match):
    expression = match.group(1)
    try:
        ans = eval(expression)
        if isinstance(ans, int) or (isinstance(ans, float) and ans.is_integer()):
            return str(factorial(int(ans)))
        else:
            return "Error: Factorials must be an integer value"
    except Exception as e:
        return f"Invalid expression inside factorial: {e}"



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



def compute(arg):
    if validate(arg):
        arg = re.sub(r'\((.*?)\)!', replace_factorial, arg) 
        arg = re.sub(r'(\d+(\.\d+)?)!', replace_factorial, arg)
        try:
            result = (eval(arg.replace('^', '**')))
            return(result)
        except:
            return "Error during computation"
    else:
        return "Error: Improper Input"
    