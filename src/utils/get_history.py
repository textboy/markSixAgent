def get_history():
    history = []
    delimiter = '|'
    with open('memory/his_draw.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(delimiter)
            if len(parts) == 3:
                numbers = list(map(int, parts[2].split(',')))
                history.append(numbers)
    return history