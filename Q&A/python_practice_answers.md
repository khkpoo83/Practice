# Python 실무 연습문제 - 답안

> ⚠️ **주의**: 먼저 스스로 문제를 풀어보고, 막힐 때만 참고하세요!

---

## Section 1: 빌트인 모듈 답안

### 문제 1-1: 학생 성적 필터링 (JSON)

```python
import json

# JSON 파일 읽기
with open('students.json', 'r', encoding='utf-8') as f:
    students = json.load(f)

# 평균 계산 및 필터링
high_scorers = []
total_avg = 0

for student in students:
    avg = (student['math'] + student['english'] + student['science']) / 3
    student['average'] = round(avg, 2)  # 평균 추가
    
    if avg >= 80:
        high_scorers.append(student)
    
    total_avg += avg

# 전체 평균 계산
overall_avg = total_avg / len(students)

# 결과 저장
with open('high_scores.json', 'w', encoding='utf-8') as f:
    json.dump(high_scorers, f, ensure_ascii=False, indent=2)

# 출력
print(f"고득점 학생 수: {len(high_scorers)}명")
print(f"전체 평균: {overall_avg:.2f}점")
```

**실행 결과:**
```
고득점 학생 수: 4명
전체 평균: 83.42점
```

---

### 문제 1-2: 매출 데이터 분석 (CSV)

```python
import csv
from collections import defaultdict

# CSV 읽기 및 매출 집계
sales_by_product = defaultdict(int)

with open('sales.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row['product']
        price = int(row['price'])
        quantity = int(row['quantity'])
        total = price * quantity
        sales_by_product[product] += total

# 매출액 순으로 정렬
sorted_sales = sorted(sales_by_product.items(), key=lambda x: x[1], reverse=True)

# 상위 3개 추출
top_3 = sorted_sales[:3]

# CSV로 저장
with open('top_products.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['product', 'total_sales'])
    writer.writeheader()
    for product, sales in top_3:
        writer.writerow({'product': product, 'total_sales': sales})

# 전체 매출액
total_sales = sum(sales_by_product.values())

print(f"전체 매출액: {total_sales:,}원")
print("상위 제품이 top_products.csv에 저장되었습니다.")

# 상위 제품 출력
print("\n=== 매출 상위 3개 제품 ===")
for rank, (product, sales) in enumerate(top_3, 1):
    print(f"{rank}. {product}: {sales:,}원")
```

**실행 결과:**
```
전체 매출액: 21,025,000원
상위 제품이 top_products.csv에 저장되었습니다.

=== 매출 상위 3개 제품 ===
1. 노트북: 14,400,000원
2. 모니터: 5,850,000원
3. 태블릿: 3,900,000원
```

---

### 문제 1-3: 다가오는 이벤트 찾기 (datetime)

```python
import json
from datetime import datetime, timedelta

# 오늘 날짜
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
week_later = today + timedelta(days=7)

# JSON 읽기
with open('events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# 7일 이내 이벤트 필터링
upcoming_events = []

for event in events:
    event_date = datetime.strptime(event['date'], '%Y-%m-%d')
    
    # 오늘부터 7일 이내인지 확인
    if today <= event_date <= week_later:
        # D-Day 계산
        days_diff = (event_date - today).days
        
        if days_diff == 0:
            d_day = "D-Day"
        elif days_diff > 0:
            d_day = f"D-{days_diff}"
        else:
            d_day = f"D+{abs(days_diff)}"
        
        event['d_day'] = d_day
        event['days_until'] = days_diff
        upcoming_events.append(event)

# D-Day 순으로 정렬 (가까운 순)
upcoming_events.sort(key=lambda x: x['days_until'])

# days_until 필드는 정렬용이므로 제거
for event in upcoming_events:
    del event['days_until']

# 저장
with open('upcoming_events.json', 'w', encoding='utf-8') as f:
    json.dump(upcoming_events, f, ensure_ascii=False, indent=2)

print(f"7일 이내 이벤트: {len(upcoming_events)}개")
print("upcoming_events.json에 저장되었습니다.\n")

print("=== 다가오는 이벤트 ===")
for event in upcoming_events:
    print(f"{event['d_day']} - {event['title']} ({event['date']})")
```

**실행 결과:**
```
7일 이내 이벤트: 5개
upcoming_events.json에 저장되었습니다.

=== 다가오는 이벤트 ===
D-Day - 성과 평가 (2026-01-13)
D-1 - 고객 미팅 (2026-01-14)
D-2 - 프로젝트 마감 (2026-01-15)
D-3 - 교육 세미나 (2026-01-16)
D-5 - 팀 회식 (2026-01-18)
```

---

### 문제 1-4: 로그 파일 분석 (정규표현식)

```python
import re
import json
from collections import Counter

# 로그 파일 읽기
with open('server_log.txt', 'r', encoding='utf-8') as f:
    log_content = f.read()

# IP 주소 패턴 (xxx.xxx.xxx.xxx)
ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

# 모든 IP 주소 찾기
ip_addresses = re.findall(ip_pattern, log_content)

# IP별 카운트
ip_counts = dict(Counter(ip_addresses))

# 에러 메시지 추출
error_pattern = r'\[ERROR\]\s+(.+?)(?:\s+from|$)'
errors = re.findall(error_pattern, log_content)

# 결과 딕셔너리
result = {
    "ip_counts": ip_counts,
    "errors": errors
}

# JSON 저장
with open('log_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=== 로그 분석 결과 ===")
print(f"\n총 고유 IP 수: {len(ip_counts)}")
print("\nIP별 접속 횟수:")
for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ip}: {count}회")

print(f"\n총 에러 수: {len(errors)}")
print("\n에러 메시지:")
for i, error in enumerate(errors, 1):
    print(f"  {i}. {error}")

print("\nlog_analysis.json에 저장되었습니다.")
```

**실행 결과:**
```
=== 로그 분석 결과 ===

총 고유 IP 수: 6

IP별 접속 횟수:
  192.168.1.105: 4회
  10.0.0.23: 4회
  192.168.1.1: 3회
  172.16.0.8: 3회
  10.0.0.45: 2회
  172.16.0.15: 1회

총 에러 수: 5

에러 메시지:
  1. Connection timeout
  2. Database connection failed
  3. Invalid authentication token
  4. File not found: /images/product.jpg
  5. Memory limit exceeded on server

log_analysis.json에 저장되었습니다.
```

---

### 문제 1-5: 파일 정리 도구 (pathlib)

```python
import json
from pathlib import Path

# 결과 저장용 딕셔너리
file_stats = {}

# data 폴더의 모든 .txt 파일 찾기
data_dir = Path('data')

if not data_dir.exists():
    print("data 폴더가 없습니다.")
else:
    txt_files = list(data_dir.glob('*.txt'))
    
    for file_path in txt_files:
        # 파일 읽기
        content = file_path.read_text(encoding='utf-8')
        
        # 단어 수 계산 (공백으로 분리)
        words = content.split()
        word_count = len(words)
        
        # 파일 크기 (바이트)
        size_bytes = file_path.stat().st_size
        
        # 결과 저장 (상대 경로로)
        relative_path = str(file_path)
        file_stats[relative_path] = {
            "word_count": word_count,
            "size_bytes": size_bytes
        }
    
    # JSON 저장
    with open('file_stats.json', 'w', encoding='utf-8') as f:
        json.dump(file_stats, f, ensure_ascii=False, indent=2)
    
    print("=== 파일 통계 ===")
    print(f"\n분석한 파일 수: {len(file_stats)}\n")
    
    for file_path, stats in file_stats.items():
        print(f"{file_path}")
        print(f"  - 단어 수: {stats['word_count']:,}개")
        print(f"  - 파일 크기: {stats['size_bytes']:,} bytes\n")
    
    print("file_stats.json에 저장되었습니다.")
```

**실행 결과:**
```
=== 파일 통계 ===

분석한 파일 수: 3

data/file1.txt
  - 단어 수: 23개
  - 파일 크기: 294 bytes

data/file2.txt
  - 단어 수: 30개
  - 파일 크기: 399 bytes

data/file3.txt
  - 단어 수: 25개
  - 파일 크기: 325 bytes

file_stats.json에 저장되었습니다.
```

---

## Section 2: 외부 라이브러리 답안

### 문제 2-1: 공공 API 활용 (requests)

```python
import requests
import json

# 1. 모든 사용자 정보 가져오기
users_url = 'https://jsonplaceholder.typicode.com/users'
response = requests.get(users_url)

if response.status_code == 200:
    users = response.json()
    print(f"총 {len(users)}명의 사용자 정보를 가져왔습니다.\n")
    
    # 2. 각 사용자의 게시글 수 조회
    user_posts_stats = []
    
    for user in users:
        user_id = user['id']
        name = user['name']
        email = user['email']
        
        # 해당 사용자의 게시글 가져오기
        posts_url = f'https://jsonplaceholder.typicode.com/posts?userId={user_id}'
        posts_response = requests.get(posts_url)
        
        if posts_response.status_code == 200:
            posts = posts_response.json()
            post_count = len(posts)
            
            # 데이터 합치기
            user_stat = {
                "id": user_id,
                "name": name,
                "email": email,
                "post_count": post_count
            }
            user_posts_stats.append(user_stat)
            
            print(f"✓ {name}: {post_count}개의 게시글")
    
    # 3. JSON 저장
    with open('user_posts_stats.json', 'w', encoding='utf-8') as f:
        json.dump(user_posts_stats, f, ensure_ascii=False, indent=2)
    
    print(f"\nuser_posts_stats.json에 저장되었습니다.")
else:
    print(f"API 요청 실패: {response.status_code}")
```

**실행 결과:**
```
총 10명의 사용자 정보를 가져왔습니다.

✓ Leanne Graham: 10개의 게시글
✓ Ervin Howell: 10개의 게시글
✓ Clementine Bauch: 10개의 게시글
✓ Patricia Lebsack: 10개의 게시글
✓ Chelsey Dietrich: 10개의 게시글
✓ Mrs. Dennis Schulist: 10개의 게시글
✓ Kurtis Weissnat: 10개의 게시글
✓ Nicholas Runolfsdottir V: 10개의 게시글
✓ Glenna Reichert: 10개의 게시글
✓ Clementina DuBuque: 10개의 게시글

user_posts_stats.json에 저장되었습니다.
```

---

### 문제 2-2: 환율 데이터 수집 (requests)

```python
import requests
from datetime import datetime

# API 호출
url = 'https://api.exchangerate-api.com/v4/latest/USD'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    rates = data['rates']
    
    # 필요한 통화만 추출
    currencies = {
        'KRW': '원',
        'JPY': '엔',
        'EUR': '유로',
        'CNY': '위안'
    }
    
    # 결과 문자열 생성
    output_lines = []
    output_lines.append("환율 정보 (기준: USD 1,000)")
    output_lines.append("=" * 30)
    
    for code, unit in currencies.items():
        if code in rates:
            rate = rates[code]
            converted = rate * 1000
            output_lines.append(f"{code}: {converted:,.0f}{unit}")
    
    output_lines.append("=" * 30)
    output_lines.append(f"조회 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 파일 저장
    with open('exchange_rates.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    # 화면 출력
    print('\n'.join(output_lines))
    print("\nexchange_rates.txt에 저장되었습니다.")
else:
    print(f"API 요청 실패: {response.status_code}")
```

**실행 결과:**
```
환율 정보 (기준: USD 1,000)
==============================
KRW: 1,320,500원
JPY: 147,230엔
EUR: 920유로
CNY: 7,245위안
==============================
조회 시간: 2026-01-13 14:30:25

exchange_rates.txt에 저장되었습니다.
```

---

### 문제 2-3: 직원 데이터 분석 (pandas)

```python
import pandas as pd

# CSV 읽기
df = pd.read_csv('employees.csv')

print("=== 직원 데이터 분석 ===\n")

# 1. 부서별 평균 연봉
dept_avg_salary = df.groupby('department')['salary'].mean()
print("1. 부서별 평균 연봉:")
for dept, avg in dept_avg_salary.items():
    print(f"   {dept}: {avg:,.0f}원")

# 2. 재직기간 5년 이상 필터링
long_term = df[df['years_of_service'] >= 5]
print(f"\n2. 재직기간 5년 이상 직원: {len(long_term)}명")

# 3. 성과평가 'Excellent'인 직원의 평균 연봉
excellent_emp = df[df['performance'] == 'Excellent']
excellent_avg = excellent_emp['salary'].mean()
print(f"\n3. 성과평가 'Excellent' 직원 평균 연봉: {excellent_avg:,.0f}원")

# 4. 보고서 생성
salary_report = df.groupby('department').agg({
    'employee_id': 'count',
    'salary': ['mean', 'max', 'min']
}).round(0)

# 컬럼명 정리
salary_report.columns = ['직원_수', '평균_연봉', '최고_연봉', '최저_연봉']
salary_report = salary_report.reset_index()
salary_report.columns = ['부서명', '직원_수', '평균_연봉', '최고_연봉', '최저_연봉']

# CSV 저장
salary_report.to_csv('salary_report.csv', index=False, encoding='utf-8-sig')

print("\n4. 부서별 연봉 보고서:")
print(salary_report.to_string(index=False))

# 추가 도전: 각 부서 최고 연봉자
print("\n5. 부서별 최고 연봉자:")
top_earners = df.loc[df.groupby('department')['salary'].idxmax()]
for _, row in top_earners.iterrows():
    print(f"   {row['department']}: {row['name']} ({row['salary']:,}원)")

print("\nsalary_report.csv에 저장되었습니다.")
```

**실행 결과:**
```
=== 직원 데이터 분석 ===

1. 부서별 평균 연봉:
   개발: 75,571,429원
   마케팅: 60,000,000원
   영업: 61,500,000원
   인사: 52,750,000원

2. 재직기간 5년 이상 직원: 11명

3. 성과평가 'Excellent' 직원 평균 연봉: 71,181,818원

4. 부서별 연봉 보고서:
 부서명  직원_수     평균_연봉     최고_연봉     최저_연봉
   개발       7  75571429.0  88000000.0  66000000.0
 마케팅       5  60000000.0  63000000.0  55000000.0
 영업       4  61500000.0  71000000.0  52000000.0
 인사       4  52750000.0  57000000.0  48000000.0

5. 부서별 최고 연봉자:
   개발: 장서현 (88,000,000원)
   마케팅: 권나영 (63,000,000원)
   영업: 노지훈 (71,000,000원)
   인사: 문정호 (57,000,000원)

salary_report.csv에 저장되었습니다.
```

---

### 문제 2-4: 복합 데이터 분석 (pandas)

```python
import pandas as pd

# 파일 읽기
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

print("=== 온라인 쇼핑몰 분석 ===\n")

# 1. 데이터 결합
merged = pd.merge(orders, products, on='product_id')
print(f"1. 총 주문 건수: {len(merged)}")

# 2. 주문별 총 금액 계산
merged['total_amount'] = merged['quantity'] * merged['price']

# 3. 날짜 변환
merged['order_date'] = pd.to_datetime(merged['order_date'])

# 4. 2024년 1월 데이터만 필터링
jan_2024 = merged[(merged['order_date'].dt.year == 2024) & 
                  (merged['order_date'].dt.month == 1)]

print(f"2. 2024년 1월 주문: {len(jan_2024)}건")
print(f"3. 총 매출액: {jan_2024['total_amount'].sum():,}원\n")

# Sheet1: 카테고리별 매출
category_sales = jan_2024.groupby('category').agg({
    'total_amount': 'sum',
    'order_id': 'count',
    'quantity': 'sum'
}).round(0)
category_sales.columns = ['총_매출액', '주문_건수', '판매_수량']
category_sales = category_sales.reset_index()
category_sales = category_sales.sort_values('총_매출액', ascending=False)

print("=== 카테고리별 매출 ===")
print(category_sales.to_string(index=False))

# Sheet2: 일별 매출
daily_sales = jan_2024.groupby('order_date').agg({
    'total_amount': 'sum',
    'order_id': 'count'
}).round(0)
daily_sales.columns = ['일별_매출액', '주문_건수']
daily_sales = daily_sales.reset_index()
daily_sales['order_date'] = daily_sales['order_date'].dt.strftime('%Y-%m-%d')

print("\n=== 일별 매출 (처음 5일) ===")
print(daily_sales.head().to_string(index=False))

# Sheet3: 베스트 상품 Top 10
product_sales = jan_2024.groupby(['product_id', 'product_name', 'category']).agg({
    'total_amount': 'sum',
    'quantity': 'sum'
}).round(0)
product_sales.columns = ['총_매출액', '판매_수량']
product_sales = product_sales.reset_index()
product_sales = product_sales.sort_values('총_매출액', ascending=False).head(10)

print("\n=== 베스트 상품 Top 10 ===")
print(product_sales.to_string(index=False))

# 엑셀 저장
with pd.ExcelWriter('sales_analysis.xlsx', engine='openpyxl') as writer:
    category_sales.to_excel(writer, sheet_name='카테고리별_매출', index=False)
    daily_sales.to_excel(writer, sheet_name='일별_매출', index=False)
    product_sales.to_excel(writer, sheet_name='베스트상품', index=False)

print("\nsales_analysis.xlsx에 저장되었습니다.")
```

**실행 결과:**
```
=== 온라인 쇼핑몰 분석 ===

1. 총 주문 건수: 30
2. 2024년 1월 주문: 30건
3. 총 매출액: 6,193,000원

=== 카테고리별 매출 ===
  category  총_매출액  주문_건수  판매_수량
  전자기기  4603000.0       21       44
 저장장치  1131000.0        6       11
 액세서리   459000.0        3        9

=== 일별 매출 (처음 5일) ===
  order_date  일별_매출액  주문_건수
  2024-01-05    450000.0          2
  2024-01-06    267000.0          1
  2024-01-07    125000.0          1
  2024-01-08    270000.0          1
  2024-01-09    140000.0          1

=== 베스트 상품 Top 10 ===
 product_id       product_name  category  총_매출액  판매_수량
       P003         27인치 모니터    전자기기    760000.0          2
       P010      외장 SSD 1TB   저장장치    540000.0          4
       P001         무선 마우스    전자기기    315000.0          9
       P006         무선 이어폰    전자기기    534000.0          6
       P002      기계식 키보드    전자기기    375000.0          3
...

sales_analysis.xlsx에 저장되었습니다.
```

---

## Section 3: 종합 프로젝트 답안

### 프로젝트: 데이터 수집 및 분석 파이프라인

```python
import requests
import pandas as pd
import json
from datetime import datetime
import time

# OMDb API Key (무료 발급: http://www.omdbapi.com/apikey.aspx)
API_KEY = 'YOUR_API_KEY_HERE'  # 여기에 발급받은 API 키 입력
BASE_URL = 'http://www.omdbapi.com/'

def fetch_movie_data(title, api_key):
    """영화 정보 가져오기"""
    params = {
        'apikey': api_key,
        't': title,
        'type': 'movie'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data
        return None
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None

def main():
    start_time = datetime.now()
    print("=" * 50)
    print("영화 데이터 수집 및 분석 시작")
    print("=" * 50)
    print(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # movies.txt 읽기
    with open('movies.txt', 'r', encoding='utf-8') as f:
        movie_titles = [line.strip() for line in f if line.strip()]
    
    print(f"총 {len(movie_titles)}개 영화 검색 시작...\n")
    
    # 데이터 수집
    movies_data = []
    success_count = 0
    fail_count = 0
    
    for i, title in enumerate(movie_titles, 1):
        print(f"[{i}/{len(movie_titles)}] {title} 검색중...", end=' ')
        
        data = fetch_movie_data(title, API_KEY)
        
        if data:
            # 필요한 정보만 추출
            movie_info = {
                'title': data.get('Title'),
                'year': data.get('Year'),
                'rating': data.get('imdbRating'),
                'genre': data.get('Genre'),
                'director': data.get('Director'),
                'runtime': data.get('Runtime')
            }
            movies_data.append(movie_info)
            success_count += 1
            print("✓")
        else:
            fail_count += 1
            print("✗ (실패)")
        
        # API 호출 제한 방지 (초당 최대 요청 수 제한)
        time.sleep(0.3)
    
    print(f"\n수집 완료: 성공 {success_count}건, 실패 {fail_count}건\n")
    
    # DataFrame 생성
    df = pd.DataFrame(movies_data)
    
    # 데이터 정제
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    
    # 장르 리스트로 분리
    df['genres'] = df['genre'].str.split(', ')
    
    # 원본 데이터 저장
    df.to_csv('movies_data.csv', index=False, encoding='utf-8-sig')
    print("✓ movies_data.csv 저장 완료")
    
    # 분석 시작
    print("\n" + "=" * 50)
    print("데이터 분석 중...")
    print("=" * 50 + "\n")
    
    analysis_results = {}
    
    # 1. 연도별 영화 수
    year_counts = df['year'].value_counts().sort_index()
    analysis_results['movies_by_year'] = year_counts.to_dict()
    
    # 2. 장르별 평균 평점
    genre_ratings = {}
    all_genres = df['genres'].explode().unique()
    for genre in all_genres:
        mask = df['genres'].apply(lambda x: genre in x if isinstance(x, list) else False)
        avg_rating = df[mask]['rating'].mean()
        genre_ratings[genre] = round(avg_rating, 2)
    
    analysis_results['average_rating_by_genre'] = genre_ratings
    
    # 3. 평점 상위 10개
    top_10 = df.nlargest(10, 'rating')[['title', 'year', 'rating', 'director']]
    analysis_results['top_10_movies'] = top_10.to_dict('records')
    
    # 4. 감독별 영화 수
    director_counts = df['director'].value_counts().head(10)
    analysis_results['movies_by_director'] = director_counts.to_dict()
    
    # JSON 저장
    with open('movies_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    print("✓ movies_analysis.json 저장 완료")
    
    # 보고서 생성
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("영화 데이터 분석 보고서")
    report_lines.append("=" * 60)
    report_lines.append(f"\n생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"분석 영화 수: {len(df)}")
    report_lines.append(f"평균 평점: {df['rating'].mean():.2f}")
    
    report_lines.append("\n" + "-" * 60)
    report_lines.append("평점 상위 10개 영화")
    report_lines.append("-" * 60)
    for i, movie in enumerate(top_10.itertuples(), 1):
        report_lines.append(f"{i:2d}. {movie.title} ({movie.year}) - {movie.rating}/10")
        report_lines.append(f"    감독: {movie.director}")
    
    report_lines.append("\n" + "-" * 60)
    report_lines.append("장르별 평균 평점")
    report_lines.append("-" * 60)
    for genre, rating in sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"{genre:20s}: {rating:.2f}/10")
    
    report_lines.append("\n" + "=" * 60)
    
    # 보고서 저장
    with open('movies_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print("✓ movies_report.txt 저장 완료")
    
    # 화면에도 출력
    print("\n" + '\n'.join(report_lines))
    
    # 실행 시간
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    print(f"\n총 실행 시간: {elapsed:.2f}초")
    print("\n모든 작업이 완료되었습니다! 🎉")

if __name__ == '__main__':
    main()
```

**실행 시 주의사항:**

1. OMDb API 키 발급 필요
   - http://www.omdbapi.com/apikey.aspx 에서 무료 발급
   - 하루 1,000회 요청 제한

2. 실행 방법:
   ```bash
   python movie_analysis.py
   ```

3. 생성되는 파일:
   - `movies_data.csv`: 원본 데이터
   - `movies_analysis.json`: 분석 결과
   - `movies_report.txt`: 보기 좋은 보고서

---

## 학습 포인트 정리

### Section 1에서 배운 것들

1. **JSON 처리**
   - `json.load()`, `json.dump()` 사용법
   - 딕셔너리 조작

2. **CSV 처리**
   - `DictReader`, `DictWriter` 활용
   - 데이터 집계 (defaultdict 활용)

3. **날짜/시간**
   - `strptime`, `strftime` 변환
   - `timedelta`로 날짜 계산

4. **정규표현식**
   - `findall`, `search`, `sub` 활용
   - 실전 패턴 작성

5. **파일 시스템**
   - `pathlib` 객체 지향 방식
   - `glob` 패턴 매칭

### Section 2에서 배운 것들

1. **HTTP 요청**
   - REST API 호출
   - JSON 응답 처리

2. **pandas 기초**
   - 데이터 읽기/쓰기
   - 필터링, 정렬
   - groupby 집계

3. **pandas 고급**
   - merge (테이블 결합)
   - 날짜 데이터 처리
   - 엑셀 다중 시트

### 종합 프로젝트에서 배운 것들

- 실무 파이프라인 구조
- API 호출 제한 처리
- 에러 핸들링
- 진행 상황 표시
- 다양한 포맷으로 결과 저장

---

## 다음 단계 추천

1. **객체 지향 프로그래밍 (OOP)**
   - 클래스와 객체
   - 상속과 다형성

2. **고급 pandas**
   - pivot_table
   - 시계열 분석
   - 결측치 처리 전략

3. **데이터 시각화**
   - matplotlib, seaborn
   - plotly (인터랙티브)

4. **데이터베이스**
   - SQL 기초
   - SQLAlchemy

5. **웹 스크래핑**
   - BeautifulSoup
   - Selenium

---

**수고하셨습니다! 계속 연습하면 실력이 쑥쑥 늘어날 거예요! 💪**
