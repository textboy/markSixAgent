def get_history(hist_limit=120) -> list[list[int]]:
    history = []
    delimiter = '|'
    his_file_path = 'memory/hist_draw.txt'
    with open(his_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(delimiter)
            if len(parts) == 3:
                numbers = list(map(int, parts[2].split(',')))
                history.append(numbers)
    return history[-hist_limit:]  # Return the latest hist_limit history data