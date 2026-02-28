def analyze_freqency(hist):
    frequency = {}
    for numbers in hist:
        for num in numbers:
            if num in frequency:
                frequency[num] += 1
            else:
                frequency[num] = 1
    return frequency

def get_hot_cold_numbers(hist):
    frequency = analyze_freqency(hist)
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    hot_numbers_top_5 = [num for num, _ in sorted_frequency[:5]]
    cold_numbers_top_5 = [num for num, _ in sorted_frequency[-5:]]
    if hot_numbers_top_5 is None or cold_numbers_top_5 is None:
        return "ERROR: Could not get hot/cold numbers"
    return hot_numbers_top_5, cold_numbers_top_5

# List of tools for analysts
mark_six_tools = [get_hot_cold_numbers]