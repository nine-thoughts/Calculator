import numpy as np
import math

class Algebra:
    def __init__(self):
        self.history = []

    def find_vertex(self, a, b, c, power=2):
        if power != 2:
            return "Vertex method currently supports only quadratic (power=2) equations."
        x = -b / (2 * a)
        y = a * x**2 + b * x + c
        return (x, y)

    def find_axis_intersections(self, a, b, c, power=2):
        intersections = {}
        if power != 2:
            return {
                'x_axis': "Not supported for non-quadratic powers",
                'y_axis': c
            }
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            intersections['x_axis'] = (root1, root2)
        else:
            intersections['x_axis'] = None
        intersections['y_axis'] = c
        return intersections

    def solve_linear_system(self, coefficients, constants):
        try:
            A = np.array(coefficients)
            B = np.array(constants)
            solution = np.linalg.solve(A, B)
            self.history.append({
                "operation": "linear_system",
                "input": {"coefficients": coefficients, "constants": constants},
                "output": solution.tolist()
            })
            return solution.tolist()
        except np.linalg.LinAlgError:
            return 'None: No Unique solution exists'

    def _solve_linear_inequality(self, b, c, op):
        if b == 0:
            if op in ['<', '<=']:
                return "No solution" if c > 0 else "All real numbers"
            elif op in ['>', '>=']:
                return "All real numbers" if c < 0 else "No solution"

        solution = -c / b
        if b > 0:
            if op == '<': return f"x < {solution}"
            if op == '<=': return f"x ≤ {solution}"
            if op == '>': return f"x > {solution}"
            if op == '>=': return f"x ≥ {solution}"
        else:
            if op == '<': return f"x > {solution}"
            if op == '<=': return f"x ≥ {solution}"
            if op == '>': return f"x < {solution}"
            if op == '>=': return f"x ≤ {solution}"

        return "Invalid inequality"
