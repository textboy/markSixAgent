from src.utils.load_history import load_history
from src.utils.get_history import get_history
from src.agents.mark_six_agent import MarkSixAgent
from src.utils.get_time import getTimeStamp


HIST_LIMIT = 120

def main():
    # Update history data
    load_history()
    
    # Predict mark six result
    hist = get_history(HIST_LIMIT)
    markSixAgent = MarkSixAgent(hist)
    result = markSixAgent.analyze()
    print(f"[{getTimeStamp()}] {result}")

if __name__ == "__main__":
    main()