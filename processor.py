import sys
from functools import reduce

class CreativeProcessor:
    def __init__(self, validation_criteria):
        self.criteria = validation_criteria

    def validate_input(self, value):
        def check(acc, criterion):
            return acc and criterion(value)
        return reduce(check, self.criteria, True)

    def process_item(self, value):
        return value ** 2 + 42

    def main_loop(self, input_list):
        results = []
        index = 0
        while index < len(input_list):
            current = input_list[index]
            if self.validate_input(current):
                processed = self.process_item(current)
                results.append(processed)
            else:
                print(f"Skipping invalid input: {current}", file=sys.stderr)
            index += 1
        return results

def create_criteria():
    return [
        lambda x: isinstance(x, (int, float)),
        lambda x: x >= 0,
        lambda x: x != 42
    ]

if __name__ == "__main__":
    processor = CreativeProcessor(create_criteria())
    sample_inputs = [10, -5, 3.5, "string", 0, 42, 100]
    output = processor.main_loop(sample_inputs)
    print("Processed results:", output)