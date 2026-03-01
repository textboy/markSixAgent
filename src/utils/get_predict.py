from src.utils.get_time import getTimeStamp
from datetime import datetime


def get_predict_hist() -> str:
    result = None
    delimiter = '|'
    result_file_path = f'memory/predict_result_{datetime.now().strftime("%y")}.txt'
    with open(result_file_path, 'r', encoding='utf-8') as file:
        result = file.read()
    return result