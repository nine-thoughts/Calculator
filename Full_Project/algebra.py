import numpy as np
import math
import re
from sympy import symbols, Eq, solve, sympify


class Algebra:
    def __init__(self):
        # Initialize attributes like operation history
        self.history = []

    def process_expression(self, expression):
        # Add '*' between numbers and variables (e.g., "2x" -> "2*x")
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        return expression

    def solve_linear_system(self, equation_str):
        # Define the variable (e.g., x)
        x = symbols('x')
        equation_str = self.process_expression(equation_str)
        # Split the input string into left-hand side (LHS) and right-hand side (RHS)
        if "=" not in equation_str:
            raise ValueError("The input must contain an '=' sign to form an equation.")
        lhs, rhs = equation_str.split("=")
        
        # Convert LHS and RHS into SymPy expressions
        lhs = sympify(lhs.strip())
        rhs = sympify(rhs.strip())
        
        # Create the equation using Eq
        equation = Eq(lhs, rhs)
        print(f"Parsed Equation: {equation}")
        
        # Solve the equation
        solution = solve(equation, x)
        return solution



    def find_vertex(self, equation):
        # Define the variable
        x = symbols('x')
        equation = self.process_expression(equation)

    
        # Preprocess the equation (this step depends on your implementation)
        lhs, rhs = equation.split("=")
        lhs = sympify(lhs.strip())
        rhs = sympify(rhs.strip())
    
        # Form the equation in standard form
        standard_eq = Eq(lhs - rhs, 0)
    
        # Use the left-hand side of the equation to extract coefficients
        lhs_expr = standard_eq.lhs
        a = lhs_expr.coeff(x**2)
        b = lhs_expr.coeff(x)
        c = lhs_expr.subs(x, 0)
    
        # Calculate the vertex
        x_vertex = -b / (2 * a)
        y_vertex = a * (x_vertex ** 2) + b * x_vertex + c
    
        return (x_vertex, y_vertex)



    def find_axis_intersections(a, b, c):
        """
        Find the x-axis and y-axis intersections for y = ax^2 + bx + c.

        Parameters:
            a (float): Coefficient of x^2.
            b (float): Coefficient of x.
            c (float): Constant term.

        Returns:
            dict: X-axis roots and Y-axis intersection.
        """
        intersections = {}

        # X-axis roots
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            intersections['x_axis'] = (root1, root2)
        else:
            intersections['x_axis'] = None  # No real roots

        # Y-axis intersection
        intersections['y_axis'] = c

        return intersections
    


    def solve_inequality(self, inequality_str):
        """
        Solve inequality equations given as a string.
    
        Parameters:
        inequality_str (str): The inequality equation as a string (e.g., "5x-3 < 6x-9")
    
        Returns:
        str: Solution of the inequality
        """
        # Define the variable
        x = symbols('x')
        inequality_str = self.process_expression(inequality_str)
    
        # Preprocess the input to standardize operators (e.g., implicit multiplication)
        inequality_str = inequality_str.replace("^", "**")  # Replace ^ with ** for exponents
    
        # Detect inequality operators and split into left-hand side and right-hand side
        if "<" in inequality_str:
            lhs, rhs = inequality_str.split("<")
            operator = "<"
        elif ">" in inequality_str:
            lhs, rhs = inequality_str.split(">")
            operator = ">"
        elif "<=" in inequality_str:
            lhs, rhs = inequality_str.split("<=")
            operator = "<="
        elif ">=" in inequality_str:
            lhs, rhs = inequality_str.split(">=")
            operator = ">="
        else:
            raise ValueError("Invalid inequality operator in the input.")
    
        # Convert LHS and RHS to SymPy expressions
        lhs = sympify(lhs.strip())
        rhs = sympify(rhs.strip())
    
        # Rearrange inequality to standard form: lhs - rhs < 0 (or similar)
        inequality_expr = lhs - rhs
    
        # Solve the inequality
        solution = solve(inequality_expr, x, relational=True)
        
        return str(solution)


    def _solve_linear_inequality(self, b, c, inequality):
        """
        Solve a linear inequality of the form bx + c [inequality] 0.

        Parameters:
            b (float): Coefficient of x.
            c (float): Constant term.
            inequality (str): The inequality operator.

        Returns:
            str: Solution to the inequality.
        """
        if b == 0:
            # Handle special case where b = 0
            if inequality in ['<', '<=']:
                return "No solution" if c > 0 else "All real numbers"
            elif inequality in ['>', '>=']:
                return "All real numbers" if c < 0 else "No solution"
    
        # Solve bx + c [inequality] 0
        solution = -c / b
        if b > 0:
            if inequality == '<':
                return f"x < {solution}"
            elif inequality == '<=':
                return f"x ≤ {solution}"
            elif inequality == '>':
                return f"x > {solution}"
            elif inequality == '>=':
                return f"x ≥ {solution}"
        else:
            # Reverse the inequality if b < 0
            if inequality == '<':
                return f"x > {solution}"
            elif inequality == '<=':
                return f"x ≥ {solution}"
            elif inequality == '>':
                return f"x < {solution}"
            elif inequality == '>=':
                return f"x ≤ {solution}"

    
    def _solve_quadratic_inequality(self, a, b, c, inequality):
        """
        Solve a quadratic inequality.

        Parameters:
            a (float): Coefficient of x^2.
            b (float): Coefficient of x.
            c (float): Constant term.
            inequality (str): The inequality operator.

        Returns:
            str: Solution to the inequality.
        """
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return "No real solutions" if inequality in ['<', '<='] else "All real numbers"

        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        roots = sorted([root1, root2])

        if a > 0:
            if inequality in ['<', '<=']:
                return f"x in ({roots[0]}, {roots[1]})"
            else:
                return f"x in (-inf, {roots[0]}] U [{roots[1]}, inf)"
        else:
            if inequality in ['<', '<=']:
                return f"x in (-inf, {roots[0]}] U [{roots[1]}, inf)"
            else:
                return f"x in ({roots[0]}, {roots[1]})"




alg = Algebra()

def parse_equation(equation):
    # Separate left-hand side and right-hand side
    sides = equation.split('=')
    lhs = sides[0].strip()
    rhs = sides[1].strip()

    # Extract coefficients using regex
    variables = re.findall(r'([+-]?\d*\.?\d+|[+-]?[a-zA-Z])([a-zA-Z])?', lhs)
    coefficients = []
    for term in variables:
        if term[0].isalpha() or term[0] in ('+', '-'):  # Handle cases like "x", "-y"
            coeff = term[0] + "1"  # Add default coefficient of 1
        else:
            coeff = term[0]  # Extract numerical coefficient
        coefficients.append(float(coeff))

    return np.array(coefficients), rhs


def solve_linear_system(equation):
    coefficients, constant = parse_equation(equation)
    return alg.solve_linear_system(coefficients, constant)



















# import numpy as np
# import math



# def solve_linear_system(self, coefficients, constants):
#     """
#     Solve a system of linear equations Ax = B using matrices.

#     Parameters:
#         coefficients (list[list[float]]): Coefficient matrix (A).
#         constants (list[float]): Constants vector (B).

#     Returns:
#         list[float]: Solution vector (x) or None if no solution exists.
#     """
#     try:
#         A = np.array(coefficients)
#         B = np.array(constants)
#         solution = np.linalg.solve(A, B)
#         self.history.append({
#             "operation": "linear_system",
#             "input": {"coefficients": coefficients, "constants": constants},
#             "output": solution.tolist()
#         })
#         return solution.tolist()
#     except np.linalg.LinAlgError:
#         return 'None: No Unique solution exists'  # No unique solution exists

# def find_vertex(a, b, c):
#     """
#     Find the vertex of a parabola given by y = ax^2 + bx + c.

#     Parameters:
#         a (float): Coefficient of x^2.
#         b (float): Coefficient of x.
#         c (float): Constant term.

#     Returns:
#         tuple: Coordinates of the vertex (x, y).
#     """
#     x = -b / (2 * a)
#     y = a * x**2 + b * x + c
#     return (x, y)


#     def get_history(self):
#         """Retrieve the history of operations."""
#         return self.history
    
    
# def find_axis_intersections(a, b, c):
#     """
#     Find the x-axis and y-axis intersections for y = ax^2 + bx + c.

#     Parameters:
#         a (float): Coefficient of x^2.
#         b (float): Coefficient of x.
#         c (float): Constant term.

#     Returns:
#         dict: X-axis roots and Y-axis intersection.
#     """
#     intersections = {}

#     # X-axis roots
#     discriminant = b**2 - 4*a*c
#     if discriminant >= 0:
#         root1 = (-b + math.sqrt(discriminant)) / (2 * a)
#         root2 = (-b - math.sqrt(discriminant)) / (2 * a)
#         intersections['x_axis'] = (root1, root2)
#     else:
#         intersections['x_axis'] = None  # No real roots

#     # Y-axis intersection
#     intersections['y_axis'] = c

#     return intersections


# def solve_inequality(self, a, b, c, inequality):
#     """
#     Solve a linear or quadratic inequality.

#     Parameters:
#         a (float): Coefficient of x^2.
#         b (float): Coefficient of x.
#         c (float): Constant term.
#         inequality (str): The inequality operator ('<', '<=', '>', '>=').

#     Returns:
#         str: Description of the solution interval(s).
#     """
#     if inequality not in ['<', '<=', '>', '>=']:
#         raise ValueError("Invalid inequality operator")

#     if a == 0:
#         # Linear inequality
#         return self._solve_linear_inequality(b, c, inequality)
#     else:
#         # Quadratic inequality
#         return self._solve_quadratic_inequality(a, b, c, inequality)

# def _solve_linear_inequality(self, b, c, inequality):
#     """
#     Solve a linear inequality of the form bx + c [inequality] 0.

#     Parameters:
#         b (float): Coefficient of x.
#         c (float): Constant term.
#         inequality (str): The inequality operator.

#     Returns:
#         str: Solution to the inequality.
#     """
#     if b == 0:
#         # Handle special case where b = 0
#         if inequality in ['<', '<=']:
#             return "No solution" if c > 0 else "All real numbers"
#         elif inequality in ['>', '>=']:
#             return "All real numbers" if c < 0 else "No solution"

#     # Solve bx + c [inequality] 0
#     solution = -c / b
#     if b > 0:
#         if inequality == '<':
#             return f"x < {solution}"
#         elif inequality == '<=':
#             return f"x ≤ {solution}"
#         elif inequality == '>':
#             return f"x > {solution}"
#         elif inequality == '>=':
#             return f"x ≥ {solution}"
#     else:
#         # Reverse the inequality if b < 0
#         if inequality == '<':
#             return f"x > {solution}"
#         elif inequality == '<=':
#             return f"x ≥ {solution}"
#         elif inequality == '>':
#             return f"x < {solution}"
#         elif inequality == '>=':
#             return f"x ≤ {solution}"

# def _solve_quadratic_inequality(self, a, b, c, inequality):
#     discriminant = b**2 - 4*a*c
#     if discriminant < 0:
#         return "No real solutions" if inequality in ['<', '<='] else "All real numbers"

#     root1 = (-b + math.sqrt(discriminant)) / (2 * a)
#     root2 = (-b - math.sqrt(discriminant)) / (2 * a)
#     roots = sorted([root1, root2])

#     if a > 0:
#         if inequality in ['<', '<=']:
#             return f"x in ({roots[0]}, {roots[1]})"
#         else:
#             return f"x in (-inf, {roots[0]}] U [{roots[1]}, inf)"
#     else:
#         if inequality in ['<', '<=']:
#             return f"x in (-inf, {roots[0]}] U [{roots[1]}, inf)"
#         else:
#             return f"x in ({roots[0]}, {roots[1]})"
