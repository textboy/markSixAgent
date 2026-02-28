import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.get_history import get_history
from src.tools.analyze_tools import *


DEFAULT_MODEL_NAME = 'x-ai/grok-beta'
load_dotenv(os.path.join('config', '.env'))
HIST_LIMIT = 120
PREDICT_BALLS_NUM = 8

llm = ChatOpenAI(
    model=os.getenv('MODEL_NAME', DEFAULT_MODEL_NAME),
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url=os.getenv('OPENROUTER_BASE_URL'),
    temperature=0.1,
)

class MarkSixAgent:
    def __init__(self, hist):
        self.hist = hist

    def analyze(self) -> str:
        hot_numbers_top_5 = None
        cold_numbers_top_5 = None
        for tool in mark_six_tools:
            if tool.__name__ == 'get_hot_cold_numbers':
                hot_numbers_top_5, cold_numbers_top_5 = tool(self.hist)

        user_prompt = f"""
預測下一期六合彩號碼.
最新{HIST_LIMIT}歷史數據(最後為最新數據):{self.hist}
"""
        sys_prompt = f"""
你是一名六合彩分析師,根據歷史數據,透過以下策略進行推理分析,每種策略生成<=5個號碼,綜合後,預測下一期的六合彩號碼.返回1)前{PREDICT_BALLS_NUM}個高機率預測號碼(排序由機率高到低),並包含對應綜合機率,機率為號碼在多種策略中出現的次數/所有策略號碼總數;2)分析過程的詳細說明:
- 七星矩陣:分析歷史數據中號碼在七星矩陣/旋轉矩陣/輪次矩陣,預測下一期可能出現的號碼.
- 江恩螺旋四方形:分析歷史數據中號碼在江恩螺旋四方形中的位置,預測下一期可能出現的號碼.
- 號碼分佈:分析歷史數據中號碼的機率分佈情況,預測下一期可能出現的號碼範圍和分佈特徵.
- 單雙號碼:分析歷史數據中單數(奇數)和雙數(偶數)的分佈情況,預測下一期可能出現的單數和雙數比例.
- 連號分析:有兩個或兩個以上的數字是連續自然數,預測下一期可能出現的連號組合.
- 斜連號分析:有兩個或兩個以上的數字在歷史數據中呈斜連狀態,預測下一期可能出現的斜連號組合.
- 連莊分析:分析同一個號碼連續兩期被開出,預測下一期可能出現的連莊組合.
- 跳號分析:一個號碼在遺漏了特定期數後再次出現。不是連續出現（不是連莊），而是「跳過」了幾期才重新開出,預測下一期可能出現的跳號組合.
- 熱門號碼:根據歷史數據中出現頻率較高的號碼,這些號碼在下一期出現的機率可能較高.
- 冷門號碼:根據歷史數據中出現頻率較低的號碼,這些號碼在下一期出現的機率可能較低.
- 遺漏號碼:根據歷史數據中遺漏了較多期數的號碼,這些號碼在下一期出現的機率可能較高.
- 尾數分析:專注於號碼的個位數,預測下一期可能出現的尾數組合.
- 頭數分析:分析歷史數據中號碼的頭數特徵,預測下一期可能出現的頭數組合.
- 合數分析:分析歷史數據中號碼的合數特徵(相對質數),預測下一期可能出現的合數組合.
- 其它策略:根據歷史數據中的其他特徵和模式,預測下一期可能出現的號碼.
返回格式範例:
**result**
1(15%),2(10%),3(8%),4(8%),5(4.3%),6(0.2%),7(0.1%),8(0.1%)
**reasoning procedure**
...
"""
        messages = [
            SystemMessage(content=sys_prompt),
            HumanMessage(content=user_prompt)
        ]
        return llm.invoke(messages).content

if __name__ == "__main__":
    hist = get_history(HIST_LIMIT)
    markSixAgent = MarkSixAgent(hist)
    result = markSixAgent.analyze()
    print(f"{result}")