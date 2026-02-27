class MarkSix:
    def __init__(self):
        self.history = self.load_history()

    def load_history(self):
        history = []
        delimiter = '|'
        with open('memory/his_draw.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(delimiter)
                if len(parts) == 3:
                    numbers = list(map(int, parts[2].split(',')))
                    history.append(numbers)
        return history

    def analyze_freqency(self):
        frequency = {}
        for numbers in self.history:
            for num in numbers:
                if num in frequency:
                    frequency[num] += 1
                else:
                    frequency[num] = 1
        return frequency

    def predict_hot_cold_numbers(self):
        frequency = self.analyze_freqency()
        sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        hot_numbers_top_5 = [num for num, _ in sorted_frequency[:5]]
        cold_numbers_top_5 = [num for num, _ in sorted_frequency[-5:]]
        return hot_numbers_top_5, cold_numbers_top_5

    def run(self):
        predictions = self.predict_numbers()
        print("Predicted numbers:", predictions)
