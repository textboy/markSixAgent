import requests
from bs4 import BeautifulSoup

def get_mark_six_results():
    url = "https://lottery.hk/en/mark-six/results/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate the results table
    table = soup.find('table', class_='results-table')
    results = []

    # Iterate through each row in the table body
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        
        # Skip rows that don't have enough columns (like monthly headers)
        if len(cells) < 3:
            continue
            
        # Extract specific column values
        draw_date = cells[0].get_text(strip=True)
        draw_number = cells[1].get_text(strip=True)
        
        # Extract balls drawn (often inside a nested list or specific class)
        balls_drawn = [ball.get_text(strip=True) for ball in cells[2].find_all('li')]
        
        results.append({
            "Draw Date": draw_date,
            "Draw Number": draw_number,
            "Balls Drawn": balls_drawn
        })
        
    return results

# Execute and print first 5 records
data = get_mark_six_results()
for entry in data[:5]:
    print(entry)
