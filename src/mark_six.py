import os
from src.utils.load_history import load_history
from src.utils.get_history import get_history
from src.agents.mark_six_agent import MarkSixAgent
from src.utils.get_time import getTimeStamp
from src.utils.write_result import write_result
from src.utils.get_predict import get_predict_hist
from dotenv import load_dotenv


HIST_LIMIT = 120
load_dotenv(os.path.join('config', '.env'))
skip_load_history = os.getenv('SKIP_LOAD_HISTORY', 'False') in ['True', 'true', '1']

def main():
    # Update history data
    if not skip_load_history:
        load_history()
    
    # Predict mark six result
    latest_draw_no, hist = get_history(HIST_LIMIT)
    predict_hist = get_predict_hist()
    markSixAgent = MarkSixAgent(latest_draw_no, hist, predict_hist)
    result = markSixAgent.analyze()
    write_result(latest_draw_no, result)
    print(f"[{getTimeStamp()}] {result}")

if __name__ == "__main__":
    main()