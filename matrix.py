import re
import math
from sympy import symbols, Matrix, solve, N



def dimension_validation(arg):

    pattern = r"^\d+x\d+$"

    if re.match(pattern, arg):
        valid = True
    else:
        valid = False

    return valid



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



def box_value(arg):
    arg = preprocess_expression(arg)
    return round(eval(arg), 15)



def make_matrix_row(arg):

    values_list = [value for value in arg.split(",")]
    simply = []
    for num in values_list:
        simply.append(box_value(num))
    return(simply)



def get_dimension_a(arg):

    dimensions = matrix_format.split("x")
    
    a = int(dimensions[0])
    
    return a



def get_dimension_b(arg):

    dimensions = matrix_format.split("x")

    b = int(dimensions[1])
    
    return b



def validate_matrix(arg, a, b):
    for row in arg:
        if len(row) != b:
            return False  

    if len(arg) != a:
        return False
        

    return True



def matrix_addition(matrix_1, matrix_2):
    matrix_3 = []
    r = 0
    for row in matrix_1: 
        matrix_3_row = []
        c = 0
        for num in row:
            matrix_3_row.append(num + matrix_2[r][c])
            c = c + 1
        matrix_3.append(matrix_3_row)
        r = r + 1
    return matrix_3



def matrix_subtraction(matrix_1, matrix_2):
    matrix_3 = []
    r = 0
    for row in matrix_1: 
        matrix_3_row = []
        c = 0
        for num in row:
            matrix_3_row.append(num - matrix_2[r][c])
            c = c + 1
        matrix_3.append(matrix_3_row)
        r = r + 1
    return matrix_3



def validate_multiplication_dimensions(a1, b1, a2, b2):
    valid = False
    if b1 == a2:
        valid = True
    return valid



def matrix_multiplication(matrix_1, matrix_2):

    matrix_3 = []
    for r in range(len(matrix_1)):
        matrix_3_row = []
        for c in range(len(matrix_2[0])):
            sum_product = 0
            for k in range(len(matrix_2)): 
                sum_product += matrix_1[r][k] * matrix_2[k][c]
            matrix_3_row.append(sum_product)
        matrix_3.append(matrix_3_row)
    return matrix_3



def matrix_inverse(matrix):
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise ValueError("The matrix must be square.")
    
    # Create an augmented matrix [matrix | identity]
    augmented = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    
    # Perform Gaussian elimination
    for i in range(n):
        # Make the pivot element 1
        pivot = augmented[i][i]
        if pivot == 0:
            raise ValueError("The matrix is singular and cannot be inverted.")
        for j in range(len(augmented[i])):
            augmented[i][j] /= pivot
        
        # Make other elements in column i to be 0
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(len(augmented[k])):
                    augmented[k][j] -= factor * augmented[i][j]
    
    # Extract the inverse matrix (right half of the augmented matrix)
    inverse = [row[n:] for row in augmented]
    
    # Round the results to 15 decimal places
    rounded_inverse = [[round(element, 15) for element in row] for row in inverse]
    return rounded_inverse



def eigen(matrix):
    y = symbols('y')  # Using 'y' instead of lambda
    symbolic_matrix = Matrix(matrix) - y * Matrix.eye(len(matrix))
    char_poly = symbolic_matrix.det()

    # Format polynomial with "^" for exponents
    formatted_poly = str(char_poly).replace("**", "^")

    # Solve for eigenvalues and round to 15 decimals
    eigenvalues = [N(sol, 15) for sol in solve(char_poly, y)]

    # Compute and round eigenvectors
    eigenvectors_data = Matrix(matrix).eigenvects()
    eigenvectors = {
        N(eigval, 15): [[N(entry, 15) for entry in eigvecs[0]]]
        for eigval, _, eigvecs in eigenvectors_data
    }

    # Print results in requested format
    print(formatted_poly)
    for eigval in eigenvalues:
        print(eigval)
        print(eigenvectors[eigval][0])



def compute_matrix_addition():
    print('Performing matrix addition. Type "exit" at any time to quit')
    exit_flag = True
    while exit_flag:
        print("Input dimensions of the matricies in 'x' format (Ex: 2x3)")
        dimensions = input()
        if dimension_validation(dimensions):
            a = get_dimension_a(dimensions)
            b = get_dimension_b(dimensions)
            i = 1
            matrix_1 = []
            print("Input each row of values, separating each value with commas (Ex: 1, 2, 3, 4)")
            while i <= a:
                row = input()
                if row.replace(" ", "").lower() == "exit":
                    print('Function Cancled. Returning to matrix page')
                    exit_flag = False
                    break
                elif validate(row):
                    matrix_row = make_matrix_row(row)
                    matrix_1.append(matrix_row)
                    i = i + 1
                else:
                    print("Error. Unknown Input. Try Again.")
            if validate_matrix(matrix_1, a, b):
                print("Input each row of values for the second matrix, separating each value with commas")
                matrix_2 = []
                i = 1
                while i <= a:
                    row = input()
                    if row.replace(" ", "").lower() == "exit":
                        print('Function Cancled. Returning to matrix page')
                        exit_flag = False
                        break
                    matrix_row = make_matrix_row(row)
                    matrix_2.append(matrix_row)
                    i = i + 1
                if validate_matrix(matrix_2, a, b):
                    matrix_3 = matrix_addition(matrix_1, matrix_2)
                    print(matrix_3)
                elif exit_flag == False:
                    break
                else:
                    print("Invalid inputs. Dimensions do not match the input")
            elif exit_flag == False:
                break
            else:
                print("Invalid inputs. Dimensions do not match the input")
        elif dimensions.replace(" ", "").lower() == "exit":
            print("Returning to matrix page.")
            exit_flag = False
            break
        else:
            print('Invalid dimension input. Try again or type "exit" to quit')



def compute_matrix_subtraction():
    print('Performing matrix subtraction. Type "exit" at any time to quit')
    exit_flag = True
    while exit_flag:
        print("Input dimensions of the matricies in 'x' format (Ex: 2x3)")
        
        dimensions = input()
        if dimension_validation(dimensions):
            a = get_dimension_a(dimensions)
            b = get_dimension_b(dimensions)
            i = 1
            matrix_1 = []
            print("Input each row of values, separating each value with commas (Ex: 1, 2, 3, 4)")
            while i <= a:
                row = input()
                if row.replace(" ", "").lower() == "exit":
                    print('Function Cancled. Returning to matrix page')
                    exit_flag = False
                    break
                matrix_row = make_matrix_row(row)
                matrix_1.append(matrix_row)
                i = i + 1
            if validate_matrix(matrix_1, a, b):
                print("Input each row of values for the second matrix, separating each value with commas")
                matrix_2 = []
                i = 1
                while i <= a:
                    row = input()
                    if row.replace(" ", "").lower() == "exit":
                        print('Function Cancled. Returning to matrix page')
                        exit_flag = False
                        break
                    matrix_row = make_matrix_row(row)
                    matrix_2.append(matrix_row)
                    i = i + 1
                if validate_matrix(matrix_2, a, b):
                    matrix_3 = matrix_subtraction(matrix_1, matrix_2)
                    print(matrix_3)
                elif exit_flag == False:
                    break
                else:
                    print("Invalid inputs. Dimensions do not match the input")
            elif exit_flag == False:
                break
            else:
                print("Invalid inputs. Dimensions do not match the input")
        elif dimensions.replace(" ", "").lower() == "exit":
            print("Returning to matrix page.")
            exit_flag = False
            break
        else:
            print('Invalid dimension input. Try again or type "exit" to quit')



def compute_matrix_multiplication():
    print('Performing matrix multiplication. Type "exit" at any time to quit')
    exit_flag = True
    while exit_flag:
        print("Input dimensions of the first matrix in 'x' format (Ex: 2x3)")
        
        dimensions_1 = input()
        if dimension_validation(dimensions_1):
            a1 = get_dimension_a(dimensions_1)
            b1 = get_dimension_b(dimensions_1)
    
            print("Input dimensions of the second matrix")
            dimensions_2 = input()
            if dimension_validation(dimensions_2):
                a2 = get_dimension_a(dimensions_2)
                b2 = get_dimension_b(dimensions_2)
                if validate_multiplication_dimensions(a1, b1, a2, b2):
                    i = 1
                    matrix_1 = []
                    print("Input each row of values for the first matrix, separating each value with commas (Ex: 1, 2, 3, 4)")
                    while i <= a1:
                        row = input()
                        if row.replace(" ", "").lower() == "exit":
                            print('Function Cancled. Returning to matrix page')
                            exit_flag = False
                            break
                        matrix_row = make_matrix_row(row)
                        matrix_1.append(matrix_row)
                        i = i + 1
                    if validate_matrix(matrix_1, a1, b1):
                        print("Input each row of values for the second matrix, separating each value with commas")
                        matrix_2 = []
                        i = 1
                        while i <= a2:
                            row = input()
                            if row.replace(" ", "").lower() == "exit":
                                print('Function Cancled. Returning to matrix page')
                                exit_flag = False
                                break
                            matrix_row = make_matrix_row(row)
                            matrix_2.append(matrix_row)
                            i = i + 1
                        if validate_matrix(matrix_2, a2, b2):
                            matrix_3 = matrix_multiplication(matrix_1, matrix_2)
                            print(matrix_3)
                        elif exit_flag == False:
                            break
                        else:
                            print("Invalid input. Dimensions do not match the input")
                    elif exit_flag == False:
                        break
                    else:
                        print("Invalid inputs. Dimensions do not match the input")
                else:
                    print("Invalid dimensions for matrix multiplication")
            else:
                print('Invalid dimension input. Try again or type "exit" to quit')
        elif dimensions.replace(" ", "").lower() == "exit":
            print("Returning to matrix page.")
            exit_flag = False
            break
        else:
            print('Invalid dimension input. Try again or type "exit" to quit')



def compute_matrix_inversion():
    print('Performing matrix inversion. Type "exit" at any time to quit')
    exit_flag = True
    while exit_flag:
        print("Input dimensions of the matrix in 'x' format (Ex: 3x3)")
        
        dimensions = input()
        if dimension_validation(dimensions):
            a = get_dimension_a(dimensions)
            b = get_dimension_b(dimensions)
            
            if a == b:
                i = 1
                matrix_1 = []
                print("Input each row of values for the first matrix, separating each value with commas (Ex: 1, 2, 3, 4)")
                while i <= a:
                    row = input()
                    if row.replace(" ", "").lower() == "exit":
                        print('Function Cancled. Returning to matrix page')
                        exit_flag = False
                        break
                    matrix_row = make_matrix_row(row)
                    matrix_1.append(matrix_row)
                    i = i + 1
                if validate_matrix(matrix_1, a, b):
                    matrix_2 = matrix_inverse(matrix_1)
                    print(matrix_2)
                elif exit_flag == False:
                    break
                else:
                    print("Invalid inputs. Matrix does not match given dimensions")
            else:
                print("Invalid input. Must be a square matrix (Ex: 2x2, 3x3 . . .)")
       
        elif dimensions.replace(" ", "").lower() == "exit":
            print("Returning to matrix page.")
            exit_flag = False
            break
        else:
            print('Invalid dimension input. Try again or type "exit" to quit')



def compute_eigen():
    print('Solving for eigenvalues and characteristic equations. Type "exit" at any time to quit')
    exit_flag = True
    while exit_flag:
        print("Input dimensions of the matrix in 'x' format (Ex: 3x3)")

        dimensions_1 = input()
        if dimension_validation(dimensions_1):
            a = get_dimension_a(dimensions_1)
            b = get_dimension_b(dimensions_1)
            
            if a == b:
                i = 1
                matrix_1 = []
                print("Input each row of values for the first matrix, separating each value with commas (Ex: 1, 2, 3, 4)")
                while i <= a:
                    row = input()
                    if row.replace(" ", "").lower() == "exit":
                        print('Function Cancled. Returning to matrix page')
                        exit_flag = False
                        break
                    matrix_row = make_matrix_row(row)
                    matrix_1.append(matrix_row)
                    i = i + 1
                if validate_matrix(matrix_1, a, b):
                    eigen_profile = eigen(matrix_1)
                    print(eigen_profile)
                elif exit_flag == False:
                    break
                else:
                    print("Invalid inputs. Matrix does not match given dimensions")
            else:
                print("Invalid input. Must be a square matrix (Ex: 2x2, 3x3 . . .)")
       
        elif dimensions_1.replace(" ", "").lower() == "exit":
            print("Returning to matrix page.")
            exit_flag = False
            break
        else:
            print('Invalid dimension input. Try again or type "exit" to quit')



def help():
    print("Matrix Addition: mad")
    print("Matrix Subtraction: msb")
    print("Matrix Multiplication: mmp")
    print("Scalars of Matricies: mad")
    print("Matrix Inverses: inv")
    print("Eigen Profile: eig")



def matrix_page():    
    while True:
        print("Welcome to the Matrix Page")
        print('You can type "exit" to quit to main page or "help" for the list of usable codes')
        
        arg = input()
        arg = arg.replace(" ", "").lower()
        
        if arg == "exit":
            print("Returning to main page")
            break
        
        elif arg == "help":
            help()
    
        elif arg == "mad":
            compute_matrix_addition()
    
        elif arg == "msb":
            compute_matrix_subtraction()
    
        elif arg == "mmp":
            compute_matrix_multiplication()
        
        elif arg == "inv":
            compute_matrix_inversion()
            
        elif arg == "eig":
            compute_eigen()
