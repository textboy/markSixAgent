from src.utils.get_time import getTimeStamp


def get_history(hist_limit=120) -> {str, list[list[int]]}:
    history = []
    delimiter = '|'
    his_file_path = 'memory/hist_draw.txt'
    latest_draw_no = None
    with open(his_file_path, 'r') as file:
        lines = file.readlines()
        for line_num, line in enumerate(lines):
            parts = line.strip().split(delimiter)
            if len(parts) == 3:
                # locate the latest draw no from the last non-empty line
                if line_num == len(lines) - 1:
                    latest_draw_no = parts[0]
                ball_drawn_list = list(map(int, parts[2].split(',')))
                history.append(ball_drawn_list)
    print(f"[{getTimeStamp()}] The last Draw No of history memory after loading:{latest_draw_no}")
    return latest_draw_no, history[-hist_limit:]  # Return the latest hist_limit history data