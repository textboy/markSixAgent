from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from src.utils.get_time import getTimeStamp
import time


url = "https://lottery.hk/en/mark-six/results/"
his_file_path = 'memory/hist_draw.txt'
delimiter = '|'


def load_history():
    start_time = time.time()
    print(f"[{getTimeStamp()}] Start loading MarkSix history data...")

    last_draw_no = None
    with open(his_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            for i in range(-1, -11, -1):
                # bypass the empty lines at the end of file if exist
                if lines[i].strip():
                    last_line = lines[i].strip()
                    break
            last_draw_no = last_line.split(delimiter)[0]
            print(f"[{getTimeStamp()}] The last Draw No of history memory is: {last_draw_no}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.page_load_strategy = 'eager'
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; U; Android 14; en-US; Infinix X6853 Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.6.2.1316 Mobile Safari/537.36")
    # Disable images (1=Allow, 2=Block)
    options.set_preference("permissions.default.image", 2)
    cache_manager = DriverCacheManager(valid_range=30)
    service = Service(GeckoDriverManager(cache_manager=cache_manager).install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)

    try:
        driver.get(url)
        # print(f"[{getTimeStamp()}] DEBUG homepage is loaded")
    except TimeoutException:
        print(f"[{getTimeStamp()}] ERROR: loading too long and continue the following processing")
    except WebDriverException as e:
        print(f"[{getTimeStamp()}] ERROR: {e}")

    draws = []
    sorted_draws = []
    wait = WebDriverWait(driver, 2)
    # locate the table
    result_tbl_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_results")))
    if len(result_tbl_list) == 1:
        result_body_list = result_tbl_list[0].find_elements(By.XPATH, "./tbody")
        if len(result_body_list) == 1:
            # locate the rows
            result_tr_list = result_body_list[0].find_elements(By.XPATH, "./tr")
            for result_tr in result_tr_list:
                # locate the columns
                result_td_list = result_tr.find_elements(By.XPATH, "./td")
                # print(f"DEBUG length of result_td_list: {len(result_td_list)}")
                if len(result_td_list) == 4:
                    draw_no = result_td_list[0].text
                    draw_dt = result_td_list[1].text
                    ball_drawn_list = []
                    ball_drawn_li_list = result_td_list[2].find_elements(By.XPATH, "./ul/li")
                    # print(f"DEBUG length of ball_drawn_li_list: {len(ball_drawn_li_list)}")
                    for ball_drawn_li in ball_drawn_li_list:
                        ball_drawn = ball_drawn_li.text
                        ball_drawn_list.append(ball_drawn)
                    if last_draw_no is None or (draw_no > last_draw_no):
                        print(f"[{getTimeStamp()}] Draw No: {draw_no}, Draw Date: {draw_dt}, Ball: {ball_drawn_list}")
                        draws.append({"draw_no": draw_no, "draw_dt": draw_dt, "ball_drawn_list": ball_drawn_list})
                    else:
                        break

    # Write accumulated draws to file
    if len(draws) > 0:
        # sort the draws by draw_no in ascending order before writing to file
        sorted_draws = sorted(draws, key=lambda x: x['draw_no'])
        with open(his_file_path, 'a', encoding='utf-8') as f:
            for draw in sorted_draws:
                balls_str = ','.join(draw['ball_drawn_list'])
                f.write(f"{draw['draw_no']}{delimiter}{draw['draw_dt']}{delimiter}{balls_str}\n")
            print(f"[{getTimeStamp()}] Insert {len(draws)} historical draws to memory/his_draw.txt")

    driver.quit()
    end_time = time.time()
    print(f"[{getTimeStamp()}] Loading end, elapsed time: {(end_time-start_time)/60:.1f} minutes.")