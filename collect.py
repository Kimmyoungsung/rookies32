import requests
import pandas as pd
from datetime import datetime, timedelta
import time

API_KEY = "f62dd8580a25eac09e841266dca8ab5c"

def get_daily_boxoffice(target_date):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {'key': API_KEY, 'targetDt': target_date}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['boxOfficeResult']['dailyBoxOfficeList']
    return []

print("KOBIS 2022-2024 데이터 수집 시작...")
all_data = []
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
current_date = start_date

while current_date <= end_date:
    target_date = current_date.strftime('%Y%m%d')
    year_month = current_date.strftime('%Y-%m')
    if current_date.day == 1:
        print(f"\n수집 중: {year_month}")
    try:
        daily_data = get_daily_boxoffice(target_date)
        for movie in daily_data:
            movie['date'] = target_date
            movie['year_month'] = year_month
            all_data.append(movie)
        print(".", end="", flush=True)
        time.sleep(0.3)
    except Exception as e:
        print(f"오류: {e}")
    current_date += timedelta(days=1)

df = pd.DataFrame(all_data)
df.to_csv('data/kobis_raw_2022_2024.csv', index=False, encoding='utf-8-sig')
print(f"\n\n완료! {len(all_data)}개 데이터")
print(f"저장: data/kobis_raw_2022_2024.csv")
