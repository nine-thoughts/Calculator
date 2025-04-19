import math
import statistics
from collections import Counter
from typing import List

class Statistics:
    def __init__(self):
        self.history = []

    def record(self, operation, input_data, result):
        self.history.append({
            "operation": operation,
            "input": input_data,
            "result": result
        })

    def get_history(self):
        return self.history

    
    def mean(self, data):
        return sum(data) / len(data)
    
    def median(self, data):
        data.sort()
        n = len(data)
        if n % 2 == 0:
            return (data[n // 2 - 1] + data[n // 2]) / 2
        else:
            return data[n // 2]
    
    def average(self, data: List[float]):
        result = sum(data) / len(data)
        self.record("average", data, result)
        return result

    def median(self, data: List[float]):
        result = statistics.median(data)
        self.record("median", data, result)
        return result

    def mode(self, data: List[float]):
        try:
            result = statistics.mode(data)
        except statistics.StatisticsError:
            result = "No unique mode"
        self.record("mode", data, result)
        return result

    def moment(self, data: List[float], order: int):
        mean = self.average(data)
        result = sum((x - mean) ** order for x in data) / len(data)
        self.record(f"{order}th moment", data, result)
        return result

    def standard_deviation(self, data: List[float]):
        result = statistics.stdev(data)
        self.record("standard deviation", data, result)
        return result

    def variance(self, data: List[float]):
        result = statistics.variance(data)
        self.record("variance", data, result)
        return result

    def z_score(self, data: List[float]):
        mean = self.average(data)
        std_dev = self.standard_deviation(data)
        if std_dev == 0:
            result = [0 for _ in data]
        else:
            result = [(x - mean) / std_dev for x in data]
        self.record("z-scores", data, result)
        return result

    def permutations(self, n: int, r: int):
        result = math.factorial(n) // math.factorial(n - r)
        self.record("permutations", (n, r), result)
        return result

    def combinations(self, n: int, r: int):
        result = math.comb(n, r)
        self.record("combinations", (n, r), result)
        return result
    
    def expected_value(self, data: List[float]):
        probabilities = [1/len(data) for _ in data]  # Equal probability assumption
        result = sum(x * p for x, p in zip(data, probabilities))
        self.record("expected value", data, result)
        return result
